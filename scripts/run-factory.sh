#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ -f build/build.ninja ]] || meson setup build
meson compile -C build
export MAJORIS_THEME_ROOT="$PWD/theme/Majoris"
if ! dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply / org.freedesktop.DBus.ListNames >/dev/null 2>&1; then
  exec dbus-run-session -- ./build/factory/majoris-theme-factory "$@"
fi
exec ./build/factory/majoris-theme-factory "$@"
