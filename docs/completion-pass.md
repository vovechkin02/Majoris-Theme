# Exact-font completion pass — 2026-10-08

This targeted pass preserves native GTK/libadwaita structure. The supplied HTML matches `design/reference/majoris-widget-factory.html` byte-for-byte (SHA256 `254f7cc14926302526517d9c312740873e4fbe40f2fab93c6541708777bbd3d5`). The reference was not edited.

## Runtime and font evidence

Debian GNU/Linux13.5 (Trixie), GTK3 3.24.49, GTK4 4.18.6, libadwaita1.7.6, Meson1.7.0, Vala0.56.18. All Linux commands used `wsl -d debian`.

The supplied `Plus_Jakarta_Sans.zip` contains14 static TTFs (seven upright/seven italic) and two variable TTFs, plus OFL/README. `fc-scan` confirms family Plus Jakarta Sans rather than relying on filenames. It was extracted to `/home/administrator/.local/share/fonts/Majoris/PlusJakartaSans/`; repository aliases were already correct and were activated by the development installer.

Native regular resolution and HTML normal face use `PlusJakartaSans-VariableFont_wght.ttf` (SHA256 `4c5552ecc1230e6dfdf6e8755d24436fca395ad9f4ecb25287ab3e9ff7a9e68d`). HTML italic uses `PlusJakartaSans-Italic-VariableFont_wght.ttf` (SHA256 `84e8f03ee07cee2f6a5c24963c15eef8210bdcb355e4592ab7256e9cbe45d8e9`). `fc-match` for explicit family, sans-serif and system-ui resolves Plus Jakarta Sans. Native geometry reports the actual rendered heading's Pango font, not just the requested CSS family. Chromium verifies successful loading of both local faces. Fontconfig fallback order remains Plus Jakarta Sans, Noto Sans, Cantarell.

## Before versus after

Baseline is immutable under `artifacts/baseline/`: test-results, font-resolution, geometry-report, full native screenshots and individual verbose diagnostic logs. After evidence is under `artifacts/`: final build/tests, geometry, native/HTML screenshots and metadata. Both native runs use scale1,1440×1080 Xvfb/Openbox/xcompmgr,Cairo,1280×960 gallery windows and the same component workflow.

| Issue | Before | After | Classification |
|---|---|---|---|
| Exact UI font | Cantarell; runtime test skipped | Explicit/generic queries and rendered Pango label use supplied Plus Jakarta Sans; no skip | THEME BUG in development runtime configuration, resolved |
| Geometry harness font isolation | User font directory hidden by temporary XDG_DATA_HOME | User font directory remains visible; strict Pango assertion | FACTORY BUG (test harness), resolved |
| Reference font source | Installed fallback with remote hosts disabled | Temporary local @font-face copy; both faces verified loaded; source hash preserved | FACTORY BUG (reference harness), resolved |
| Heading typography | Libadwaita title-1≈23.53px/800 | HTML24px/700 with-0.02em spacing | THEME BUG, resolved |
| Card/dialog line spacing | Native defaults | GTK4 card descriptions1.45/dialog body1.5 from reference | THEME BUG, resolved for GTK4; GTK3 line-height rejected by parser |
| Factory page description | Centered instruction text | Left-aligned reference gallery description | FACTORY BUG, resolved |
| Chooser samples | Default Sans Regular12 and white colour | Plus Jakarta Sans10pt and indigo sample | FACTORY BUG, resolved; native previews retained |
| GTK3 Pixman warnings | Ten invalid-rectangle diagnostics in isolated state test | Same tests with600×400 window emit no Pixman warnings | FACTORY BUG (undersized harness allocation), resolved |
| GTK4 state probe | Intermittent late BACKDROP overwrites ACTIVE, baseline failed | Explicit state reapplied after event settlement; palette assertions retained | FACTORY BUG (event/state harness), resolved |
| Simple/dense/split headers |48/48/48/48px|48/48/48/48px|No regression |
| Window controls/glyphs |32×32 /16×16|32×32 /16×16|No regression |
| ActionRow |52px|54px|NATIVE TOOLKIT CONSTRAINT: subtitle font metrics |
| SwitchRow/ComboRow |50/50px|50/50px|No regression |
| EntryRow/PasswordEntryRow |52/52px|54/54px|NATIVE TOOLKIT CONSTRAINT: native floating-title editor |
| SpinRow |69px|69px|NATIVE TOOLKIT CONSTRAINT: integrated expanding editor |
| Expanded ExpanderRow |127px|127px|NATIVE TOOLKIT CONSTRAINT: child row included |
| ViewSwitcher |Native icons/label structure|Retained; StackSwitcher remains label-only equivalent|NATIVE TOOLKIT CONSTRAINT |
| Popover/menu |Native arrow/accelerators|Retained; destructive item remains flat danger text|NATIVE TOOLKIT CONSTRAINT |
| Banner |Centered message/no leading icon|Retained native Adw.Banner; exposed surface matches|NATIVE TOOLKIT CONSTRAINT: no leading-icon slot |
| Toast |Native close/control distribution|Retained; dark/radius8/p300 action/shadow match|NATIVE TOOLKIT CONSTRAINT: native minimum/layout; no GTK CSS max-width |
| Dialog |Equal response distribution|Retained actual AlertDialog with divided surface2 footer/destructive response|NATIVE TOOLKIT CONSTRAINT |
| Status |Native symbolic icon|48px p50 tile/p600 glyph retained|NATIVE TOOLKIT CONSTRAINT: icon artwork differs; theme styling passes |
| Tooltip |Real pointer-triggered tooltip|Recaptured with supplied font;11px,6/8padding,radius4,dark/shadow|No remaining theme defect observed |
| GTK3 typography |Weight650 represented600; native line metrics|Exact family now present; line-height remains unavailable|NATIVE TOOLKIT CONSTRAINT |
| GNOME/Mutter/GDM |Not runtime verified|Still requires full desktop VM|FULL-GNOME VALIDATION REQUIRED |

