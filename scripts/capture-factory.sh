#!/usr/bin/env bash
# Optional X11/WSLg screenshot utility; requires x11-apps and imagemagick.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p artifacts/screenshots
meson compile -C build
GDK_BACKEND=x11 GTK_A11Y=none ./build/factory/majoris-theme-factory >artifacts/factory-launch.log 2>&1 &
factory_pid=$!
trap 'kill "$factory_pid" 2>/dev/null || true' EXIT
sleep 3
window_id=$(xwininfo -root -tree | awk '/"Majoris Widget Factory"/ {print $1; exit}')
[[ -n "$window_id" ]] || { cat artifacts/factory-launch.log; echo 'No realized WSLg window' >&2; exit 1; }
xwd -silent -id "$window_id" -out artifacts/screenshots/factory.xwd
magick artifacts/screenshots/factory.xwd artifacts/screenshots/factory.png
echo 'Saved artifacts/screenshots/factory.png'
