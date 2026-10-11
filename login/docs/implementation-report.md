# Implementation and validation report

Implemented 12 October 2026 for Debian 13 Trixie amd64, GNOME Shell source
48.7-0+deb13u2 and Mutter ABI 16. This is implemented source and built evaluation
packages. Real GDM/PAM and secure-lock release acceptance remains outstanding;
this report does not certify an OS image for shipping.

## Delivered implementation

Native LoginDialog/AuthPrompt and UnlockDialog/ScreenShield presentation follows
the supplied prototype: dark/light palettes, atmospheric system wallpapers,
Plus Jakarta Sans, initials/native account photos, glass cards, account chooser,
Other User, credential prompts, reserved error space, native session selection,
header clock/date, lock clock, fade transitions and bottom controls.

GDM/PAM conversations, AccountsService filtering, installed-session discovery,
NetworkManager Quick Settings, native input sources/accessibility, SystemActions
and modal lock protection remain owned by GNOME. No browser, extension, new
privileged daemon, alternate authenticator or production fake account is added.
See architecture.md for each hook and deliberate visual deviations, including
the wordmark fallback and native Quick Settings network menu.

## Files and patched components

All new implementation is under `login/`:

- `shell/majorisLogin.js`: shared native presentation and lifecycle helpers.
- `patches/gnome-shell-48.7/0001-majoris-login-presentation.patch` and
  `patches/compatibility.json`: exact-source hooks, source archives/module hashes.
  `prepare-shell.py` generates the second quilt patch embedding the helper.
- `theme/`, `assets/`, `resources.gresource.xml`, `config/`: generated scoped St
  CSS, semantic tokens, both 4K wallpapers, symbolic SVGs, four font weights and
  licence, settings schema and GDM defaults/profile example.
- `meson.build`, `packaging/debian/`: independent resource Debian package.
- `scripts/`: generators, pinned source fetcher, resource/Shell build, strict
  preparation, installation, offline restoration and native-render verification.
- `tests/`: source/resource contracts, real Shell actor screenshot/assertion
  fixture and read-only VM preflight recorder.
- `docs/`, `README.md`, `COPYRIGHT`: architecture, integration, recovery and VM
  acceptance instructions.

The root README gains a module link; root meson.build adds its contract test.
Existing application theme, icons and desktop styles are unchanged.

Patched Shell modules: gdm/authPrompt.js, gdm/loginDialog.js,
ui/unlockDialog.js, ui/screenShield.js, ui/layout.js, ui/boxpointer.js,
ui/userWidget.js, ui/status/accessibility.js, ui/status/keyboard.js,
ui/sessionMode.js and js-resources.gresource.xml; gdm/majorisLogin.js is added.
The upstream authentication/service implementation modules are unchanged.

Built packages are `majoris-login-resources_0.1.0_all.deb`,
`gnome-shell_48.7-0+deb13u2+majoris1_amd64.deb` and matching
`gnome-shell-common_48.7-0+deb13u2+majoris1_all.deb` in
`artifacts/login-packages/`. Optional extension-prefs/debug packages are also
produced by Debian packaging. These artifacts are ignored build outputs, not
committed theme binaries. The resource and Shell builds remain independent.

## Build, installation and recovery

Follow integration.md for dependencies, authenticated source acquisition,
exact-version preparation, normal dpkg builds and live-build integration.
From Debian 13, run:

```sh
python3 login/tests/test-contracts.py
python3 login/scripts/build-resources.py --output "$PWD/artifacts/login-packages"
python3 login/scripts/prepare-shell.py /build/gnome-shell-48.7 --check
sh login/scripts/build.sh shell /build/gnome-shell-48.7
```

Stage the matching original Debian Shell/common packages in
`/var/lib/majoris-login/stock` before invoking install.sh with the three absolute
custom package paths. The helper validates identity/version/recovery availability
before apt installation. It does not restart GDM or alter account/autologin data.

From a saved-session text console, `majoris-login-restore disable` disables the
presentation for profiles using the documented databases. The stronger
`majoris-login-restore stock` reinstalls the offline stock pair and purges the
resource package. Follow recovery.md before restarting GDM or rebooting.
Recovery is explicitly documented but has not been executed on a real GDM VM.

## Actual tests and evidence

- Root `meson test -C build --print-errorlogs`: **38/38 passed**; includes the
  six Majoris Login contracts. Log: artifacts/login-theme-tests-final.log.
- `python3 login/tests/test-contracts.py`: **6/6 passed**. Both palettes,
  generated resources, licences, native ownership, strict schema and incompatible
  version rejection before mutation checked.
- Final independent resource dpkg build: successful, including its six contract
  checks. Log: artifacts/login-resources-build-final.log.
- Final patched Shell native compilation and Debian binary packaging: successful.
  Log: artifacts/login-shell-packaging.log.
- Fresh source extraction/preparation: **all 12 affected compiled modules match
  byte-for-byte**. Log: artifacts/login-patch-roundtrip.log. Extraction used
  --no-check only for this local repeatability test; archive hashes were pinned.
- Final full upstream Shell suite: **19/20 passed**, one failure in
  closeWithActiveWindows (GLib hash-table iterator assertion during shutdown).
  Log: artifacts/login-shell-tests-final.log. The same failure was reproduced
  with unmodified matching Debian source: artifacts/login-stock-baseline-test.log.
  The evaluation binary packages were therefore built with DEB_BUILD_OPTIONS=nocheck
  after recording the actual suite result. Normal committed build instructions
  retain tests; these packages do not constitute a fully passing release build.
- Native real Shell/St fixture captures both palettes and twelve states per
  resolution: 1280x720, 1920x1080, 2560x1440 and 3840x2160. Evidence is under
  artifacts/login-native-final/<resolution>/, including geometry.json. Card
  width is 432 logical pixels, height 486, and error insertion does not move the
  field. Submission sensitivity, password masking reset and fade-only geometry
  assertions pass. Screenshot contents are upstream mock AccountsService test
  data with empty fields, never real credentials.
- Shell scripts pass bash/sh syntax checks. Generated CSS passes --check and the
  GSettings schema passes strict compilation.

Native fixtures use private mount namespaces and mock system buses, not active
GDM. Expected environment warnings include absent IBus/GVfs/background services;
the upstream fixture also lacks realmd and LoginManager.GetSession(dummy), which
logs mock-service errors. These are not evidence of working real services.
The fixture renders login actors while in unlock mode; native locked-mode policy
can leave the power menu empty. Actual greeter capabilities/actions and installed
input-source labels require the VM checks; screenshot names do not prove them.

## Unverified release criteria and limits

No real GDM service was activated. Actual password login, session launch,
fingerprint/smartcard/domain authentication, lock grabs and secure unlock,
logind power/suspend actions, policy/inhibitors, package installation/removal,
offline recovery and ISO boot remain **unverified**. The executable checklist in
vm-validation.md covers those and autologin/hidden users, account filtering,
session selection, accessibility/OSK/screen reader, translations/RTL, fractional
scaling, multiple monitors, suspend/resume, notifications/privacy and stock
security-update fallback. Complete it in a disposable target VM before shipping.

Compatibility is deliberately exact: other Debian/Shell versions are rejected
before patching. Revalidate and rebuild after upstream/security updates; do not
hold security packages. Missing resources/schema uses stock presentation. There
is no approved logo in the repository, so the supplied placeholder is replaced
with a wordmark until a readable administrator-approved system SVG is configured.