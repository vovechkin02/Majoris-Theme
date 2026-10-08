#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/../tools/dev-install.py" install "$@"
fc-cache -f
echo 'Use GTK_THEME=Majoris for GTK3. The factory selects the Majoris icon overlay and right-side controls.'
fc-match 'Plus Jakarta Sans'
if [[ $(fc-match -f '%{family}' 'Plus Jakarta Sans') != *'Plus Jakarta Sans'* ]]; then
  echo 'Plus Jakarta Sans is unavailable: typography match remains unverified.' >&2
fi
