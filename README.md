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

GTK3 uses user-local theme selection (`GTK_THEME=Majoris`). GTK4/libadwaita uses fixed user CSS in explicit modes and the reusable StyleManager bridge for live/system switching. Auto installation uses neutral CSS and requires the factory or wrapper bridge. The minimal icon overlay inherits Adwaita and hicolor. The factory selects it and right-side window controls in its process. See [GTK3](docs/gtk3.md), [GTK4](docs/gtk4-libadwaita.md), [mapping](design/gtk-mapping.md) and [testing](docs/testing.md).

Plus Jakarta Sans is required. The supplied variable normal/italic fonts were installed and verified in Debian WSL; generic sans-serif and system-ui also resolve to Plus Jakarta Sans. Fonts remain external assets; see [fonts](fonts/README.md). The [dark HTML](design/reference/majoris-widget-factory-dark.html) is a canonical design source, and its effective override cascade generates `design/tokens-dark.json`. See [dark implementation and switching](docs/dark-theme.md).

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

The factory menu has Appearance → Light / Dark / System. GTK3 can also use `GTK_THEME=Majoris:dark`. The development installer supports `--variant=light|dark|auto`, preserves prior files and installs both palettes/assets simultaneously. Light/dark installs select fixed user CSS; auto installs a neutral comment-only entrypoint that imports neither variant; automatic GTK4 behaviour requires the bridge (factory links it, other GTK4 apps use the wrapper). A fixed GTK_THEME setting prevents automatic GTK3 selection; the auto wrapper clears it and follows GNOME settings through native GtkSettings.

Windows helpers stay in Debian: `scripts/wsl.ps1 factory -Variant dark`, `factory -Variant auto`, `capture -Variant auto` and `reference -Variant auto`. Capture/reference auto means both explicit suites; results are in the synchronized Linux checkout. Native captures use `artifacts/screenshots/light/` and `dark/`; HTML uses `html/` and `html-dark/`.

Both variants require the [GNOME VM checklist](docs/testing.md), including Light → Dark → Light without stale colours, Settings, inactive/maximized/restored/tiled windows, Mutter corners/shadows, scaling and the full Shell. WSL source/parser tests and Xvfb captures do not establish those GNOME session results.

The [surgical conformance audit](docs/surgical-conformance.md) records the invariant palette, semantic dark actions, mixed-checkbox and CSD edge fixes, native regression evidence and remaining GNOME VM acceptance.


The [theme-state backport](docs/theme-state-backport.md) supplies DING desktop
transparency in active/backdrop states and complete light/dark Shell descendants,
Quick Settings states and semantic surfaces. Majoris-Theme owns those assets,
GTK3/GTK4 bridges and variant tests. Majoris OS/session owns automatic global
attachment, its LD_PRELOAD dispatcher, Shell extension activation, wallpaper and
GNOME/Mutter lifecycle. The ISO builder can consume `theme/Majoris/` verbatim;
no GTK/Shell CSS patching or distro-only dispatcher is needed in this repository.
See the [exact VM regression checklist](docs/theme-state-vm-checklist.md).

Majoris Login is a separate native GDM/lock module under [login](login/README.md), with an independent resource package and exact-version Debian Shell patches. Its [VM acceptance matrix](login/docs/vm-validation.md) must be completed before release; ordinary GTK application themes remain separate.

## Native editor components

The factory now includes an integrated native document editor fixture:
`./scripts/run-factory.sh --page=editor --light` (or `--dark`), also available
from its Headerbars page. `editor-focus`, `editor-states` and `editor-overflow`
provide diagnostics. New reusable classes are `majoris-document-tabs`,
`majoris-editor-toolbar` and `majoris-statusbar`. GtkSourceView 5.16 development
headers and introspection bindings are included in the Debian bootstrap list;
no experimental toolkit is required. Both Majoris SourceView schemes install
with the theme. [Integration guide](docs/editor-components.md) ·
[Validation report](docs/editor-implementation-report.md).

Menu and interface typography follow the [finalisation report](docs/menu-finalisation.md), with native Pango/allocation tests and review captures at both display scales.

## Sidebar design

The factory's **Sidebar Design** page and `./scripts/run-factory.sh --page=sidebar`
show the final navigation component. Preferred width is 224px; native rows have
a 32px minimum, 4px gap, 16px icons and a fixed-inset selected indicator.
[Integration guide](docs/sidebar-design.md) ·
[Before/after table and native validation](docs/sidebar-finalisation.md).

Data presentation: [Grid/List/Details design and integration](docs/data-view-design.md),
[native finalisation evidence](docs/data-view-finalisation.md).

The [Universal Toolbar](docs/toolbar-design-system.md) provides one reusable
`Majoris.Ui.Toolbar` GTK4/Vala component, packaged as `majoris-ui-gtk4`. All uses
share a neutral 40px strip, with standard 32px or compact 28px controls and mixed
raised/flat items. Groups, separators, spacers, arbitrary native widgets and generic
segmented controls are supported. Legacy toolbar classes remain compatible.
Open the factory's Toolbars page or use `--page=toolbars`; `toolbars-narrow`,
`toolbars-editing`, `toolbars-states` and `toolbars-popover` remain available.
The [final polish report](docs/toolbar-polish.md) records 8px insets, native spacing,
focus/opacity and font validation. `toolbars-stacked` demonstrates zero-gap
document-tab composition; `toolbars-files-parent` reproduces the application
parent padding for comparison.
See the specification for Meson consumption, GTK3 composition and migration.
