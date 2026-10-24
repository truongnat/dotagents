#!/usr/bin/env python3
"""Validate memory entry files against .agents/rules/memory-policy.md schema.

Checks:
1. File naming: YYYY-MM-DD-<type>-<short-topic>.md (or legacy index/readme exemption)
2. Valid YAML frontmatter demarcated by ---
3. Exactly 15 required metadata fields:
   schema_version, id, title, type, scope, status, created, updated,
   verified_on, confidence, tags, applies_to, sources, related, supersedes
4. Valid enum values for type, scope, status, confidence
5. Date format ISO YYYY-MM-DD (or 'unknown' for verified_on)
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "title",
    "type",
    "scope",
    "status",
    "created",
    "updated",
    "verified_on",
    "confidence",
    "tags",
    "applies_to",
    "sources",
    "related",
    "supersedes",
)

ALLOWED_TYPES = {"bugfix", "decision", "pattern", "workflow", "environment"}
ALLOWED_SCOPES = {"global", "project"}
ALLOWED_STATUSES = {"active", "needs-review", "superseded", "archived"}
ALLOWED_CONFIDENCES = {"high", "medium", "low"}

FILENAME_PATTERN = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<type>[a-z]+)-(?P<slug>[a-z0-9-]+)\.md$"
)


def parse_frontmatter(content: str) -> tuple[dict[str, str], str] | None:
    if not content.startswith("---\n"):
        return None
    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return None
    fm_raw = parts[1]
    body = parts[2]

    # Minimal YAML key parser for top-level keys without external dependencies
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in fm_raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        # Top-level key: no leading spaces, ends before colon
        m = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if m:
            current_key = m.group(1)
            fields[current_key] = m.group(2).strip()
        elif current_key and line.startswith("  "):
            # Sub-field or list item, keep key present
            pass
    return fields, body


def is_valid_iso_date(val: str) -> bool:
    clean = val.strip("\"'")
    try:
        datetime.strptime(clean, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    fname = path.name

    # Check filename conventions
    m = FILENAME_PATTERN.match(fname)
    if not m:
        errors.append(f"Tên file '{fname}' không đúng định dạng YYYY-MM-DD-<type>-<short-topic>.md")
    else:
        file_date = m.group("date")
        file_type = m.group("type")
        if not is_valid_iso_date(file_date):
            errors.append(f"Ngày trong tên file '{file_date}' không phải ngày ISO hợp lệ")
        if file_type not in ALLOWED_TYPES:
            errors.append(f"Type trong tên file '{file_type}' không thuộc danh mục: {sorted(ALLOWED_TYPES)}")

    content = path.read_text(encoding="utf-8")
    fm_res = parse_frontmatter(content)
    if not fm_res:
        errors.append("Thiếu hoặc sai cấu trúc YAML frontmatter (phải bao bởi ---)")
        return errors

    fields, _ = fm_res

    # Check all 15 required fields
    for req in REQUIRED_FIELDS:
        if req not in fields:
            errors.append(f"Thiếu trường bắt buộc trong frontmatter: '{req}'")

    # Check enum values if present
    if "type" in fields:
        raw_type = fields["type"].split("#")[0].strip().strip("\"'")
        if raw_type not in ALLOWED_TYPES:
            errors.append(f"Giá trị 'type' không hợp lệ: '{raw_type}' (cho phép: {sorted(ALLOWED_TYPES)})")
        if m and raw_type != m.group("type"):
            errors.append(f"Type trong frontmatter ('{raw_type}') không khớp type ở tên file ('{m.group('type')}')")

    if "scope" in fields:
        raw_scope = fields["scope"].split("#")[0].strip().strip("\"'")
        if raw_scope not in ALLOWED_SCOPES:
            errors.append(f"Giá trị 'scope' không hợp lệ: '{raw_scope}' (cho phép: {sorted(ALLOWED_SCOPES)})")

    if "status" in fields:
        raw_status = fields["status"].split("#")[0].strip().strip("\"'")
        if raw_status not in ALLOWED_STATUSES:
            errors.append(f"Giá trị 'status' không hợp lệ: '{raw_status}' (cho phép: {sorted(ALLOWED_STATUSES)})")

    if "confidence" in fields:
        raw_conf = fields["confidence"].split("#")[0].strip().strip("\"'")
        if raw_conf not in ALLOWED_CONFIDENCES:
            errors.append(f"Giá trị 'confidence' không hợp lệ: '{raw_conf}' (cho phép: {sorted(ALLOWED_CONFIDENCES)})")

    # Check date fields
    for date_field in ("created", "updated"):
        if date_field in fields:
            raw_d = fields[date_field].split("#")[0].strip().strip("\"'")
            if not is_valid_iso_date(raw_d):
                errors.append(f"Trường '{date_field}' không đúng định dạng YYYY-MM-DD: '{raw_d}'")

    if "verified_on" in fields:
        raw_v = fields["verified_on"].split("#")[0].strip().strip("\"'")
        if raw_v != "unknown" and not is_valid_iso_date(raw_v):
            errors.append(f"Trường 'verified_on' phải là YYYY-MM-DD hoặc 'unknown': '{raw_v}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate memory entry files against memory-policy.md schema.")
    parser.add_argument("paths", nargs="*", default=[".agents/memory/entries", ".agents/memory/archive"],
                        help="Directories or files to validate (default: .agents/memory/entries, .agents/memory/archive)")
    args = parser.parse_args()

    files_to_check: list[Path] = []
    for p_str in args.paths:
        p = Path(p_str)
        if p.is_file():
            if p.suffix == ".md" and p.name != "README.md" and p.name != "INDEX.md":
                files_to_check.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*.md")):
                if f.name not in ("README.md", "INDEX.md"):
                    files_to_check.append(f)

    if not files_to_check:
        print("Không tìm thấy memory entry nào để kiểm tra (ngoại trừ README/INDEX).")
        return 0

    total_errors = 0
    for f in files_to_check:
        errs = validate_file(f)
        if errs:
            total_errors += len(errs)
            print(f"FAIL {f}:")
            for e in errs:
                print(f"  - {e}")

    if total_errors > 0:
        print(f"\nKiểm tra thất bại: {total_errors} lỗi trên {len(files_to_check)} file.")
        return 1

    print(f"OK: đã kiểm tra {len(files_to_check)} memory entry, tất cả đều hợp lệ theo memory-policy.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
