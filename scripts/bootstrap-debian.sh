#!/usr/bin/env bash
set -euo pipefail
. /etc/os-release
[[ "$ID" == debian && "$VERSION_CODENAME" == trixie ]] || { echo 'Debian Trixie required; refusing distro changes.' >&2; exit 1; }
packages=(valac meson ninja-build pkg-config build-essential libgtk-3-dev libgtk-4-dev libadwaita-1-dev python3-gi python3-tinycss2 gir1.2-gtk-3.0 gir1.2-gtk-4.0 gir1.2-adw-1 dbus-x11 xvfb unzip 7zip fontconfig x11-apps x11-utils imagemagick gnome-shell-common)
for package in "${packages[@]}"; do apt-cache show "$package" >/dev/null; done
sudo apt-get update
sudo apt-get install -y "${packages[@]}"