Baseline Meson:16 OK,1 FAIL (GTK4 state),1 SKIP (font). Final Meson:18 OK,0 failures,0 skips. Header geometry, shadow/radius/colour/selector contracts remain passing. Spinner tests now verify SVG geometry, CSS asset reference, native animation reference and installed subtree. Both native fixtures render the dedicated spinner. Level bar stays DISCRETE with eight segments and value6. Preference regression checks require all seven native row types and their50px minimum without forcing natural row heights smaller.

## Typography review

Body13px, button13px/600, sidebar13px, page heading24px/700, card heading14px, descriptions11.5px, menu12px, preference titles13px/600/descriptions11.5px, dialog16px/12px, tooltip11px and toast12px remain in the design hierarchy. Inspect overview, preferences, inputs, menus-popup, dialog, tooltip-popup and feedback against the complete local-font reference. The heading spacing and GTK4 description/body line-height are now explicit. Baselines and control centering use Pango/native layout rather than browser rasterization. GTK3 rejects `line-height` but accepts `letter-spacing`; exact browser line-box parity is therefore PARTIAL for GTK3, not a falsely passing global equivalence claim.

## Diagnostic investigation

Run `dbus-run-session -- xvfb-run -a python3 tests/test-native-state-colours.py 3` individually. Original stderr is saved in `artifacts/baseline/gtk3-states-verbose.txt`. The realized GTK3 widget test separately emits no Pixman warning (`gtk3-widgets-verbose.txt`). A controlled copy changing only default window size to600×400 removes the diagnostic (`gtk3-sized-probe.txt`); final harness keeps that allocation. CSS and palette assertions were unchanged during the probe. This points to test-window shadow damage/clipping at minimum allocation, not WSL rendering assumed harmless. No stderr redirection to discard diagnostics or suppression was added. GTK4's independent late-backdrop race is handled by reapplying the explicitly tested native state after settlement.

## Evidence and acceptance

Native capture covers overview, buttons, controls/states, selection, inputs, ranges/progress/level/spinner, all preference rows, navigation, popover/menu, banner/toast, status, real tooltip, real dialog, simple/dense/split headers, overlay scrollbars, GTK3 native and stock GTK4 demo. Separate complete popup surfaces preserve override-redirect windows omitted by root xwd. HTML overview/full-reference use the same supplied font files. See `artifacts/visual-conformance-report.md` for reviewed category statuses and `artifacts/integration/availability.json` for real application launch results.

