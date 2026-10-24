#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Chạy integration test cho init-project.sh..."

TEMP_TARGET="$(mktemp -d)"
SANDBOX="$(mktemp -d)"
trap 'rm -rf "$TEMP_TARGET" "$SANDBOX"' EXIT

# Scenario 1: Pre-existing custom project.md and custom AGENTS.md
mkdir -p "$TEMP_TARGET/.agents/rules"
echo "# CUSTOM PROJECT RULES DO NOT OVERWRITE" > "$TEMP_TARGET/.agents/rules/project.md"
echo "# CUSTOM ROOT AGENTS" > "$TEMP_TARGET/AGENTS.md"

# Run init-project.sh
"$SCRIPT_DIR/init-project.sh" "$TEMP_TARGET"

# Assert pre-existing files preserved
if ! grep -q "CUSTOM PROJECT RULES DO NOT OVERWRITE" "$TEMP_TARGET/.agents/rules/project.md"; then
  echo "FAIL: .agents/rules/project.md bị ghi đè!" >&2
  exit 1
fi
if ! grep -q "CUSTOM ROOT AGENTS" "$TEMP_TARGET/AGENTS.md"; then
  echo "FAIL: root AGENTS.md bị ghi đè!" >&2
  exit 1
fi

# Assert .agents/AGENTS.md copied
if [[ ! -f "$TEMP_TARGET/.agents/AGENTS.md" ]]; then
  echo "FAIL: thiếu .agents/AGENTS.md!" >&2
  exit 1
fi

# Assert NO generated cache artifacts copied into target
if find "$TEMP_TARGET" -name '*.pyc' -o -name '__pycache__' | grep -q .; then
  echo "FAIL: init-project sao chép cả artifact rác/pycache vào target!" >&2
  exit 1
fi
(
  cd "$TEMP_TARGET"
  git init -q
  "$TEMP_TARGET/.agents/scripts/doctor.sh"
)

# Scenario 2: Test relative destination directory handling inside an isolated temp sandbox
(
  cd "$SANDBOX"
  "$SCRIPT_DIR/init-project.sh" "my_relative_app"
  if [[ ! -f "my_relative_app/AGENTS.md" || ! -f "my_relative_app/.agents/AGENTS.md" ]]; then
    echo "FAIL: init-project thất bại với relative destination path!" >&2
    exit 1
  fi
)

# Scenario 3: Test --force overwrite
"$SCRIPT_DIR/init-project.sh" --force "$TEMP_TARGET"
if grep -q "CUSTOM PROJECT RULES DO NOT OVERWRITE" "$TEMP_TARGET/.agents/rules/project.md"; then
  echo "FAIL: --force không ghi đè .agents/rules/project.md!" >&2
  exit 1
fi

echo "test_init_project: ok"
