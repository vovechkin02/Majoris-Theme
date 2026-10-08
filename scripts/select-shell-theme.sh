#!/usr/bin/env bash
# GNOME session helper; requires an enabled User Themes extension.
set -euo pipefail
schema=org.gnome.shell.extensions.user-theme
if ! gsettings list-schemas | grep -Fxq "$schema"; then
 echo 'User Themes schema is unavailable; run this in the configured Majoris GNOME session.' >&2; exit 1
fi
select_theme() {
 if [[ "$(gsettings get org.gnome.desktop.interface color-scheme)" == "'prefer-dark'" ]]; then
  gsettings set "$schema" name Majoris-Dark
 else gsettings set "$schema" name Majoris
 fi
}
case "${1:---auto}" in
 --light) gsettings set "$schema" name Majoris;;
 --dark) gsettings set "$schema" name Majoris-Dark;;
 --auto)
  previous="$(gsettings get "$schema" name)"
  trap 'gsettings set "$schema" name "$previous"' EXIT
  trap 'exit' INT TERM
  select_theme
  while IFS= read -r change; do select_theme; done < <(gsettings monitor org.gnome.desktop.interface color-scheme)
  ;;
 *) echo 'Use --light, --dark or --auto' >&2; exit 2;;
esac
