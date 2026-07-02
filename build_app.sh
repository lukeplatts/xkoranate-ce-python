#!/bin/sh
# Build the frozen app: dist/xkoranate.app (macOS) or dist/xkoranate/ (Linux).
set -e
cd "$(dirname "$0")"
.venv/bin/pyinstaller --noconfirm xkoranate.spec
case "$(uname -s)" in
    Darwin) echo "Built: $(pwd)/dist/xkoranate.app" ;;
    *)      echo "Built: $(pwd)/dist/xkoranate/xkoranate" ;;
esac
