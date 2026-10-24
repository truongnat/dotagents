#!/usr/bin/env python3
"""Unit tests for validate-memory.py."""

from __future__ import annotations

import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib.machinery import SourceFileLoader

mod = SourceFileLoader("validate_memory", str(Path(__file__).resolve().parent / "validate-memory.py")).load_module()


def test_valid_entry() -> None:
    valid_content = """---
schema_version: 1
id: "MEM-20261024-sqlite-wal-locking"
title: "SQLite WAL mode avoids busy lock on concurrent reads"
type: bugfix
scope: project
status: active
created: "2026-10-24"
updated: "2026-10-24"
verified_on: "2026-10-24"
confidence: high
tags: [sqlite, concurrency, wal]
applies_to:
  repo: "any"
  stack: "sqlite"
  versions: ">=3.7.0"
sources:
  - "crates/infra/sqlite.rs"
related: []
supersedes: null
---

# Tóm tắt
Chi tiết...
"""
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "2026-10-24-bugfix-sqlite-wal-locking.md"
        f.write_text(valid_content, encoding="utf-8")
        errs = mod.validate_file(f)
        assert errs == [], f"Unexpected errors: {errs}"


def test_missing_fields_and_invalid_enum() -> None:
    invalid_content = """---
schema_version: 1
id: "MEM-test"
type: invalid_type
status: in_progress
created: "not-a-date"
---
"""
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "bad-name.md"
        f.write_text(invalid_content, encoding="utf-8")
        errs = mod.validate_file(f)
        assert any("Tên file" in e for e in errs)
        assert any("Thiếu trường bắt buộc" in e for e in errs)
        assert any("Giá trị 'type' không hợp lệ" in e for e in errs)
        assert any("Giá trị 'status' không hợp lệ" in e for e in errs)
        assert any("created" in e for e in errs)


def main() -> int:
    test_valid_entry()
    test_missing_fields_and_invalid_enum()
    print("test_validate_memory: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
