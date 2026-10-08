#!/usr/bin/env bash
# Launch a GTK4/libadwaita application with native live theme integration.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
bridge="libmajoris-gtk4-theme.so"
if [[ -f "$root/build/libmajoris-gtk4-theme.so" ]]; then
 export MAJORIS_THEME_ROOT="$root/theme/Majoris"
 bridge="$root/build/libmajoris-gtk4-theme.so"
fi
export LD_PRELOAD="$bridge${LD_PRELOAD:+:$LD_PRELOAD}"
exec "$@"
