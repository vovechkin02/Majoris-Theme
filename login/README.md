# Majoris Login

Native GNOME Shell 48.7 GDM and lock presentation, translated from the supplied
login prototype. GDM/PAM remains the authentication service. No web renderer,
extension injection, privileged helper or new daemon is used.

This module has two independent build products: `majoris-login-resources`
(theme, wallpapers, fonts, icons, schema and greeter defaults), and separately
rebuilt Debian GNOME Shell packages containing focused presentation hooks.
Ordinary Majoris GTK/Shell application theme updates do not rebuild that binary.

Target: Debian 13 Trixie amd64, exact source **48.7-0+deb13u2**, Mutter ABI 16.
`patches/compatibility.json` pins source archive and modified-module SHA-256s.
Other versions fail before patching. The downstream version is
`48.7-0+deb13u2+majoris1`. Security updates are not held or disabled: a stock
update safely removes the custom layout until its patches are revalidated.

Build and tests: [integration](docs/integration.md). Design, native service
ownership and deviations: [architecture](docs/architecture.md). Console/offline
rollback: [recovery](docs/recovery.md). Real session release acceptance:
[VM matrix](docs/vm-validation.md).

Native actor screenshots validate St layout and CSS, not authentication.
Do not describe a headless fixture as a successful GDM login or secure unlock.
The VM matrix must be completed before enabling this as a shipping default.

Actual build/test results and outstanding acceptance: [implementation report](docs/implementation-report.md).