Design/theme correctness is supported by source contracts, native geometry, exact font resolution and reviewed captures. Native toolkit structure remains explicitly PARTIAL. WSL captures cannot certify GNOME Shell/Mutter/GDM or fractional Wayland scaling. Complete the final VM checklist in `docs/testing.md` before claiming full desktop conformance.

## Changed files and reproducibility

The exact source manifest is `docs/changed-files.txt`. Changes are confined to generated GTK typography and its source templates, factory description/chooser samples and Pango reporting, font/geometry/state/asset/typography regression assertions, deterministic local-font HTML rendering, strict capture acceptance, optional application integration capture, and review/testing/report documentation. Fontconfig XML already satisfied both strong aliases and required fallback order, so no cosmetic rewrite was made.

Reproduce with `MAJORIS_REQUIRE_EXACT_FONT=1 meson setup --wipe build`, `meson compile -C build`, `MAJORIS_REQUIRE_EXACT_FONT=1 meson test -C build --print-errorlogs`, `./scripts/install-dev.sh`, `./scripts/run-factory.sh`, `MAJORIS_REQUIRE_EXACT_FONT=1 ./scripts/capture-visual-regressions.sh`, `./scripts/render-html-reference.sh`, and `python3 tools/report-visual-conformance.py`. Interactive factory launch was smoke-tested under Xvfb and deliberately terminated after4seconds. The screenshot suite subsequently exercised all pages.

## Real application findings and fixes

Debian runtime dependencies, Nautilus and GNOME Control Center were installed to make the optional checks concrete. Majoris Clock's existing sibling binary then ran without changing its project. The initial WSLg/default-backend attempt produced blank Xvfb images; these were rejected, and integration capture now explicitly uses X11, waits for visible windows, and sets Majoris icon/font settings in its temporary configuration.

Files and Clock exposed a real hidden-banner defect: applying padding/border to `banner` left a26px indigo strip even when its revealer was closed. The theme now applies the surface to the public revealable content node, and a native unrevealed Banner regression asserts zero height. Actual Files/Clock captures confirm the empty strip disappeared. This is a resolved THEME BUG, not a native constraint.

Files also reproduced the32×44 window-control regression. Read-only GTK allocation probing showed its content header60px, native homogeneous toolbar stack44px, and all three title buttons32×44. A hidden native query-entry suffix inherited the full-size generic button minimum and its native internal margins. A factory compound-entry stack reproduces exactly60/44px before the fix (`artifacts/integration/compound-entry-before.txt`). The generic `headerbar entry button` treatment now uses a20px, borderless, shadowless internal control with neutral hover/press. Afterward the unchanged strict factory geometry test passes48px, and the real Files probe shows both header panes48px, three32×32 controls and16×16 glyphs. No Nautilus ID selector or application hack was added. `Files-geometry-before.txt` and `Files-geometry.txt` preserve measured evidence.

Clock's simple/split headers, sidebar, focus cards, spin fields, primary action, progress display and window controls were visually inspected. Header surfaces align at48px, with square internal joins; hidden-banner strips no longer appear. Real pointer close-hover and native preference-page captures are included. Files captures include location/search/view/dropdown/menu controls, sidebar selection, list selection and scrolled view. Native folder artwork and application-owned sidebar widths/content remain application differences.

GNOME Control Center first rejected the non-GNOME session. With an explicit GNOME session marker it stayed running but exposed no visible application surface; the capture was blank and rejected. That is an environmental integration limitation, not a visual PASS. Its hardware/session-dependent panels remain on the full GNOME VM checklist. GTK4 demo and GTK3 native fixtures were also successfully captured. D-Bus/portal/PipeWire/service diagnostics remain in logs; isolated theme tests use libadwaita's supported `ADW_DISABLE_PORTAL=1` to avoid unavailable desktop-service startup, while integration logs retain actual application failures.

The final evidence set contains27 refreshed native PNG captures (including separate popup/tooltip surfaces),2 exact-font HTML PNGs, and7 valid Files/Clock integration PNGs. A rejected blank Settings PNG is retained only as failed environment evidence. Before/after geometry is also summarized in `artifacts/geometry-before-after.json`. The supplied variable normal face resolves for regular, semibold and bold; italic resolves to the supplied italic variable face.
