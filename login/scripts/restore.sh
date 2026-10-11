#!/bin/sh
# Run from a text console/recovery system. Does not remove accounts or sessions.
set -eu
[ "$(id -u)" = 0 ] || { echo 'Root is required' >&2; exit 1; }
case "${1:-}" in
  disable)
    mkdir -p /etc/dconf/db/gdm.d /etc/dconf/db/local.d
    for db in gdm local; do
        printf '%s\n' '[org/majoris/login]' 'enabled=false' > "/etc/dconf/db/$db.d/99-majoris-login-recovery"
    done
    dconf update
    echo 'Presentation disabled for profiles using gdm/local. Restart GDM from the console when ready. For other user profiles, use the stock-package restore.'
    ;;
  stock)
    directory=${2:-/var/lib/majoris-login/stock}
    for name in gnome-shell gnome-shell-common; do
        [ -r "$directory/$name.deb" ] || { echo "Missing offline recovery package: $directory/$name.deb" >&2; exit 1; }
        [ "$(dpkg-deb -f "$directory/$name.deb" Package)" = "$name" ]
        case "$(dpkg-deb -f "$directory/$name.deb" Version)" in *+majoris*) echo 'Recovery package must be stock Debian' >&2; exit 1 ;; esac
    done
    # Resolve/check the transaction before mutation, then restore both halves.
    apt-get -s --allow-downgrades install "$directory/gnome-shell.deb" "$directory/gnome-shell-common.deb"
    apt-get -y --allow-downgrades install "$directory/gnome-shell.deb" "$directory/gnome-shell-common.deb"
    apt-get -y purge majoris-login-resources
    dconf update
    echo 'Stock packages restored; no account/session data changed. Restart GDM or reboot from the console.'
    ;;
  *) echo 'Usage: majoris-login-restore disable | stock [OFFLINE_STOCK_DIRECTORY]' >&2; exit 2 ;;
esac
