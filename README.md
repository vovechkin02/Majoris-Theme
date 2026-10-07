# Majoris Theme

The authoritative light GTK3, GTK4/libadwaita and GNOME Shell theme for Majoris, with a native Vala Widget Factory and headerbar regression fixtures. The [HTML factory](design/reference/majoris-widget-factory.html) is the visual authority. Material, Unity8 and Sunrise are implementation references only; see [reference analysis](docs/reference-analysis.md).

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

GTK3 uses user-local theme selection (`GTK_THEME=Majoris`). GTK4/libadwaita uses normal user CSS overrides, including the palette import. The minimal icon overlay inherits Adwaita and hicolor. The factory selects it and right-side window controls in its process. See [GTK3](docs/gtk3.md), [GTK4](docs/gtk4-libadwaita.md), [mapping](design/gtk-mapping.md) and [testing](docs/testing.md).

Plus Jakarta Sans is required but not supplied/installed; fc-match currently returns Cantarell. See [fonts](fonts/README.md). Dark entrypoints remain valid and use the light palette while a dark specification is pending.

Development installation requires no root. Previous files are journaled and backed up; later edits are protected. Restore with `./scripts/uninstall-dev.sh` or `.\scripts\wsl.ps1 uninstall`. The installer changes files, not global gsettings preferences. Desktop integration selects the GTK3 theme and icon overlay.

`meson setup --wipe build` reconfigures. `DESTDIR=/tmp/majoris-stage meson install -C build` stages theme, icons, fontconfig, factory and metadata. Use prefix `/usr` for `/usr/share/themes/Majoris` and `/usr/share/icons/Majoris`. Future Debian packaging and the Majoris ISO consume these outputs independently of the ISO builder. Production libadwaita overrides and fontconfig activation belong to distribution/session integration.

Shell receives static grammar and Trixie selector checks; final Shell/Mutter/desktop validation requires a [Majoris VM](docs/gnome-shell.md). See [implementation results](docs/implementation-report.md) for measured results and outstanding visual checks.
`scripts/render-html-reference.sh` and `scripts/capture-visual-regressions.sh` produce uncropped reference/native artifacts. `tools/report-visual-conformance.py` generates the component comparison report from reviewed observations. See [testing workflow](docs/testing.md) and [fresh audit](docs/visual-conformance-audit.md).
