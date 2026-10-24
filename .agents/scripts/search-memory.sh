#!/usr/bin/env bash
set -euo pipefail

# Wrapper preserving backward compatibility with search-memory.sh
# and delegating directly to python3 search-memory.py
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/search-memory.py" "$@"
