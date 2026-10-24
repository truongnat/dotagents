#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== Kiểm tra sức khỏe dotagents framework ==="
echo "Đường dẫn gốc: $ROOT_DIR"
echo

failures=0

# 1. Kiểm tra cấu trúc thư mục cốt lõi
echo "[1/4] Kiểm tra thư mục cốt lõi:"
required_dirs=("rules" "skills" "scripts" "template" "memory")
for d in "${required_dirs[@]}"; do
  if [[ -d "$ROOT_DIR/.agents/$d" ]]; then
    echo "  ✓ .agents/$d"
  else
    echo "  ✗ Thiếu thư mục .agents/$d"
    failures=$((failures + 1))
  fi
done

# 2. Kiểm tra quyền thực thi của scripts
echo
echo "[2/4] Kiểm tra quyền thực thi scripts:"
for s in "$SCRIPT_DIR"/*.sh "$SCRIPT_DIR"/*.py; do
  [[ ! -f "$s" ]] && continue
  fname="$(basename "$s")"
  if [[ -x "$s" ]]; then
    echo "  ✓ $fname (executable)"
  else
    echo "  ✗ $fname (chưa có chmod +x)"
    failures=$((failures + 1))
  fi
done

# 3. Chạy validate-skills.sh
echo
echo "[3/4] Kiểm tra tính hợp lệ của Skills:"
if "$SCRIPT_DIR/validate-skills.sh" "$ROOT_DIR/.agents/skills"; then
  echo "  ✓ Toàn bộ skills hợp chuẩn YAML frontmatter"
else
  echo "  ✗ Lỗi định dạng skills"
  failures=$((failures + 1))
fi

# 4. Chạy validate-memory.py
echo
echo "[4/4] Kiểm tra tính hợp lệ của Memory Schema:"
if python3 "$SCRIPT_DIR/validate-memory.py" "$ROOT_DIR/.agents/memory/entries"; then
  echo "  ✓ Toàn bộ memory entries đạt 15 trường frontmatter và enum chuẩn"
else
  echo "  ✗ Lỗi định dạng memory entries"
  failures=$((failures + 1))
fi

# 5. Chạy unit tests
echo
if python3 "$SCRIPT_DIR/test-validate-memory.py" && python3 "$SCRIPT_DIR/test-search-memory.py"; then
  echo "  ✓ Unit tests passing (validate-memory, search-memory)"
else
  echo "  ✗ Unit tests failed"
  failures=$((failures + 1))
fi

echo
if (( failures == 0 )); then
  echo "===> KẾT QUẢ: MỌI THỨ HOÀN TOÀN TỐT! (0 lỗi) <==="
  exit 0
else
  echo "===> KẾT QUẢ: Phát hiện $failures lỗi cần xử lý! <==="
  exit 1
fi
