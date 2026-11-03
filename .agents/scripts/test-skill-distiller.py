#!/usr/bin/env python3
"""Unit tests cho skill-distiller.py và promote-skill.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys

SCRIPTS_DIR = Path(__file__).resolve().parent
distiller_mod = SourceFileLoader("skill_distiller", str(SCRIPTS_DIR / "skill-distiller.py")).load_module()
promote_mod = SourceFileLoader("promote_skill", str(SCRIPTS_DIR / "promote-skill.py")).load_module()


def test_kebab_case() -> None:
    assert distiller_mod.to_kebab_case("My New Feature") == "my-new-feature"
    assert distiller_mod.to_kebab_case("Docker_PG_Migrate-2026!") == "docker-pg-migrate-2026"
    assert distiller_mod.to_kebab_case("---bad---name---") == "bad-name"


def test_render_skill_md() -> None:
    content = distiller_mod.render_skill_md(
        name="test-skill",
        description="Mô tả kỹ năng kiểm thử",
        triggers=["Khi chạy unit test"],
        anti_triggers=["Khi deploy production"],
        procedure=["Chạy pytest", "Kiểm tra exit code"],
        rules=["Không bỏ qua assert"],
        gotchas=["Chú ý timeout"],
        code_snippets=["pytest -v"]
    )
    assert content.startswith("---\nname: test-skill\n")
    assert 'description: "Mô tả kỹ năng kiểm thử"' in content
    assert "## Khi nào dùng" in content
    assert "- Khi chạy unit test" in content
    assert "## Không dùng khi" in content
    assert "## Quy trình" in content
    assert "1. Chạy pytest" in content
    assert "## Quy tắc" in content
    assert "## Các bẫy thường gặp & Xử lý sự cố" in content
    assert "## Đoạn mã / Lệnh mẫu" in content
    assert "```bash\npytest -v\n```" in content
    assert "## Điều kiện hoàn tất" in content


def test_similarity_and_deduplication() -> None:
    with tempfile.TemporaryDirectory() as td:
        skills_dir = Path(td)
        existing_skill_dir = skills_dir / "sqlite-wal-optimization"
        existing_skill_dir.mkdir(parents=True)
        (existing_skill_dir / "SKILL.md").write_text("""---
name: sqlite-wal-optimization
description: "Tối ưu hóa ghi đồng thời và chống khóa DB với SQLite WAL mode"
---
# SQLite WAL Optimization
## Khi nào dùng
- Khi gặp SQLite database locked
""", encoding="utf-8")

        # Test trùng lặp cao
        similar = distiller_mod.find_similar_skills(
            name="sqlite-wal-lock-fix",
            description="Tối ưu hóa và chống khóa SQLite WAL mode",
            skills_dir=skills_dir
        )
        assert len(similar) >= 1
        name, sim, _ = similar[0]
        assert name == "sqlite-wal-optimization"
        assert sim > 0.4


def test_end_to_end_distill_and_promote() -> None:
    with tempfile.TemporaryDirectory() as td:
        base_dir = Path(td)
        staging_dir = base_dir / "staging"
        skills_dir = base_dir / "skills"
        skills_dir.mkdir(parents=True)

        payload_path = base_dir / "lesson.json"
        payload_data = {
            "name": "auto-cache-busting",
            "description": "Tự động xóa cache tài nguyên tĩnh khi build tài sản frontend",
            "triggers": ["Khi deploy frontend assets mới"],
            "anti_triggers": ["Khi chỉ sửa backend API"],
            "procedure": ["Sinh content hash", "Cập nhật manifest.json"],
            "rules": ["Bắt buộc dùng SHA-256"],
            "gotchas": ["Tránh hardcode timestamp"],
            "code_snippets": ["npm run build -- --hash"]
        }
        payload_path.write_text(json.dumps(payload_data, ensure_ascii=False), encoding="utf-8")

        # 1. Chạy distiller
        cmd_distill = [
            sys.executable,
            str(SCRIPTS_DIR / "skill-distiller.py"),
            "--payload", str(payload_path),
            "--skills-dir", str(skills_dir),
            "--staging-dir", str(staging_dir)
        ]
        res_distill = subprocess.run(cmd_distill, capture_output=True, text=True)
        assert res_distill.returncode == 0, f"Distill failed: {res_distill.stderr}"

        draft_file = staging_dir / "auto-cache-busting" / "SKILL.md"
        assert draft_file.exists()

        # 2. Chạy promote dry-run
        cmd_dry_run = [
            sys.executable,
            str(SCRIPTS_DIR / "promote-skill.py"),
            "auto-cache-busting",
            "--staging-dir", str(staging_dir),
            "--skills-dir", str(skills_dir),
            "--dry-run"
        ]
        res_dry_run = subprocess.run(cmd_dry_run, capture_output=True, text=True)
        assert res_dry_run.returncode == 0, f"Dry run failed: {res_dry_run.stderr}"

        # 3. Chạy promote chính thức
        cmd_promote = [
            sys.executable,
            str(SCRIPTS_DIR / "promote-skill.py"),
            "auto-cache-busting",
            "--staging-dir", str(staging_dir),
            "--skills-dir", str(skills_dir)
        ]
        res_promote = subprocess.run(cmd_promote, capture_output=True, text=True)
        assert res_promote.returncode == 0, f"Promote failed: {res_promote.stderr}"

        promoted_file = skills_dir / "auto-cache-busting" / "SKILL.md"
        assert promoted_file.exists()
        assert not draft_file.exists()


def main() -> int:
    print("Running test_kebab_case...")
    test_kebab_case()
    print("Running test_render_skill_md...")
    test_render_skill_md()
    print("Running test_similarity_and_deduplication...")
    test_similarity_and_deduplication()
    print("Running test_end_to_end_distill_and_promote...")
    test_end_to_end_distill_and_promote()
    print("ALL TESTS PASSED! (4/4 test suites)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
