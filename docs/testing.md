# Testing

Run `meson setup build`, `meson compile -C build`, then `meson test -C build --print-errorlogs` in Debian Trixie. The Windows helper is `scripts/wsl.ps1 test`. The full Meson suite includes full HTML declaration/pseudo-element extraction and generated CSS/SVG drift; parsed semantic shadow/radius/color/state contracts; strong font aliases; reversible installer restoration, conflicts and asset migration; native GTK3/GTK4 parsers and titlebar colors; GTK3 painted button backgrounds; and native simple/dense/split geometry. Source contracts explicitly do not claim computed GTK appearance.

Generate after template changes with `python3 tools/generate-theme.py`, preserving the reference. Synchronize generated CSS and assets back to the Windows checkout before using its helper again. Capture refuses generated-theme drift rather than silently inspecting an older stylesheet.

```bash
./scripts/install-dev.sh
./scripts/render-html-reference.sh
./scripts/capture-visual-regressions.sh
python3 tools/report-visual-conformance.py
```

The renderer needs Chromium and Pillow. Native capture needs Xvfb, D-Bus, xwd/xwininfo, ImageMagick, Openbox, xcompmgr, xdotool and gtk4-demo; GTK3 painted probes need python3-cairo and python3-gi-cairo. Bootstrap includes these Trixie packages. Captures use scale 1, a 1440x1080 display, 1280x960 gallery windows, Cairo and disabled animations. Header stress fixtures use their intentionally smaller widths. Font resolution and all capture conditions are recorded in JSON.

The authoritative reference remains unchanged. A temporary rendering copy loads the exact supplied local fonts at 1440x1080 and 1440x4000 without crops. Blank frames and failed font loads are rejected. Ordinary CI can skip missing fonts; completion acceptance requires MAJORIS_REQUIRE_EXACT_FONT=1.

The Visual States laboratory holds real GTK flags, clearly labeled as diagnostics. It includes default/hover/pressed/focus/disabled/selected/backdrop for buttons, titlebar controls, inputs, selection controls and navigation. Pointer/Tab interaction remains available. Tooltip capture actually moves the pointer over Back. Popup captures preserve the full popup surface separately because xwd root capture omitted override-redirect surfaces on this setup; full-display captures are retained too.

`artifacts/geometry.json`, screenshots, logs and the generated conformance report are ignored build evidence. Reviewed observations live in `docs/visual-review.json`; regenerating the report does not automatically grant visual acceptance. Inspect changed captures and update the review record deliberately.

Final Majoris VM checks remain necessary for Mutter/Shell, fractional scaling, maximized/restore behavior, keyboard/input behavior and desktop applications. Installed GTK3 native fixtures and stock gtk4-demo provide local integration evidence. See the completion audit for current application results and exact-font validation.

## Exact supplied-font completion workflow

Use Debian Trixie only (`wsl -d debian`). Inspect the supplied archive with `unzip -l` and its actual family metadata with `fc-scan`. Extract it to `~/.local/share/fonts/Majoris/PlusJakartaSans/`, run `./scripts/install-dev.sh` and `fc-cache -f`. Verify `fc-match -f '%{family}\n'` for `Plus Jakarta Sans`, `sans-serif` and `system-ui`; all must resolve to Plus Jakarta Sans.

Preserve `artifacts/baseline/` before installing fonts or changing source. Set `MAJORIS_REQUIRE_EXACT_FONT=1` for Meson and native capture acceptance: a missing font is a failure. Ordinary font-free CI may still skip runtime resolution. The isolated geometry test preserves user-local fonts and verifies the actual Pango font used by a rendered factory label.

The HTML renderer makes a temporary copy with local normal/italic `@font-face` declarations, verifies Chromium loaded both faces, records their SHA256 hashes, and disables remote font hosts. It leaves `design/reference` unchanged. GTK and Chromium use the same supplied variable TTF files. GTK4 supports the reference line-height declarations; GTK3 rejects line-height (diagnostic in `artifacts/typography-property-probe.txt`). Both support page-heading letter spacing.

