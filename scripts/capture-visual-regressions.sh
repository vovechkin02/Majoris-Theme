#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/generate-theme.py --check
meson compile -C build
exec dbus-run-session -- xvfb-run -a -s '-screen 0 1440x1080x24' python3 tools/capture-visual.py "$PWD/build/factory/majoris-theme-factory"
