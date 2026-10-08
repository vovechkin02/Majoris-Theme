#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mode="${1:-${MAJORIS_VARIANT:-light}}"; mode="${mode#--}"
case "$mode" in
 light|dark) export MAJORIS_VARIANT="$mode";;
 both) "$0" --light; "$0" --dark; exit;;
 *) echo 'Use --light, --dark or --both' >&2; exit 2;;
esac
command -v chromium >/dev/null || { echo 'Install the Debian chromium package for deterministic reference rendering.' >&2; exit 1; }
exec dbus-run-session -- python3 tools/render-html-reference.py