Run optional real-app captures with `dbus-run-session -- xvfb-run -a -s '-screen 0 1440x1080x24' python3 tools/check-integrations.py`. Review the availability JSON and stderr; a failed launch is not a successful integration check. This does not gate unit tests. Clock uses the existing sibling build with an in-memory settings backend. WSL app captures do not establish GNOME compositor correctness.

## Final GNOME VM checklist

Use Debian Trixie with GNOME/Mutter/Wayland, the supplied font, the installed theme and icon overlay. Record versions, scale, resolution, application versions and screenshots for each result.

- Clock: simple and split header surfaces, sidebar, cards, spin inputs, primary action, progress and all window controls.
- Files: dense headerbar, 32×32 hover plates, location/search/view/dropdown/menu controls, sidebar and list selection, overlay scrollbar. Confirm the earlier 32×44 regression is absent.
- Settings: headerbar/sidebar selection, preference groups and boxed lists, switches, combo/entry rows, buttons, dialogs and scrollbars.
- Factory: simple, dense and split headers; both split panes must share a 48px border-box target and square internal joins.
- Every application: maximized, restored and inactive states; minimize/maximize/restore/close glyphs, pointer hover, pressed, keyboard focus and tooltip behavior.
- Scale factors: 100%, 200%, and fractional 125%/150% where practical; record pixel allocations separately from logical targets.
- Shell top panel and clock, Shell popovers and menus, Quick Settings, overview, dock interaction, dialogs and tooltips.
- Mutter shadows, fullscreen/maximize transitions, Wayland client-side decorations and fractional scaling.
- GDM/login appearance in a separate safe VM test.

These checks remain required even when all WSL tests pass. Use `FULL-GNOME VALIDATION REQUIRED` for these gaps, with report status `NOT VALIDATABLE UNDER WSL`.

Real-app geometry can be inspected with the read-only optional probe: `cc -shared -fPIC tools/probe-application.c -o artifacts/probe-application.so $(pkg-config --cflags --libs gtk4)`, then run `tools/check-integrations.py` as above. It records GTK allocations/classes through public traversal APIs; it changes no widget properties. The integration harness rejects blank surfaces and captures Files list/scroll/hover and Clock preferences. `ADW_DISABLE_PORTAL=1` is the supported libadwaita setting used by isolated tests to avoid desktop portal startup under Xvfb; this does not certify portal integration.

## Light and dark completion validation

Run `scripts/run-factory.sh --light`, `--dark`, and `--system`, or choose Appearance in its existing menu. `scripts/capture-visual-regressions.sh --both` saves both native suites with identical dimensions, content and fonts. `scripts/render-html-reference.sh --both` renders the two untouched authorities using a temporary local-font copy. The dark test contracts parse the effective override block and cover semantic palette, shadows, radii, stationary motion, spinner assets and tooltip inversion. Native tests cover actual GTK3 selection, GTK4 StyleManager force/default switching and full widget-tree geometry equality. Use `MAJORIS_REQUIRE_EXACT_FONT=1 meson test -C build --print-errorlogs` for final acceptance.

Repeat every VM check above in both Light and Dark. Include normal, inactive, maximized, restored and tiled windows in Clock, Files, Settings and the factory; inspect sidebar/data selection, popovers, dialogs, tooltips, toast/banner, switches, entries and scrollbars. Inspect the top panel, Quick Settings, calendar, notifications, overview and dock in both Shell themes. Switch Light → Dark → Light without logout where supported, checking every visible and reopened transient for stale colours. The StyleManager/GSettings tests use a private memory backend and restore their previous values; production portal and session preference delivery remains a VM check. See [dark implementation](dark-theme.md) and [completion evidence](dark-theme-completion.md).

Surgical conformance regressions additionally check invariant indigo primitives,
independent dark semantic actions/focus, all six native checkbox states in both
GTK versions/schemes, halo-only titlebar focus and seven managed CSD classes.
The edge runtime fixture uses actual Openbox maximize/fullscreen states and
checks the restore glyph, 48px header, 32px plates and 16px glyphs. Directional
tiled classes are explicit diagnostic equivalents, requiring Mutter acceptance.
`tools/verify-rendered-window-edges.py` validates untouched native pixel captures
against exact edge alpha paints and rejects managed insets/corner seams.
`tools/compare-final-fixes.py` compares both complete screenshot suites to the
immutable `artifacts/baseline-final-fixes` baseline. No screenshots are cropped,
recoloured or otherwise modified for acceptance. Symbolic and primary-reference
audits are read-only and write evidence into artifacts.


