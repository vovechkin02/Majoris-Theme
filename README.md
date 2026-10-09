# Majoris Theme

The authoritative light and dark GTK3, GTK4/libadwaita and GNOME Shell theme for Majoris, with a native Vala Widget Factory and headerbar regression fixtures. The [HTML factory](design/reference/majoris-widget-factory.html) is the visual authority. Material, Unity8 and Sunrise are implementation references only; see [reference analysis](docs/reference-analysis.md).

Development uses the existing **Debian 13 Trixie WSL distribution named `debian`**. The Windows helper synchronizes source into `~/src/Majoris-Theme` and builds inside Linux. It excludes Windows Git metadata and generated artifacts. Edit this Windows repository, then synchronize via the helper; do not edit both copies independently.

```powershell
wsl -d debian -- bash -lc 'cat /etc/os-release; uname -a'
.\scripts\wsl.ps1 bootstrap
.\scripts\wsl.ps1 build
.\scripts\wsl.ps1 test
.\scripts\wsl.ps1 install
.\scripts\wsl.ps1 factory
.\scripts\wsl.ps1 inspector
```

Bootstrap checks Trixie and apt-cache package availability, requires sudo for dependencies and refuses distro upgrades. In Debian, from the Linux source directory:

```bash
meson setup build --prefix=/usr
meson compile -C build
meson test -C build --print-errorlogs
./scripts/install-dev.sh
./scripts/run-factory.sh
./scripts/run-inspector.sh
./build/factory/majoris-theme-factory --geometry-report
```

GTK3 uses user-local theme selection (`GTK_THEME=Majoris`). GTK4/libadwaita uses user CSS plus the reusable StyleManager bridge for live and system switching. The minimal icon overlay inherits Adwaita and hicolor. The factory selects it and right-side window controls in its process. See [GTK3](docs/gtk3.md), [GTK4](docs/gtk4-libadwaita.md), [mapping](design/gtk-mapping.md) and [testing](docs/testing.md).

Plus Jakarta Sans is required. The supplied variable normal/italic fonts were installed and verified in Debian WSL; generic sans-serif and system-ui also resolve to Plus Jakarta Sans. Fonts remain external assets; see [fonts](fonts/README.md). The [dark HTML](design/reference/majoris-widget-factory-dark.html) is preserved verbatim, and its effective override cascade generates `design/tokens-dark.json`. See [dark implementation and switching](docs/dark-theme.md).

Development installation requires no root. Previous files are journaled and backed up; later edits are protected. Restore with `./scripts/uninstall-dev.sh` or `.\scripts\wsl.ps1 uninstall`. The installer changes files, not global gsettings preferences. Desktop integration selects the GTK3 theme and icon overlay.

`meson setup --wipe build` reconfigures. `DESTDIR=/tmp/majoris-stage meson install -C build` stages theme, icons, fontconfig, factory and metadata. Use prefix `/usr` for `/usr/share/themes/Majoris` and `/usr/share/icons/Majoris`. Future Debian packaging and the Majoris ISO consume these outputs independently of the ISO builder. Production libadwaita overrides and fontconfig activation belong to distribution/session integration.

Shell receives static grammar and Trixie selector checks; final Shell/Mutter/desktop validation requires a [Majoris VM](docs/gnome-shell.md). See [implementation results](docs/implementation-report.md) for measured results and outstanding visual checks.
`scripts/render-html-reference.sh` and `scripts/capture-visual-regressions.sh` produce uncropped reference/native artifacts. `tools/report-visual-conformance.py` generates the component comparison report from reviewed observations. See [testing workflow](docs/testing.md) and [fresh audit](docs/visual-conformance-audit.md).


Light, dark and system appearance use the same native geometry. Applications should use `Adw.StyleManager` with `DEFAULT`, and let the shared theme integration supply their colours. Avoid hardcoded dark backgrounds, text or titlebars.

```bash
./scripts/install-dev.sh --variant=auto
./scripts/run-factory.sh --light
./scripts/run-factory.sh --dark
./scripts/run-factory.sh --system
./scripts/with-majoris-gtk4.sh nautilus
./scripts/with-majoris-gtk3.sh --dark gtk3-demo
./scripts/with-majoris-gtk3.sh --auto gtk3-demo
./scripts/render-html-reference.sh --both
./scripts/capture-visual-regressions.sh --both
```

The factory menu has Appearance → Light / Dark / System. GTK3 can also use `GTK_THEME=Majoris:dark`. The development installer supports `--variant=light|dark|auto`, preserves prior files and installs both palettes/assets simultaneously. A fixed dark install selects dark user CSS; automatic GTK4 behaviour requires the bridge (factory links it, other GTK4 apps use the wrapper). A fixed GTK_THEME setting prevents automatic GTK3 selection; the auto wrapper clears it and follows GNOME settings through native GtkSettings.

Windows helpers stay in Debian: `scripts/wsl.ps1 factory -Variant dark`, `factory -Variant auto`, `capture -Variant auto` and `reference -Variant auto`. Capture/reference auto means both explicit suites; results are in the synchronized Linux checkout. Native captures use `artifacts/screenshots/light/` and `dark/`; HTML uses `html/` and `html-dark/`.

Both variants require the [GNOME VM checklist](docs/testing.md), including Light → Dark → Light without stale colours, Settings, inactive/maximized/restored/tiled windows, Mutter corners/shadows, scaling and the full Shell. WSL source/parser tests and Xvfb captures do not establish those GNOME session results.

The [surgical conformance audit](docs/surgical-conformance.md) records the invariant palette, semantic dark actions, mixed-checkbox and CSD edge fixes, native regression evidence and remaining GNOME VM acceptance.
