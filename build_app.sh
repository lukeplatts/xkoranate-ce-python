#!/bin/sh
# Build dist/xkoranate.app
set -e
cd "$(dirname "$0")"
.venv/bin/pyinstaller --noconfirm xkoranate.spec
echo "Built: $(pwd)/dist/xkoranate.app"
