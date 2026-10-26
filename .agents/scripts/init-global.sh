#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Cách dùng:
  init-global.sh [--force] [thư-mục-đích]

Khởi tạo cấu trúc dotagents toàn cục (Global Framework) cho người dùng.
Mặc định cài đặt vào: ~/.agents (hoặc thư mục đích nếu được chỉ định).

Mặc định an toàn: KHÔNG ghi đè các file đã tồn tại trừ khi truyền cờ --force (-f).

Ví dụ:
  ./init-global.sh
  ./init-global.sh --force
  ./init-global.sh /path/to/custom-global-agents
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
  target_arg="${HOME:-~}/.agents"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

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

# 1. Global AGENTS.md (lấy từ .agents/AGENTS.md - quy trình làm việc chuẩn của dotagents)
if [[ -f "$ROOT_DIR/.agents/AGENTS.md" ]]; then
  copy_file_safe "$ROOT_DIR/.agents/AGENTS.md" "$TARGET/AGENTS.md" "AGENTS.md"
fi

# 2. Toàn bộ file bên dưới .agents/ (bỏ qua AGENTS.md, project.md và cache)
cd "$ROOT_DIR/.agents"
find . -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '.DS_Store' | while IFS= read -r rel_file; do
  rel_file="${rel_file#./}"
  [[ "$rel_file" == "AGENTS.md" ]] && continue
  [[ "$rel_file" == "rules/project.md" ]] && continue
  copy_file_safe "$ROOT_DIR/.agents/$rel_file" "$TARGET/$rel_file" "$rel_file"
done

# Đảm bảo scripts có quyền thực thi
chmod +x "$TARGET/scripts/"*.sh "$TARGET/scripts/"*.py 2>/dev/null || true

echo "==> Khởi tạo Global dotagents thành công tại: $TARGET"
echo "Bước tiếp theo:"
echo "  1. Cấu hình agent của bạn để đọc: $TARGET/AGENTS.md làm Global Instructions."
echo "  2. Chạy: $TARGET/scripts/doctor.sh để kiểm tra tính toàn vẹn."
