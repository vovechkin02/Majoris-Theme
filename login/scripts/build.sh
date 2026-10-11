#!/bin/sh
# Build only; never install or restart the caller's display manager.
set -eu
module=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
case "${1:-}" in
  resources)
    shift
    exec python3 "$module/scripts/build-resources.py" "$@"
    ;;
  shell)
    [ "$#" = 2 ] || { echo 'Usage: build.sh shell /path/to/extracted/gnome-shell-48.7' >&2; exit 2; }
    python3 "$module/scripts/prepare-shell.py" "$2"
    cd "$2"
    exec dpkg-buildpackage -us -uc -b
    ;;
  *) echo 'Usage: build.sh resources | shell SOURCE' >&2; exit 2 ;;
esac
