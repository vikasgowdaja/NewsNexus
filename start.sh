#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [ -x "$VENV_PYTHON" ]; then
  PYTHON_EXE="$VENV_PYTHON"
else
  PYTHON_EXE="python3"
fi

exec "$PYTHON_EXE" "$ROOT_DIR/run_all.py" "$@"