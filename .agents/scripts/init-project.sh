#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Cách dùng:
  init-project.sh [--force] <thư-mục-project-đích>

Khởi tạo cấu trúc .agents/ và AGENTS.md cho một repository mới từ dotagents framework.
Mặc định an toàn: KHÔNG ghi đè các file đã tồn tại (như .agents/rules/project.md, AGENTS.md, ...)
trừ khi truyền cờ --force.

Ví dụ:
  ./init-project.sh ~/tx/GitHub/my-new-app
  ./init-project.sh --force ~/tx/GitHub/my-new-app
USAGE
}

force=false
target_arg=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force|-f)
      force=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$target_arg" ]]; then
        target_arg="$1"
      else
        echo "Lỗi: quá nhiều tham số vị trí: $1" >&2
        usage >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ -z "$target_arg" ]]; then
  usage >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Ensure target directory exists first so cd/pwd resolves absolute path cleanly
mkdir -p "$target_arg"
TARGET="$(cd "$target_arg" && pwd)"


copy_file_safe() {
  local src="$1"
  local dest="$2"
  local rel="$3"

  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" && "$force" != true ]]; then
    echo "  - Giữ nguyên (đã tồn tại): $rel"
  else
    cp "$src" "$dest"
    echo "  + Sao chép: $rel"
  fi
}

# 1. Root AGENTS.md
copy_file_safe "$ROOT_DIR/AGENTS.md" "$TARGET/AGENTS.md" "AGENTS.md"

# 2. .agents/AGENTS.md
if [[ -f "$ROOT_DIR/.agents/AGENTS.md" ]]; then
  copy_file_safe "$ROOT_DIR/.agents/AGENTS.md" "$TARGET/.agents/AGENTS.md" ".agents/AGENTS.md"
fi

# 3. Toàn bộ file bên dưới .agents/ (bỏ qua __pycache__, *.pyc, .DS_Store, artifact tạm)
cd "$ROOT_DIR"
find .agents -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' | while IFS= read -r rel_file; do
  [[ "$rel_file" == ".agents/AGENTS.md" ]] && continue
  copy_file_safe "$ROOT_DIR/$rel_file" "$TARGET/$rel_file" "$rel_file"
done

# Đảm bảo scripts có quyền thực thi
chmod +x "$TARGET/.agents/scripts/"*.sh "$TARGET/.agents/scripts/"*.py 2>/dev/null || true

echo "==> Khởi tạo thành công!"
echo "Bước tiếp theo:"
echo "  1. Mở file: $TARGET/.agents/rules/project.md và điền stack, lệnh test/run của project."
echo "  2. Chạy: $TARGET/.agents/scripts/doctor.sh để kiểm tra tính toàn vẹn."
