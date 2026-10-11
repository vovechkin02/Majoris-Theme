# Build, install and ISO integration

Run on Debian 13 amd64. Install the matching source build dependencies with
`apt-get build-dep gnome-shell` (enable Trixie deb-src), plus quilt and
python3-tinycss2. No testing/unstable repository is needed.

```sh
# From Majoris-Theme; source archives come from the URL in compatibility.json.
python3 login/scripts/generate-theme.py --check
python3 login/tests/test-contracts.py
sh login/scripts/build.sh resources --output "$PWD/artifacts/login-packages"
dpkg-source -x gnome-shell_48.7-0+deb13u2.dsc /build/gnome-shell-48.7
python3 login/scripts/prepare-shell.py /build/gnome-shell-48.7 --check
sh login/scripts/build.sh shell /build/gnome-shell-48.7
```

Verify Debian archive signatures with the Debian archive keyring in the build
infrastructure and compare all three downloaded file SHA-256s with the manifest.
The helper checks the precise Debian changelog version and all affected module
hashes before mutation. Re-extract a clean tree after a failed preparation;
reapplying to an already prepared or modified tree is deliberately rejected.
Do not use `nocheck` to claim validation. WSLg has a read-only X11 socket mount;
native compositor tests may need a private mount namespace containing a fresh
1777 X11 directory and an isolated mock system bus rather than WSL's logind.

The resource package is `Architecture: all`; Shell binaries are built normally
for amd64. Preserve upstream Debian packaging and publish the matching
gnome-shell/gnome-shell-common pair together. No patched executable is committed
to this theme repository. Keep its `.dsc`, quilt patches, orig archive, Debian
archive, buildinfo and changes in the Majoris package build/release system.

Before installation, stage offline stock recovery packages in the target image:

```sh
mkdir -p /var/lib/majoris-login/stock
# Obtain these signed packages via apt from the same Trixie archive version.
cp gnome-shell_48.7-0+deb13u2_amd64.deb /var/lib/majoris-login/stock/gnome-shell.deb
cp gnome-shell-common_48.7-0+deb13u2_all.deb /var/lib/majoris-login/stock/gnome-shell-common.deb
chmod 0644 /var/lib/majoris-login/stock/*.deb
```

Place all three custom packages in the live-build package source/local package
stage. From the image's chroot, with its normal policy-rc.d preventing services
from starting, invoke the noninteractive helper with **absolute package paths**:

```sh
sh login/scripts/install.sh \
  /packages/majoris-login-resources_0.1.0_all.deb \
  /packages/gnome-shell_48.7-0+deb13u2+majoris1_amd64.deb \
  /packages/gnome-shell-common_48.7-0+deb13u2+majoris1_all.deb
```

The helper verifies target/version/package identities and recovery pair before
apt mutates packages, then checks resource ownership/readability as Debian-gdm.
It never edits gdm3/daemon.conf, users, autologin, session defaults, or ordinary
user theme preferences, and never restarts GDM. Maintainer scripts update schemas,
dconf and font caches. Debhelper manages standard font/icon cache triggers.
Existing GDM dconf profiles are preserved; ensure yours includes `system-db:gdm`
for the greeter defaults to apply. The package creates a standard profile only
if absent and removes only that unchanged, package-created profile on removal.

Set a greeter appearance with an administrator file such as
`/etc/dconf/db/gdm.d/30-majoris-appearance`:

```ini
[org/majoris/login]
appearance='light'
logo='/usr/share/majoris/branding/approved-logo.svg'
```

Run `dconf update`. Do not set the logo path unless the asset exists and is
readable by Debian-gdm. For a lock-screen default, use the corresponding system
database included in user profiles; individual users can set
`gsettings set org.majoris.login appearance light`. No private file is needed.
Stop/restart GDM only from a console after saving sessions when activating or
recovering a deployed image. Never disable Debian security updates or hold Shell
packages; revalidate/rebuild for each new source version, or use stock fallback.

Re-render wallpapers only when the reference changes:
`python3 login/scripts/generate-wallpaper.py` (Pillow and NumPy required).
Font sources are the supplied Plus_Jakarta_Sans.zip, with SIL OFL retained.
