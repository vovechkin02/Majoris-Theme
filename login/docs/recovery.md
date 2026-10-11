# Console and offline recovery

Before ISO acceptance, keep the exact stock Debian Shell/common pair under
`/var/lib/majoris-login/stock`. The installer refuses to proceed without them.
Keep a VM snapshot and the Majoris resource package alongside the build output.
No account or PAM configuration is changed by this component.

If GDM fails, switch to a text console (Ctrl+Alt+F3) or boot recovery media and
enter the target root/chroot. Save running sessions before restarting GDM.

```sh
# Fast presentation-only fallback (requires patched Shell to execute).
sudo majoris-login-restore disable
sudo systemctl restart gdm3

# Definitive fallback, including a Shell/resource initialization failure.
sudo majoris-login-restore stock
sudo systemctl restart gdm3
```

`stock` first simulates the apt transaction, then restores both matching Debian
packages with explicit downgrade permission and removes the resource package.
It does not touch users, home directories, PAM, session data or autologin.
For nonstandard user dconf profiles, the stock-package route is definitive.
No automatic "success" watchdog bypasses authentication or unlocks the session.

If the helper is unavailable, use the stock packages directly:

```sh
sudo apt-get --allow-downgrades install \
  /var/lib/majoris-login/stock/gnome-shell.deb \
  /var/lib/majoris-login/stock/gnome-shell-common.deb
sudo apt-get purge majoris-login-resources
sudo dconf update
sudo systemctl restart gdm3
```

Before deployment, execute both recovery paths in a disposable VM and verify
stock GDM login, a user session, lock/unlock and reboot. Package extraction and
shell syntax tests alone do not establish recovery acceptance. The helper does
not restart services by itself, so live-build can run it noninteractively.
