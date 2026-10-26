#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Chạy integration test cho init-global.sh..."

# Đảm bảo thư mục tạm hoạt động ổn định trên mọi môi trường
if [[ -z "${TMPDIR:-}" ]]; then
  if mkdir -p "$HOME/.cache/tmp" 2>/dev/null; then
    export TMPDIR="$HOME/.cache/tmp"
  fi
fi

TEMP_TARGET="$(mktemp -d)"
SANDBOX="$(mktemp -d)"
trap 'rm -rf "$TEMP_TARGET" "$SANDBOX"' EXIT

# Scenario 1: Đã có sẵn file custom AGENTS.md và rules/language.md
mkdir -p "$TEMP_TARGET/rules"
echo "# CUSTOM GLOBAL AGENTS" > "$TEMP_TARGET/AGENTS.md"
echo "# CUSTOM LANGUAGE RULES" > "$TEMP_TARGET/rules/language.md"

# Chạy init-global.sh vào thư mục đích
"$SCRIPT_DIR/init-global.sh" "$TEMP_TARGET"

# Kiểm tra an toàn: không ghi đè file có sẵn khi không có --force
if ! grep -q "CUSTOM GLOBAL AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: AGENTS.md bị ghi đè khi không dùng --force!" >&2
  exit 1
fi
if ! grep -q "CUSTOM LANGUAGE RULES" "$TEMP_TARGET/rules/language.md"; then
  echo "FAIL: rules/language.md bị ghi đè khi không dùng --force!" >&2
  exit 1
fi

# Scenario 2: Kiểm tra cấu trúc phẳng (không bị lồng .agents/.agents)
if [[ -d "$TEMP_TARGET/.agents" ]]; then
  echo "FAIL: init-global tạo thư mục con .agents/ bên trong global target!" >&2
  exit 1
fi

# Kiểm tra các thư mục cốt lõi nằm trực tiếp dưới TARGET
for dir in rules skills scripts template memory; do
  if [[ ! -d "$TEMP_TARGET/$dir" ]]; then
    echo "FAIL: thiếu thư mục $dir trong global target!" >&2
    exit 1
  fi
done

# Scenario 3: rules/project.md không được copy vào global
if [[ -f "$TEMP_TARGET/rules/project.md" ]]; then
  echo "FAIL: rules/project.md (chỉ dành cho per-project) bị copy vào global target!" >&2
  exit 1
fi

# Scenario 4: Không copy artifact rác/pycache
if find "$TEMP_TARGET" -name '*.pyc' -o -name '__pycache__' | grep -q .; then
  echo "FAIL: init-global sao chép cả artifact rác/pycache vào target!" >&2
  exit 1
fi

# Scenario 5: Chạy doctor.sh trên thư mục global vừa khởi tạo
"$TEMP_TARGET/scripts/doctor.sh"

# Scenario 6: Test đường dẫn tương đối trong sandbox
(
  cd "$SANDBOX"
  "$SCRIPT_DIR/init-global.sh" "my_relative_global"
  if [[ ! -f "my_relative_global/AGENTS.md" || ! -d "my_relative_global/rules" ]]; then
    echo "FAIL: init-global thất bại với relative destination path!" >&2
    exit 1
  fi
)

# Scenario 7: Test --force ghi đè file có sẵn
"$SCRIPT_DIR/init-global.sh" --force "$TEMP_TARGET"
if grep -q "CUSTOM GLOBAL AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: --force không ghi đè AGENTS.md!" >&2
  exit 1
fi

echo "test_init_global: ok"
