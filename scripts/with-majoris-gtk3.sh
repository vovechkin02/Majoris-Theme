#!/usr/bin/env bash
# GTK3 named-theme selection; auto follows GNOME settings without modifying them.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
bridge="libmajoris-gtk3-theme.so"
[[ ! -f "$root/build/libmajoris-gtk3-theme.so" ]] || bridge="$root/build/libmajoris-gtk3-theme.so"
mode="${1:---auto}"
case "$mode" in
 --light) export GTK_THEME=Majoris; shift;;
 --dark) export GTK_THEME=Majoris:dark; shift;;
 --auto) unset GTK_THEME; export LD_PRELOAD="$bridge${LD_PRELOAD:+:$LD_PRELOAD}"; shift;;
 *) echo 'Usage: with-majoris-gtk3.sh --light|--dark|--auto PROGRAM [ARGS...]' >&2; exit 2;;
esac
exec "$@"
