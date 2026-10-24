#!/usr/bin/env python3
"""Search memory entries with project-first ordering and metadata filtering.

Maintains all existing search-memory.sh behaviors:
- Project memory checked before global memory (~/.agents/memory)
- Smart-case searching
- Archive excluded by default, included via --archive
- Fallback searching when ripgrep (rg) is not installed

Adds metadata filters:
- --type <bugfix|decision|pattern|workflow|environment>
- --status <active|needs-review|superseded|archived>
- --confidence <high|medium|low>
- --tag <tag>
- --summary (prints concise metadata card: title, status, ID, summary snippet)
"""

from __future__ import annotations

import argparse
import os
import re
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
    current_key: str | None = None
    for line in fm_raw.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            raw_val = m.group(2).strip()
            # Strip inline comments (e.g. status: needs-review # active | ...)
            val_without_comment = raw_val.split("#", 1)[0].strip()
            fields[current_key] = val_without_comment.strip("\"'")
        elif current_key and line.startswith("  "):
            # Multi-line or array entry: strip inline comments too
            clean_item = line_str.split("#", 1)[0].strip().lstrip("- ")
            if clean_item:
                fields[current_key] = (fields.get(current_key, "") + " " + clean_item).strip()
    return fields


def get_memory_paths(custom_project: str | None, custom_home: str | None) -> list[tuple[str, Path]]:
    if custom_project:
        project_root = Path(custom_project)
    elif os.environ.get("PROJECT_ROOT"):
        project_root = Path(os.environ["PROJECT_ROOT"])
    else:
        try:
            out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL)
            project_root = Path(out.decode("utf-8").strip())
        except Exception:
            project_root = Path.cwd()
    agents_home = Path(custom_home) if custom_home else Path(os.environ.get("AGENTS_HOME", Path.home() / ".agents"))

    paths: list[tuple[str, Path]] = []
    p_mem = project_root / ".agents/memory"
    g_mem = agents_home / "memory"
    if p_mem.is_dir():
        paths.append(("project", p_mem))
    if g_mem.is_dir() and g_mem.resolve() != p_mem.resolve():
        paths.append(("global", g_mem))
    return paths


def matches_filter(
    fm: dict[str, str],
    type_filter: str | None,
    status_filter: str | None,
    confidence_filter: str | None,
    tag_filter: str | None,
) -> bool:
    if type_filter and fm.get("type") != type_filter:
        return False
    if status_filter and fm.get("status") != status_filter:
        return False
    if confidence_filter and fm.get("confidence") != confidence_filter:
        return False
    if tag_filter:
        tags = fm.get("tags", "")
        if tag_filter.lower() not in tags.lower():
            return False
    return True


def run_rg(rg_path: str, query: str, files: list[Path]) -> bool:
    if not files:
        return False
    cmd = [rg_path, "--line-number", "--heading", "--color", "never", "--smart-case", "--", query]
    cmd.extend(str(f) for f in files)
    res = subprocess.run(cmd)
    return res.returncode == 0


def run_python_fallback_search(query: str, files: list[Path]) -> bool:
    found = False
    is_lower = query.islower()
    for f in files:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        file_printed = False
        for idx, line in enumerate(lines, 1):
            target = line.lower() if is_lower else line
            q = query.lower() if is_lower else query
            if q in target:
                if not file_printed:
                    print(f"\n{f}:")
                    file_printed = True
                print(f"{idx}:{line}")
                found = True
    return found


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Search memory entries with project-first ordering and metadata filtering.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", nargs="?", default="", help="Từ khóa tìm kiếm (bỏ trống nếu chỉ lọc metadata)")
    parser.add_argument("--archive", action="store_true", help="Bao gồm cả thư mục archive (mặc định bỏ qua)")
    parser.add_argument("--type", choices=["bugfix", "decision", "pattern", "workflow", "environment"], help="Lọc theo type")
    parser.add_argument("--status", choices=["active", "needs-review", "superseded", "archived"], help="Lọc theo status")
    parser.add_argument("--confidence", choices=["high", "medium", "low"], help="Lọc theo confidence")
    parser.add_argument("--tag", help="Lọc theo tag")
    parser.add_argument("--summary", action="store_true", help="Hiển thị tóm tắt ngắn gọn các file khớp")
    parser.add_argument("--project-root", help="Ghi đè đường dẫn project root")
    parser.add_argument("--agents-home", help="Ghi đè đường dẫn AGENTS_HOME")

    args = parser.parse_args()

    paths = get_memory_paths(args.project_root, args.agents_home)
    if not paths:
        print("Không tìm thấy thư mục memory nào trong project hoặc AGENTS_HOME.", file=sys.stderr)
        return 1

    scope_str = " (bao gồm archive)" if args.archive else " (chỉ corpus hiện hành)"
    query_display = args.query if args.query else "(lọc theo metadata)"
    print(f"Truy vấn: {query_display}")
    print(f"Thứ tự phạm vi: project → global{scope_str}\n")

    rg_path = None
    try:
        which_out = subprocess.check_output(["which", "rg"], stderr=subprocess.DEVNULL)
        rg_path = which_out.decode("utf-8").strip()
    except Exception:
        rg_path = None

    total_matches = 0
    for scope_name, dir_path in paths:
        candidate_files: list[Path] = []
        for f in sorted(dir_path.rglob("*.md")):
            if f.name in ("README.md", "INDEX.md"):
                continue
            if not args.archive and "archive" in f.parts:
                continue

            fm = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))

            # Default active policy: if --archive is not passed and no explicit --status is given,
            # exclude superseded and archived entries even if placed outside the archive/ directory
            if not args.archive and not args.status:
                entry_status = fm.get("status", "active")
                if entry_status in ("archived", "superseded"):
                    continue

            # Apply explicit metadata filter
            if any([args.type, args.status, args.confidence, args.tag]):
                if not matches_filter(fm, args.type, args.status, args.confidence, args.tag):
                    continue
            candidate_files.append((f, fm))

        if not candidate_files:
            continue

        # Rank candidates: active > needs-review > others; high > medium > low
        status_rank = {"active": 0, "needs-review": 1, "superseded": 2, "archived": 3}
        conf_rank = {"high": 0, "medium": 1, "low": 2}
        candidate_files.sort(
            key=lambda item: (
                status_rank.get(item[1].get("status", ""), 9),
                conf_rank.get(item[1].get("confidence", ""), 9),
                item[0].name,
            )
        )
        ranked_files = [f for f, _ in candidate_files]
        if args.summary:
            print(f"--- Phạm vi: {scope_name} ({dir_path}) ---")
            for f, fm in candidate_files:
                title = fm.get("title", "(không có tiêu đề)")
                st = fm.get("status", "unknown")
                typ = fm.get("type", "unknown")
                mem_id = fm.get("id", f.stem)
                print(f"[{mem_id}] ({typ} | {st}) {title}\n  File: {f}")
                total_matches += 1
            print()
            continue

        if not args.query:
            # Metadata filter only without search query: list files
            print(f"--- Phạm vi: {scope_name} ({dir_path}) ---")
            for f in ranked_files:
                print(f"  {f}")
                total_matches += 1
            print()
            continue

        # Content text search
        matched = False
        if rg_path:
            matched = run_rg(rg_path, args.query, ranked_files)
        else:
            matched = run_python_fallback_search(args.query, ranked_files)

        if matched:
            total_matches += 1
            print()

    if total_matches == 0:
        print("Không có kết quả phù hợp.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