## Theme-state backport validation

The baseline clean build, tests, current captures and geometry are preserved in
`artifacts/pre-theme-state-backport/`. Parsed desktop contracts cover all four
GTK entrypoints and both normal/backdrop states. Native GTK style-render probes
require zero background/frame alpha for a real `desktopwindow` class and opaque
backgrounds before/after removing that class. These prove native style rendering;
wallpaper, Home/Trash and DING extension lifecycle remain VM checks.

Shell selector/property tests check exact surfaces and descendant colours,
checked white children, insensitive text/icons, icon-button surfaces and search.
Both source round trips must independently own every colour-sensitive selector.
Negative regressions reject the specific white-surface/foreground bugs, while
legitimate selected white foregrounds remain accepted. The existing Shell
validator also enforces this contract; it does not run a GNOME Shell session.

Installer tests cover fixed light/dark and neutral auto CSS, repeat installation,
mode transitions, asset migration, conflict protection, original files/symlinks
and uninstall. A real neutral install also runs both switching cycles through
the existing GTK4 bridge. Existing GTK3 selection and GTK4 system/force switching
regressions remain enabled. No global user preferences are changed by tests.

Run the clean Meson suite with `MAJORIS_REQUIRE_EXACT_FONT=1`, generation `--check`,
and `scripts/capture-visual-regressions.sh --both`. The application captures and
geometry must match the preserved baseline. [Exact GNOME VM scenarios](theme-state-vm-checklist.md)
cover active/backdrop desktop transparency, readable Shell descendants and both
live switching directions without logout. Global process attachment, dispatcher,
Shell activation, wallpaper and lifecycle belong to the distro/session; this
repository supplies theme assets, bridges and regressions.

## Shared layout regression workflow

`layout-contract` checks token-derived body/page padding, footer padding and
semantic divider, all GTK3/GTK4 light/dark selectors, geometry parity and the
absence of broad container padding. `native shared layout` loads the generated
theme through the existing GTK4 bridge. It checks actual insets, header/body
alignment, footer height including its divider, group/list row padding, last-row
divider removal, suffix centring, 32px buttons with 16px artwork and stable
light → dark → light allocations at 360, 390, 650, 900 and 1200px.

```bash
meson setup build --prefix=/usr
meson compile -C build
MAJORIS_REQUIRE_EXACT_FONT=1 meson test -C build --print-errorlogs
python3 tools/generate-theme.py --check
./scripts/run-factory.sh --light
./scripts/run-factory.sh --dark
./scripts/run-factory.sh --system
./scripts/render-html-reference.sh --both
./scripts/capture-visual-regressions.sh --both
```

The factory `--page=layout` demonstrates desktop/compact page containers inside
ScrolledWindow and Clamp, 16px card gaps, optional headers/footers, body-only
cards, inset native preference groups and flat icon actions. Scroll each inner
example to inspect the footer and final group. Full-frame `layout-middle.png`
and `layout-bottom.png` captures also expose these parts for visual review. The preferences page compares
a boxed ListBox with a genuine PreferencesGroup, including subtitle, switch,
button and icon suffixes and an expanded row. Native container semantics are
preserved; an inset group owns a separate list boundary without extra shadow.

Capture includes `layout-360`, `layout-390`, `layout-650`, `layout-900` and
`layout-1200` in both schemes. These use `MAJORIS_CONTENT_WIDTH` to hide factory
navigation, disable horizontal Stack homogeneity and set actual page/window
width. At narrow widths the factory hides auxiliary titlebar actions while
retaining the menu and exact window controls. The capture asserts actual window
width and writes `layout-WIDTH-geometry.json`. This fixture option does not
change theme headerbar geometry or application breakpoints. For a focused rerun:

```bash
MAJORIS_CAPTURE_PAGES=layout,layout-360,layout-390,layout-650,layout-900,layout-1200,preferences ./scripts/capture-visual-regressions.sh --both
```

Expected differences: new demonstrations and preference comparison; centred
Configure suffix; compact page gutters and a single gallery column below 650px
available page width. The old section body's inset remains 16px. Final boxed
rows omit the 1px divider, so their minimum allocation can be one pixel shorter
than other rows with identical content insets. No reference/baseline is replaced.

Validation on Debian Trixie / GTK 4.18.6 / libadwaita 1.7.6: build and all 40
Meson tests passed with exact Plus Jakarta Sans, including both parsers,
headerbar geometry, variant geometry, explicit/system switching and installer
bridge tests. Both HTML renders and full native capture workflows completed;
changed layout captures were refreshed after responsive fixes. Evidence is in
`artifacts/layout-suite.log`, `artifacts/layout-native.json`,
`artifacts/layout-captures.log` and `artifacts/screenshots/`. Required tools and
Google Fonts' normal/italic Plus Jakarta Sans were installed only in the WSL
test environment, with the repository's font aliases. No project dependency was
introduced. Existing generated palettes, glyphs and HTML references are unchanged.

Remaining Majoris GNOME VM acceptance: actual pointer hover/press and keyboard
focus/disabled states on preference rows and flat actions; backdrop readability;
Mutter headerbar allocation/window controls; fractional scaling; system scheme
changes through the real desktop portal; scrolling every card variant; and
representative Clock/Files/Settings/Terminal adoption. Xvfb allocation, capture
and bridge tests do not establish these session-level results. Follow the
existing VM checklist; do not accept or overwrite baselines automatically.

## Editor component validation

The supplemental showcase is preserved in `design/reference/editor-v1/`.
Run `python3 tools/generate-theme.py` and `--check` after changing
`gtk4-editor.css.in`, `editor-tokens.json` or SourceView XML templates. All
GTK4 editor CSS and both distributable XML schemes are generated. The original
HTML factories and primitive token JSON are unchanged.

The Debian bootstrap now lists stable `libgtksourceview-5-dev` and
`gir1.2-gtksource-5` dependencies. They were already installed for this task;
no system package modification or distribution upgrade was performed.

New Meson tests cover opt-in selectors and GTK3 isolation, every editor/syntax
role and 4.5:1 foreground contrast, installed Relax NG XML validation through
libxml2, actual standard XDG discovery, repeated development installation,
rollback conflicts and restoration, staged `/usr` packaging/discovery, native
38/40/34px bars and 28px controls, six interaction state flags without geometry
changes, light → dark → light, explicit monospace, third-party scheme ownership,
pinning/reordering/closing and narrow overflow. The native suite runs at both
GDK_SCALE=1 and 2. Existing 48px headerbar, exact window glyph, Notebook,
button, palette, installer and system/explicit appearance regressions remain.

```bash
meson setup build --prefix=/usr --reconfigure
meson compile -C build
MAJORIS_REQUIRE_EXACT_FONT=1 meson test -C build --print-errorlogs
python3 tools/generate-theme.py --check
DESTDIR=/tmp/majoris-theme-stage meson install -C build
./scripts/run-factory.sh --page=editor --light
./scripts/run-factory.sh --page=editor --dark
./scripts/run-factory.sh --page=editor --system
python3 tools/render-editor-reference.py
./scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_SCALE=2 MAJORIS_CAPTURE_PAGES=editor,editor-overflow ./scripts/capture-visual-regressions.sh --both
```

The staged-package test uses its own temporary DESTDIR rather than modifying
`/usr`. Development install tests isolate XDG config/data/state; both schemes
are installed simultaneously and no user's existing scheme is destroyed.
Factory launch smoke checks can use `MAJORIS_TREE=1` to dump the realized tree
and exit automatically. `--page=editor-source` focuses the editor to expose active selection;
`--page=editor-focus`, `editor-states` and
`editor-overflow` provide focused, held-state and overflowing tab diagnostics.
Formatting and status menus are genuine native controls. The editor fixture
is accessible from the existing factory Headerbars page.

