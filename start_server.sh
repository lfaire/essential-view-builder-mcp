#!/bin/bash
# Wrapper to start the Essential View Builder MCP server.
# Forces Homebrew Python 3.11 (where `mcp` is installed on your machine).

set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
PY="/usr/local/bin/python3.11"

if [[ ! -x "$PY" ]]; then
  echo "ERROR: Expected Python not found/executable: $PY" >&2
  echo "Install Homebrew python@3.11 (or update this script to your python path)." >&2
  exit 1
fi

echo "Using Python: $PY" >&2
exec "$PY" "$BASE_DIR/server.py"
