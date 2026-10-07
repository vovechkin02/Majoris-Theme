# Implementation report — 7 October 2026

Implementation is built and launched. Full visual acceptance remains open for typography, rendered HTML comparison and real desktop validation; this is not a claim that every visual completion criterion is certified.

## Repository tree

```text
Majoris-Theme/
  README.md LICENSE VERSION meson.build meson_options.txt
  design/ reference/majoris-widget-factory.html tokens.json DESIGN.md gtk-mapping.md templates/
  docs/ reference-analysis.md testing.md gtk3.md gtk4-libadwaita.md gnome-shell.md implementation-report.md
  theme/Majoris/ index.theme gtk-3.0/ gtk-4.0/ gnome-shell/
  icons/Majoris/ index.theme scalable/ui/{minimize,maximize,restore,close} symbolic SVGs
  fonts/ README.md fontconfig/65-majoris-fonts.conf
  factory/ meson.build data/ src/{main,application,window,factory-page,headerbar-tests,geometry-report}.vala
  scripts/ bootstrap-debian.sh install-dev.sh uninstall-dev.sh run-factory.sh run-inspector.sh test.sh wsl.ps1 capture-factory.sh
  tools/ design.py extract-design-tokens.py verify-design-tokens.py generate-theme.py validate-css.py validate-shell.py dev-install.py
  tests/ test-design-tokens.py test-css-selectors.py test-theme-tree.py test-geometry.py test-installer.py test-gtk3-widgets.py expected/headerbars.json
  build/ and artifacts/ are ignored; Linux build lives in ~/src/Majoris-Theme/build
```

## Tested runtime

Debian GNU/Linux 13.5, Trixie; WSL2 kernel 6.6.114.1-microsoft-standard-WSL2 x86_64. GTK3 **3.24.49**, GTK4 **4.18.6**, libadwaita **1.7.6**, Vala **0.56.18**, Meson **1.7.0**, Ninja **1.12.1**. Shell static reference: gnome-shell-common **48.7-0+deb13u2**. Linux commands consistently used `wsl -d debian`, including dependency setup via Debian root. No distribution upgrade was performed.

## Executed verification

* `cat /etc/os-release`, `uname -a`, apt-cache package inspection and requested dependency installation.
* Extracted all three supplied archives and wrote the reference analysis before implementation.
* `python3 tools/extract-design-tokens.py`, `python3 tools/generate-theme.py`.
* `meson setup build`, `meson compile -C build`, `meson test -C build --print-errorlogs`, and Windows `scripts/wsl.ps1 test`.
* `meson configure build --prefix=/usr`, `DESTDIR=/tmp/majoris-stage meson install -C build --no-rebuild` verified themes and icon paths under `/usr/share`.
* `meson setup --wipe build` and subsequent compilation verified clean reconfiguration.
* Development installer, uninstall/restoration, reinstall and isolated conflict/idempotency tests. Current Debian user has the development symlinks installed, with previous files retained in the journal.
* Native WSLg factory launch via run-factory.sh and screenshot capture. Stock gtk4-demo launched successfully; its only diagnostic requested optional syntax-highlighting software. Nautilus/Control Center were not tested.
* Byte-preservation SHA256: `254F7CC14926302526517D9C312740873E4FBE40F2FAB93C6541708777BBD3D5`, identical for supplied and repository HTML. No legacy project naming found. `git diff --check` passed.

Final test suite: **9 passed, 0 failed**. Native GTK parsers pass for light, dark-entrypoint and palette files. Shell static grammar and important installed selectors pass. Installer restoration/conflict protection passes. GTK3 realized button/entry geometry, border and text-color checks pass. Compiler warnings remain for intentionally exercised deprecated GTK APIs and Vala-generated C; no theme parser errors remain.

## Geometry

| Measurement | Simple / Clock | Dense / Files |
|---|---:|---:|
| Headerbar allocation | 420 × 49 | 900 × 49 |
| Minimize plate | 32 × 32 | 32 × 32 |
| Maximize plate | 32 × 32 | 32 × 32 |
| Close plate | 32 × 32 | 32 × 32 |
| Each glyph allocation | 16 × 16 | 16 × 16 |

The visual target is 48px; the border-box allocation includes a 1px separator. Menu and search targets allocate 32×32; the location entry is 32px high. The JSON report recursively locates actual GtkWindowControls, GtkButton and GtkImage nodes, using full allocations rather than content dimensions. The test fails any stretched plate and any simple/dense height mismatch.

## Visual findings and limits

The realized native gallery screenshot was inspected against the HTML's declared visual specification: light surfaces, indigo selection, suggested/destructive buttons, compact controls, 8px cards and exact window glyphs. A native two-column grid and wrapping layout reproduce the gallery structure without app appearance CSS. Toolkit-driven wrapping, menu structure and preference-row spacing differ from HTML; these have not been certified as final matches.

Plus Jakarta Sans was not supplied. `fc-match "Plus Jakarta Sans"` resolves to **Cantarell** after fontconfig installation; exact typography remains unverified. No replacement font is bundled. Dark palette remains pending and dark entrypoints explicitly use the supplied light design.

The available browser tool rejected the local HTML file protocol. No alternate route was used to bypass that restriction. A side-by-side rendered HTML/native comparison therefore remains outstanding. Hover, held-press, focus, inactive, maximized/restore states and lower-gallery menus/dialogs/toasts still require interactive visual acceptance; the factory provides their native controls but automated geometry does not prove every appearance state.

GNOME Shell is statically checked only. Final St property behavior, panel/quick-settings/calendar/notifications/overview, Mutter decorations/shadows, scaling, GDM and whole-desktop integration require the Majoris VM/ISO. WSLg is not a full GNOME session.
