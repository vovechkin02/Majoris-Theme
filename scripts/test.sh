#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -f build/build.ninja ]] || meson setup build
meson compile -C build
meson test -C build --print-errorlogs
