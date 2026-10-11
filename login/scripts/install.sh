#!/bin/sh
# Non-interactive live-build/chroot install. Packages, not resource overwrites.
set -eu
expected='48.7-0+deb13u2+majoris1'
if [ "$(id -u)" != 0 ]; then echo 'Run as root inside the target Debian 13 system/chroot.' >&2; exit 1; fi
[ "$#" -ge 3 ] || { echo 'Usage: install.sh RESOURCE.deb SHELL.deb SHELL-COMMON.deb [other matching .deb files]' >&2; exit 2; }
[ "$(. /etc/os-release; printf '%s' "$VERSION_CODENAME")" = trixie ] || { echo 'Debian 13 Trixie required' >&2; exit 1; }
require_version() {
    [ "$2" = "$3" ] || { echo "Unsupported $1 version: $2; expected $3" >&2; exit 1; }
}
found_resources=false
found_shell=false
found_common=false
for file do
    package=$(dpkg-deb -f "$file" Package)
    version=$(dpkg-deb -f "$file" Version)
    case "$package" in
      majoris-login-resources) require_version "$package" "$version" 0.1.0; found_resources=true ;;
      gnome-shell) require_version "$package" "$version" "$expected"; found_shell=true ;;
      gnome-shell-common) require_version "$package" "$version" "$expected"; found_common=true ;;
      gnome-shell-extension-prefs|gnome-shell-dbgsym) require_version "$package" "$version" "$expected" ;;
      *) echo "Unexpected package: $package" >&2; exit 1 ;;
    esac
done
$found_resources && $found_shell && $found_common || { echo 'All three matching packages required' >&2; exit 1; }
# Require recovery packages staged by the ISO build before changing the login.
recovery=/var/lib/majoris-login/stock
[ -f "$recovery/gnome-shell.deb" ] && [ -f "$recovery/gnome-shell-common.deb" ] || { echo 'Stage matching stock Debian packages in /var/lib/majoris-login/stock first (see recovery.md).' >&2; exit 1; }
[ "$(dpkg-deb -f "$recovery/gnome-shell.deb" Version)" = '48.7-0+deb13u2' ]
[ "$(dpkg-deb -f "$recovery/gnome-shell-common.deb" Version)" = '48.7-0+deb13u2' ]
[ "$(dpkg-deb -f "$recovery/gnome-shell.deb" Package)" = gnome-shell ]
[ "$(dpkg-deb -f "$recovery/gnome-shell-common.deb" Package)" = gnome-shell-common ]
mkdir -p /var/lib/majoris-login
if [ ! -e /var/lib/majoris-login/installation-state ]; then
    dpkg-query -W gdm3 gnome-shell gnome-shell-common > /var/lib/majoris-login/installation-state 2>/dev/null || true
fi
apt-get -y install "$@"
dconf update
glib-compile-schemas /usr/share/glib-2.0/schemas
fc-cache -f
for file in /usr/share/majoris-login/theme/login.css /usr/share/majoris-login/assets/wallpapers/dark.png /usr/share/majoris-login/assets/wallpapers/light.png; do
    [ -r "$file" ] || { echo "Missing login resource: $file" >&2; exit 1; }
    [ "$(stat -c %U "$file")" = root ] || { echo "Resource not owned by root: $file" >&2; exit 1; }
done
getent passwd Debian-gdm >/dev/null
runuser -u Debian-gdm -- test -r /usr/share/majoris-login/theme/login.css
echo 'Packages installed. Existing autologin/user configuration preserved. No display-manager restart was performed.'