Capture adds editor composites (tabs, toolbar, syntax/selection/gutter and
statusbar together) in both modes, focus/state and long-name overflow fixtures.
It preserves full-frame root screenshots without crops or pixel manipulation.
At 200% the framebuffer is 2880×2160; captures are stored in `light-2x` and
`dark-2x`. The capture environment now supplies the actual Majoris icon overlay
in an isolated XDG directory, preserving user fonts and Adwaita fallback icons.
This corrects missing symbols in earlier captures without changing icon assets.

The supplemental HTML renderer uses temporary copies with local fonts and
hides unrelated sections/introduction to expose each review section; target
markup/styles and preserved references stay unchanged. It verifies appearance
and font readiness and saves source/font hashes. These reference captures are
visual comparisons, not GTK rendering or automatic acceptance.

Native evidence: `artifacts/editor-suite.log`, `editor-native.json`,
`editor-native-2x.json`, `editor-factory-switching.json`,
`editor-factory-switching-2x.json`, `editor-captures.log`, `editor-2x-captures.log`,
`editor-full-captures.log`, `editor-baseline-nodes.txt` and screenshot directories.
The native baseline records libadwaita's unthemed tab strip at 53px under the
existing generic control styles; the opt-in component measures 38px. Source
scheme selection and native operations are exercised without an app CSS provider.
See [visual observations and deliberate differences](editor-implementation-report.md).

Remaining GNOME/Mutter acceptance: actual pointer drag/drop and cross-window
transfer, keyboard traversal/close and screen-reader behavior, real window
activation/backdrop, Wayland, fractional scaling, increased accessibility fonts
and real system/portal-driven appearance changes. Xvfb 100%/200% screenshots
and held native state flags do not establish those session/input results.


## Location component verification

Run `python3 tools/generate-theme.py --check` and `./scripts/test.sh`.
The `location component contract` verifies opt-in selectors, scheme palettes,
9px/7px exceptions, focus colours, normal control geometry and GTK3 isolation.
`native location interactions` compiles the actual factory component and uses
X11 input via xdotool: Ctrl+L, Alt+D, selection, invalid/valid Enter, Escape,
outside cancellation, breadcrumb activation, empty-space click, history,
Up/Home, narrow layout and Light → Dark → Light foreground checks.
Existing contracts cover exact window-control SVGs and unchanged components.

Run `./scripts/run-factory.sh --light --page=location` and repeat with `--dark`.
Use `--page=location-editing` for an editing capture and
`MAJORIS_CONTENT_WIDTH=480` for narrow windows. Scroll the diagnostic section
for high contrast, editing and backdrop. Held hover/pressed/focus flags are
visual diagnostics, not proof of real input or accessibility.
Capture with the existing `tools/capture-visual.py` using
`MAJORIS_CAPTURE_PAGES=location,location-editing` and `MAJORIS_VARIANT=light` or
`dark` under dbus-run-session / Xvfb. See [verification evidence](location-implementation-report.md).
Real GNOME/Mutter, Wayland, fractional scaling, portal-driven desktop switching
and screen-reader acceptance require the target desktop.

## Sidebar finalisation validation

For reproducible Xvfb startup, the final run used `GIO_USE_VFS=local` and
`meson test -C build --num-processes 4 --print-errorlogs`. Keep native capture
and the full suite separate when investigating startup-timing failures.

