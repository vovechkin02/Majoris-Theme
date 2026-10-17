#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mode="${1:-${MAJORIS_VARIANT:-light}}"; mode="${mode#--}"
case "$mode" in
 light|dark) export MAJORIS_VARIANT="$mode";;
 both) MAJORIS_VARIANT=light "$0" --light; MAJORIS_VARIANT=dark "$0" --dark; exit;;
 *) echo 'Use --light, --dark or --both' >&2; exit 2;;
esac
python3 tools/generate-theme.py --check
meson compile -C build
screen='-screen 0 1440x1080x24'
if [[ "${MAJORIS_CAPTURE_SCALE:-1}" == 2 ]]; then screen='-screen 0 2880x2160x24'; fi
exec dbus-run-session -- xvfb-run -a -s "$screen" python3 tools/capture-visual.py "$PWD/build/factory/majoris-theme-factory"
