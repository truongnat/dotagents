#!/usr/bin/env python3
"""Promote Skill: Kiểm định và chuyển draft skill từ staging sang production.

Phần mềm thuộc hệ thống Self-Learning Skill Loop của dotagents.
Hỗ trợ:
- Kiểm tra tính đầy đủ và quy chuẩn của draft `SKILL.md`.
- Chạy linter đối chiếu với quy chuẩn `.agents/AGENTS.md`.
- Chuyển thư mục skill từ `.agents/skills/.staging/<name>` sang `.agents/skills/<name>`
  (hoặc `~/.agents/skills/<name>` khi truyền --global).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> dict[str, str]:
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


def validate_draft_skill(skill_dir: Path) -> list[str]:
    """Kiểm tra tính hợp lệ về nội dung và cấu trúc của draft skill."""
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return [f"Không tìm thấy file SKILL.md trong thư mục {skill_dir}"]

    content = skill_file.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)

    name = fm.get("name", "")
    desc = fm.get("description", "")
    dir_name = skill_dir.name

    if not name:
        errors.append("Thiếu trường 'name' trong YAML frontmatter")
    elif name != dir_name:
        errors.append(f"Tên skill '{name}' không khớp với tên thư mục '{dir_name}'")

    if not desc:
        errors.append("Thiếu trường 'description' trong YAML frontmatter")

    if re.search(r"[^a-z0-9-]", name) or name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append(f"Tên '{name}' không đúng định dạng kebab-case")

    required_sections = [
        "## Khi nào dùng",
        "## Không dùng khi",
        "## Quy trình",
        "## Quy tắc",
        "## Điều kiện hoàn tất"
    ]
    for sec in required_sections:
        if sec not in content:
            errors.append(f"Thiếu phần bắt buộc: '{sec}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote draft skill vào thư mục chính thức")
    parser.add_argument("name", help="Tên skill cần promote (ví dụ: my-new-skill)")
    parser.add_argument("--staging-dir", default=".agents/skills/.staging", help="Thư mục staging (mặc định: .agents/skills/.staging)")
    parser.add_argument("--skills-dir", default=".agents/skills", help="Thư mục skills đích (mặc định: .agents/skills)")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Promote vào ~/.agents/skills/ thay vì dự án hiện tại")
    parser.add_argument("--overwrite", action="store_true", help="Ghi đè nếu skill đã tồn tại ở đích")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ kiểm tra tính hợp lệ mà không thực hiện chuyển file")

    args = parser.parse_args()

    name = args.name.strip()
    staging_dir = Path(args.staging_dir)
    source_dir = staging_dir / name

    if not source_dir.exists():
        print(f"Lỗi: Không tìm thấy draft skill tại: {source_dir.resolve()}", file=sys.stderr)
        return 1

    # 1. Kiểm tra tính hợp lệ của draft skill
    errors = validate_draft_skill(source_dir)
    if errors:
        print(f"[THẤT BẠI] Draft skill '{name}' không đạt tiêu chuẩn:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 2

    # 2. Xác định thư mục đích
    if args.is_global:
        target_base = Path.home() / ".agents" / "skills"
    else:
        target_base = Path(args.skills_dir)

    target_dir = target_base / name

    if target_dir.exists() and not args.overwrite:
        print(f"Lỗi: Skill '{name}' đã tồn tại tại đích: {target_dir.resolve()}", file=sys.stderr)
        print("Sử dụng cờ --overwrite nếu muốn ghi đè lên phiên bản cũ.", file=sys.stderr)
        return 3

    if args.dry_run:
        print(f"[DRY-RUN THÀNH CÔNG] Draft skill '{name}' hoàn toàn hợp lệ.")
        print(f"  Nguồn: {source_dir.resolve()}")
        print(f"  Đích dự kiến: {target_dir.resolve()}")
        return 0

    # 3. Tiến hành promote
    target_base.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(source_dir, target_dir)
    shutil.rmtree(source_dir)

    print(f"[PROMOTED THÀNH CÔNG] Đã chuyển skill '{name}' vào: {target_dir.resolve()}")

    # 4. Xác thực lại với validate-skills.sh nếu ở phạm vi repo
    validate_script = Path(".agents/scripts/validate-skills.sh")
    if not args.is_global and validate_script.exists():
        res = subprocess.run([str(validate_script), str(target_base)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[CẢNH BÁO] validate-skills.sh phát hiện vấn đề:\n{res.stdout}\n{res.stderr}")
        else:
            print(f"[KIỂM ĐỊNH HOÀN TẤT] {res.stdout.strip()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
