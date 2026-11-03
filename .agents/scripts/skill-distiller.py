#!/usr/bin/env python3
"""Skill Distiller: Tự động trích xuất, kiểm tra trùng lặp và sinh draft skill.

Phần mềm thuộc hệ thống Self-Learning Skill Loop của dotagents.
Hỗ trợ:
- Nhận input từ file JSON, CLI arguments hoặc văn bản reflection.
- Đối chiếu kiểm tra trùng lặp (lexical similarity & token overlap) với kho skills hiện có.
- Sinh file draft `SKILL.md` chuẩn hóa tại `.agents/skills/.staging/<skill-name>/SKILL.md`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


def to_kebab_case(s: str) -> str:
    """Chuyển chuỗi thành chuẩn kebab-case hợp lệ."""
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s_-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def parse_frontmatter(content: str) -> dict[str, str]:
    """Trích xuất frontmatter YAML đơn giản."""
    if not content.startswith("---\n"):
        return {}
    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return {}
    fm_raw = parts[1]
    fields: dict[str, str] = {}
    for line in fm_raw.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            raw_val = m.group(2).strip().strip("\"'")
            fields[key] = raw_val
    return fields


def tokenize(text: str) -> set[str]:
    """Tách từ ngữ nghĩa để tính độ tương đồng (hỗ trợ cả tiếng Việt unicode)."""
    words = re.findall(r"[\w-]{2,}", text.lower())
    # Bỏ stop words cơ bản
    stop_words = {
        "and", "the", "for", "with", "from", "when", "that", "this", "skill",
        "dùng", "khi", "cho", "với", "trong", "các", "những", "được", "hoặc", "của", "và"
    }
    return {w for w in words if w not in stop_words}


def compute_similarity(tokens1: set[str], tokens2: set[str]) -> float:
    """Tính độ tương đồng Jaccard giữa 2 tập từ."""
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)


def find_similar_skills(
    name: str,
    description: str,
    skills_dir: Path
) -> list[tuple[str, float, str]]:
    """Tìm kiếm các skill hiện có có nội dung/mục đích tương đồng."""
    results: list[tuple[str, float, str]] = []
    if not skills_dir.exists():
        return results

    query_tokens = tokenize(f"{name} {description}")

    for skill_path in skills_dir.glob("*/SKILL.md"):
        if ".staging" in skill_path.parts:
            continue
        existing_name = skill_path.parent.name
        try:
            content = skill_path.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = parse_frontmatter(content)
        existing_desc = fm.get("description", "")
        existing_tokens = tokenize(f"{existing_name} {existing_desc}")

        sim = compute_similarity(query_tokens, existing_tokens)
        if sim > 0.35:  # Ngưỡng phát hiện tương đồng đáng chú ý
            results.append((existing_name, sim, existing_desc))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def render_skill_md(
    name: str,
    description: str,
    triggers: list[str],
    anti_triggers: list[str],
    procedure: list[str],
    rules: list[str],
    gotchas: list[str],
    code_snippets: list[str]
) -> str:
    """Tạo nội dung SKILL.md theo đúng template chuẩn."""
    lines = [
        "---",
        f"name: {name}",
        f"description: \"{description}\"",
        "---",
        f"# {name}",
        "",
        "## Khi nào dùng",
    ]
    if triggers:
        for t in triggers:
            lines.append(f"- {t}")
    else:
        lines.append("- Áp dụng khi gặp ngữ cảnh tương tự mô tả.")

    lines.extend(["", "## Không dùng khi"])
    if anti_triggers:
        for at in anti_triggers:
            lines.append(f"- {at}")
    else:
        lines.append("- Không áp dụng khi bài toán nằm ngoài phạm vi mô tả.")

    lines.extend(["", "## Quy trình"])
    if procedure:
        for idx, step in enumerate(procedure, 1):
            lines.append(f"{idx}. {step}")
    else:
        lines.append("1. Đọc và xác định điều kiện tiền đề.")
        lines.append("2. Thực thi tuần tự các bước kiểm chứng.")
        lines.append("3. Kiểm tra kết quả thực tế.")

    lines.extend(["", "## Quy tắc"])
    if rules:
        for r in rules:
            lines.append(f"- {r}")
    else:
        lines.append("- Phải kiểm chứng kết quả thực tế trước khi kết luận.")
        lines.append("- Giữ thay đổi ở mức tối thiểu (minimal diff).")

    if gotchas:
        lines.extend(["", "## Các bẫy thường gặp & Xử lý sự cố"])
        for g in gotchas:
            lines.append(f"- {g}")

    if code_snippets:
        lines.extend(["", "## Đoạn mã / Lệnh mẫu"])
        for snippet in code_snippets:
            lines.append("```bash")
            lines.append(snippet.strip())
            lines.append("```")

    lines.extend(["", "## Điều kiện hoàn tất", "- Thao tác kiểm chứng thành công và không phát sinh lỗi ngoại lệ.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Distiller - Tự động trích xuất và sinh draft skill")
    parser.add_argument("--name", help="Tên skill (kebab-case)")
    parser.add_argument("--description", help="Mô tả mục đích và trigger của skill")
    parser.add_argument("--payload", help="Đường dẫn file JSON chứa thông tin bài học đúc kết")
    parser.add_argument("--skills-dir", default=".agents/skills", help="Thư mục skills chính (mặc định: .agents/skills)")
    parser.add_argument("--staging-dir", default=".agents/skills/.staging", help="Thư mục staging cho draft skills")
    parser.add_argument("--trigger", action="append", default=[], help="Thêm điều kiện kích hoạt")
    parser.add_argument("--anti-trigger", action="append", default=[], help="Thêm điều kiện không áp dụng")
    parser.add_argument("--step", action="append", default=[], help="Thêm bước thực hiện trong quy trình")
    parser.add_argument("--rule", action="append", default=[], help="Thêm quy tắc bắt buộc")
    parser.add_argument("--gotcha", action="append", default=[], help="Thêm cạm bẫy / lưu ý")
    parser.add_argument("--code", action="append", default=[], help="Thêm đoạn mã / lệnh mẫu")
    parser.add_argument("--force", action="store_true", help="Bỏ qua cảnh báo trùng lặp và tạo draft mới")

    args = parser.parse_args()

    # Nạp dữ liệu từ payload JSON nếu có
    data: dict[str, Any] = {}
    if args.payload:
        p_path = Path(args.payload)
        if not p_path.exists():
            print(f"Lỗi: File payload không tồn tại: {args.payload}", file=sys.stderr)
            return 1
        with open(p_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    raw_name = args.name or data.get("name")
    if not raw_name:
        print("Lỗi: Thiếu tên skill (--name hoặc trong --payload)", file=sys.stderr)
        return 1

    name = to_kebab_case(raw_name)
    description = (args.description or data.get("description") or "").strip()
    if not description:
        print("Lỗi: Thiếu mô tả skill (--description hoặc trong --payload)", file=sys.stderr)
        return 1

    triggers = args.trigger or data.get("triggers", [])
    anti_triggers = args.anti_trigger or data.get("anti_triggers", [])
    procedure = args.step or data.get("procedure", [])
    rules = args.rule or data.get("rules", [])
    gotchas = args.gotcha or data.get("gotchas", [])
    code_snippets = args.code or data.get("code_snippets", [])

    skills_dir = Path(args.skills_dir)
    staging_dir = Path(args.staging_dir)

    # 1. Kiểm tra trùng lặp
    similar = find_similar_skills(name, description, skills_dir)
    if similar:
        top_name, top_sim, top_desc = similar[0]
        if top_sim >= 0.65 and not args.force:
            print(f"[CẢNH BÁO TRÙNG LẶP] Skill '{name}' có độ tương đồng cao ({top_sim:.1%}) với skill hiện có '{top_name}'.")
            print(f"  Mô tả hiện có: {top_desc}")
            print("  Khuyến nghị: Thay vì tạo skill mới, hãy cập nhật vào skill sẵn có hoặc dùng cờ --force để tiếp tục.")
            return 2
        else:
            print(f"[THÔNG BÁO] Phát hiện {len(similar)} skill có điểm chung:")
            for s_name, s_sim, _ in similar[:3]:
                print(f"  - {s_name} (độ tương đồng: {s_sim:.1%})")

    # 2. Sinh nội dung SKILL.md
    content = render_skill_md(
        name=name,
        description=description,
        triggers=triggers,
        anti_triggers=anti_triggers,
        procedure=procedure,
        rules=rules,
        gotchas=gotchas,
        code_snippets=code_snippets
    )

    # 3. Ghi vào thư mục staging
    draft_skill_dir = staging_dir / name
    draft_skill_dir.mkdir(parents=True, exist_ok=True)
    draft_file = draft_skill_dir / "SKILL.md"

    draft_file.write_text(content, encoding="utf-8")
    print(f"[THÀNH CÔNG] Đã tạo draft skill tại: {draft_file.resolve()}")
    print("Tiếp theo: Dùng 'scripts/promote-skill.py' để kiểm định và chuyển vào danh mục chính thức.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
