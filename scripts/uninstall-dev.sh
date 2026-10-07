#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/../tools/dev-install.py" uninstall
fc-cache -f
