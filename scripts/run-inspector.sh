#!/usr/bin/env bash
set -euo pipefail
echo 'GTK Inspector enabled. If hidden, use Ctrl+Shift+D (enable org.gtk.Settings.Debug enable-inspector-keybinding if needed).'
GTK_DEBUG=interactive exec "$(dirname "$0")/run-factory.sh" "$@"