Run generation/extraction through the existing pipeline:

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson setup build --reconfigure
meson compile -C build
MAJORIS_REQUIRE_EXACT_FONT=1 meson test -C build --print-errorlogs
```

`sidebar contracts`, four `GTK3/4 native sidebar 1x/2x` tests and
`native sidebar input and adaptation` extend the existing suite. They cover
actual ListBox/StackSidebar trees, logical 32px rows and 36px pitch, icon/gap
allocations, Pango sizes/weights/ink/baselines, badge preservation, ellipsis,
state stability, real indicator pixels in LTR/RTL, larger native Pango text,
actual pointer/keyboard interaction, scrolling and adaptive focus restoration.
The existing geometry report now asserts a 224px main factory sidebar.

```bash
MAJORIS_CAPTURE_DIRECTORY=artifacts/sidebar-finalisation MAJORIS_CAPTURE_PAGES=sidebar,sidebar-basic,sidebar-states,sidebar-focus,sidebar-selected-pressed,sidebar-scroll,sidebar-narrow,sidebar-narrow-content,sidebar-rtl,sidebar-large,sidebar-backdrop,split ./scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_DIRECTORY=artifacts/sidebar-finalisation MAJORIS_CAPTURE_SCALE=2 MAJORIS_CAPTURE_PAGES=sidebar,sidebar-states,sidebar-narrow-content,sidebar-large,split ./scripts/capture-visual-regressions.sh --both
./scripts/render-html-reference.sh --both
```

State fixtures hold real widget flags. The backdrop fixture instead opens a
small native focus-target window so the sidebar window becomes genuinely
inactive. Captures remain full-frame native output. Existing before images
are preserved separately; do not replace them to grant acceptance. Reference
HTML is now intentionally revised for this sidebar contract; previous
completion reports describe earlier, unchanged-reference passes.

See [the sidebar report](sidebar-finalisation.md) for the complete before/after
table, screenshot map, evidence and GNOME/Wayland/fractional-scaling limitations.
In particular, actual enlarged Pango text is tested without claiming that
legacy Xft DPI or GNOME's text-scaling settings automatically alter fixed CSS
pixel typography. Real screen-reader, high-contrast and session settings need
the Majoris VM.

### Initial sidebar padding

The four `sidebar initial padding` tests exercise GTK3/GTK4 at 1× and 2×,
including visibility/removal/reordering and direct-row starts in light/dark.
See [native spacing evidence](sidebar-padding.md). Capture the fixtures with:

```bash
MAJORIS_CAPTURE_DIRECTORY=artifacts/sidebar-padding MAJORIS_CAPTURE_PAGES=sidebar,sidebar-no-heading,sidebar-first-hidden,sidebar-first-removed,sidebar-scroll ./scripts/capture-visual-regressions.sh --both
```

### Data views

See [data-view specification](data-view-design.md) and
[finalisation evidence](data-view-finalisation.md). Tests named `data view`
exercise native densities, metrics, selection pixels, thumbnail aspect ratio,
GTK3 equivalents, real sort/resize/modifier input and a 1,200-item recycled grid.
State diagnostics use actual GTK flags; the input test uses X11 events.

```bash
meson test -C build --num-processes 4 --print-errorlogs
MAJORIS_CAPTURE_DIRECTORY=artifacts/data-view-finalisation MAJORIS_CAPTURE_PAGES=data-grid,data-grid-compact,data-list,data-list-compact,data-column,data-column-compact,data-column-sorted,data-column-multi,data-column-resized,data ./scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_DIRECTORY=artifacts/data-view-finalisation MAJORIS_CAPTURE_SCALE=2 MAJORIS_CAPTURE_PAGES=data-grid,data-grid-compact,data-list,data-list-compact,data-column,data-column-compact ./scripts/capture-visual-regressions.sh --both
```


## Data-view focus consistency and metadata

`data view focus validation 1x/2x` uses real X11 pointer/key events and native
screenshot pixels, verifying the owner row/tile, 2px focus, absence of nested
Details cell rings, selection combinations, Ctrl/Shift selection, focus loss,
view switching, keyboard return, disabled views and focused child controls.
`data view metadata validation 1x/2x` checks every requested string at 12px/400,
Pango extents including layout offsets, label and parent containment, standard/
compact rows, resolved fonts and normal/unhinted rendering settings.
GTK3 tests additionally verify native pointer/cursor navigation, Shift selection,
inactive-window selection retention and focus return. GTK3 retains its native
focus model rather than emulating GTK4 CSS states.

```bash
python3 tools/generate-theme.py --check
meson test -C build --num-processes 4 --print-errorlogs
```

New tests regenerate unmodified native captures under `artifacts/data-view-focus/`
in `light`, `dark`, `light-2x` and `dark-2x`. The `geometry` directory includes
`focus-state-report.json`, `metadata-text-metrics.json` and corresponding `-2x`
reports. [Investigation, measurements and limitations](data-view-focus-validation.md).
