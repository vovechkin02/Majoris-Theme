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
