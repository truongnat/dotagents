#!/usr/bin/env python3
"""Focused tests for search-memory.py metadata parsing, comment stripping, ranking, and PROJECT_ROOT."""

from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent / "search-memory.py"


def test_frontmatter_comment_stripping() -> None:
    content = """---
schema_version: 1
status: needs-review # active | needs-review | superseded | archived
type: bugfix # bugfix | decision
confidence: high # note
tags: [sqlite, wal] # inline tag comment
---

# Body
"""
    from importlib.machinery import SourceFileLoader
    mod = SourceFileLoader("search_mem", str(SCRIPT_PATH)).load_module()

    fm = mod.parse_frontmatter(content)
    assert fm.get("status") == "needs-review", f"Failed to strip comment: {fm.get('status')}"
    assert fm.get("type") == "bugfix", f"Failed to strip comment: {fm.get('type')}"
    assert fm.get("confidence") == "high", f"Failed to strip comment: {fm.get('confidence')}"
    assert "sqlite" in fm.get("tags", "")


def test_search_cli_filter_with_comments_and_env() -> None:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        mem_dir = root / ".agents/memory/entries/bugfixes"
        mem_dir.mkdir(parents=True)
        entry_file = mem_dir / "2026-10-24-bugfix-wal-lock.md"
        entry_file.write_text(
            """---
schema_version: 1
id: "MEM-20261024-wal-lock"
title: "SQLite concurrency busy lock"
type: bugfix # bugfix | decision
scope: project # project | global
status: active # active | needs-review
confidence: high # high | medium
tags: [sqlite, wal]
applies_to: {repo: "any"}
sources: ["sqlite.rs"]
related: []
supersedes: null
---

# Summary
WAL mode resolves busy locking.
""",
            encoding="utf-8",
        )

        # 1. Search with PROJECT_ROOT env and --status active
        env = os.environ.copy()
        env["PROJECT_ROOT"] = str(root)
        cmd = ["python3", str(SCRIPT_PATH), "locking", "--status", "active"]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
        assert res.returncode == 0
        assert "MEM-20261024-wal-lock" in res.stdout or "WAL mode resolves busy locking" in res.stdout, res.stdout

        # 2. Search with --status needs-review should return no results
        cmd_neg = ["python3", str(SCRIPT_PATH), "locking", "--status", "needs-review"]
        res_neg = subprocess.run(cmd_neg, env=env, capture_output=True, text=True)
        assert res_neg.returncode == 0
        assert "Không có kết quả phù hợp" in res_neg.stdout

        # 3. Add superseded entry outside archive/
        sup_file = mem_dir / "2026-10-24-bugfix-old-lock.md"
        sup_file.write_text(
            """---
schema_version: 1
id: "MEM-20261024-old-lock"
title: "Old lock workaround"
type: bugfix
status: superseded
confidence: low
---

# Summary
locking obsolete workaround
""",
            encoding="utf-8",
        )

        # Without --archive and without explicit --status, superseded must be excluded by default
        cmd_default = ["python3", str(SCRIPT_PATH), "workaround"]
        res_default = subprocess.run(cmd_default, env=env, capture_output=True, text=True)
        assert "Không có kết quả phù hợp" in res_default.stdout

        # With --archive, superseded entry is included
        cmd_arch = ["python3", str(SCRIPT_PATH), "workaround", "--archive"]
        res_arch = subprocess.run(cmd_arch, env=env, capture_output=True, text=True)
        assert "Old lock workaround" in res_arch.stdout or "workaround" in res_arch.stdout


def main() -> int:
    test_frontmatter_comment_stripping()
    test_search_cli_filter_with_comments_and_env()
    print("test_search_memory: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
