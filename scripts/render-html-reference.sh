#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v chromium >/dev/null || { echo 'Install the Debian chromium package for deterministic reference rendering.' >&2; exit 1; }
exec dbus-run-session -- python3 tools/render-html-reference.py
