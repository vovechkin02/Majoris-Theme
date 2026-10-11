#!/bin/bash
# Root is used only for private mount namespaces; Shell runs as the caller.
# No GDM is started, no PAM conversation is attempted, no production files copied.
set -eu
module=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ "${1:-}" != --isolated ]; then
    [ "$#" -ge 3 ] && [ "$#" -le 4 ] || { echo 'Usage: sudo verify-native.sh SHELL_SOURCE BUILD_USER OUTPUT [WIDTHxHEIGHT]' >&2; exit 2; }
    [ "$(id -u)" = 0 ] || { echo 'Root needed for the private mount namespace only' >&2; exit 1; }
    exec unshare --mount --propagation private bash "$0" --isolated "$@"
fi
shift
source=$(realpath "$1")
user=$2
output=$(realpath -m "$3")
resolution=${4:-1280x720}
build="$source/obj-x86_64-linux-gnu"
temporary=$(mktemp -d)
trap 'rm -rf -- "$temporary"' EXIT
mkdir "$temporary/x11" "$temporary/schemas"
chmod 1777 "$temporary/x11"
chmod 755 "$temporary"
mount --bind "$temporary/x11" /tmp/.X11-unix
mkdir -p /usr/share/majoris-login
mount --bind "$module" /usr/share/majoris-login
cp "$build"/data/*.xml "$temporary/schemas/"
cp "$module/config/org.majoris.login.gschema.xml" "$temporary/schemas/"
glib-compile-schemas "$temporary/schemas"
printf '%s\n' '<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><include>/etc/fonts/fonts.conf</include><dir>/usr/share/majoris-login/assets/fonts/static</dir></fontconfig>' > "$temporary/fonts.conf"
install -d -o "$user" -g "$user" "$output"
runuser -u "$user" -- env \
    DBUS_SYSTEM_BUS_ADDRESS=unix:path=/tmp/majoris-no-host-bus \
    GSETTINGS_SCHEMA_DIR="$temporary/schemas" \
    GSETTINGS_BACKEND=memory \
    FONTCONFIG_FILE="$temporary/fonts.conf" \
    GNOME_SHELL_SESSION_MODE=user \
    GNOME_SHELL_DATADIR="$build/data" \
    GNOME_SHELL_BUILDDIR="$build/src" \
    GI_TYPELIB_PATH="$build/subprojects/gvc:$build/src:$build/src/st" \
    LD_LIBRARY_PATH="$build/subprojects/gvc:$build/src:$build/src/st" \
    GDM_GREETER_TEST=1 \
    MAJORIS_LOGIN_CAPTURE_DIR="$output" \
    MAJORIS_LOGIN_SIZE="$resolution" \
    timeout 120 "$build/tests/gnome-shell-dbus-runner.py" -- \
    "$build/src/gnome-shell-test-tool" --headless --hotplug "$module/tests/native-actors.js"
