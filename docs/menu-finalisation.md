# Context-menu v2 implementation

The latest implementation follows the supplied v2 mockup for **4px outer padding**,
**2px/8px separator margins** and **12px/600 bordered keycaps**. Native menu rows
retain a 32px minimum with natural growth. Existing menu surface/state palettes,
window controls, dropdowns, ordinary popovers and login remain unchanged.

The exact per-toolkit mapping and application adoption API are documented in
[menu-row-integration.md](menu-row-integration.md). The target mockup is retained
unmodified in `design/reference/majoris-full-theme-mockup-v2.html`.

## Changes

- Both canonical widget-factory references and extracted token JSON files: approved
  geometry, split shortcut groups and separate light/dark keycap palettes.
- `design/templates/gtk-common.css.in`: reusable native row/keycap classes.
- `gtk3.css.in`: compact menus/separators, 600-weight native accelerator fallback,
  and custom-row child requisitions. Ordinary popover padding remains 8px.
- `gtk4.css.in`: menu-only compact geometry, native combined accelerator capsules.
  Ordinary popovers and chooser content retain previous geometry. The menu contents node owns the 4px inset; libadwaita's extra 6px section-box padding is removed and realised edge allocations are asserted.
- `gtk-dark.css.in`: indigo keyboard focus for reusable dark rows.
- `shell.css.in`: compact popup menus, boxed accelerator labels and explicit
  preservation of Quick Settings padding. Login styles are unchanged.
- Generated light/dark GTK3/GTK4 and Shell CSS, including the dark Shell alias.
- `factory/src/menu-row.vala`, `integration/menu_rows.py`: reusable native keycap
  rows, accessible names/shortcuts, action-enabled state and dismissal.
- Factory action registrations, menu models and gallery: real keycap actions,
  shortcut-free menu, checked/radio items, leading icons and native submenus.
- Meson source/installation rules: build and expose reusable integration sources.
- `tests/test-menu-contract.py` and `test-menu-native.py`: source geometry and
  realised Pango allocations, native navigation, activation and accelerator tests.

## Evidence and limits

Before/after native screenshots are indexed in `artifacts/menu-v2/README.md`.
The matrix covers GTK3/GTK4, light/dark and 100%/200%. It includes F2, Delete,
Alt+Return, Space, Ctrl+C, Ctrl+V, punctuation and descending glyphs. Measurements
record ink/logical bounds, label allocations, actual layout origins, baselines,
ascent/descent and fonts. A larger-font fixture checks that keycaps can grow.

The previously reported shortcut clipping was not reproduced in the original
fixture. The new tests demonstrate full glyph containment rather than attributing
the issue to an unproven line-height cause. GTK3 layout origins use shared GdkWindow
coordinates, so tests convert them to local label coordinates before checking clips.

An independently opened GTK3 submenu initially retained the keyboard grab between
test scenarios. Explicitly dismissing it restored delivery of real F2 events. This
was a fixture lifecycle defect, not a theme shortcut-clipping diagnosis.

Standard third-party GTK3 menus cannot gain separate key widgets through CSS;
standard GTK4 accelerators receive a combined capsule. Exact individual capsules
require the documented component. Shell labels have the same combined-label limit.
Live GNOME Shell/Wayland/Mutter and screen-reader checks remain VM validation tasks.
Raw Xvfb root captures can omit ARGB popups; direct native popup captures are supplied
alongside surrounding-window views and X11 inventories, with no image composites.

## Final v2 validation

All **56 Meson tests passed**. The native menu matrix passed for both toolkits,
both variants and both scales, including real arrow/Enter/Escape/F2 input,
disabled actions and enlarged shortcut text. `tools/report-menu-v2.py` confirms
identical light/dark keycap allocations and ink/logical geometry in all four
pairs. Token verification, generation consistency and `git diff --check` passed.
The existing factory capture command completed for both themes at scales 1 and 2.

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson compile -C build
meson test -C build --print-errorlogs
python3 tools/report-menu-v2.py
MAJORIS_CAPTURE_PAGES=menus scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_PAGES=menus MAJORIS_CAPTURE_SCALE=2 scripts/capture-visual-regressions.sh --both
```

## Previous implementation measurements

The following notes describe the pre-v2 baseline and are retained for provenance.

# Menu and typography finalisation

The canonical light/dark HTML references, extracted tokens, GTK3/GTK4 templates,
generated GTK and Shell variants, native factory and Meson tests have been updated.
Menu surfaces are opaque, with 8px outer geometry, 4px item corners, 8px surface
padding, 4px/8px item padding, neutral stationary states and semantic destructive
foregrounds. Labels use Plus Jakarta Sans Medium at 14px; accelerators use 12px
Regular. Interactive typography is scoped to controls/navigation, preserving
existing editor/document typography. Window-control SVGs are unchanged.

## Native measurements and clipping investigation

The same real menu-model fixture was run against the original generated theme and
the updated theme. Measurements are saved under `artifacts/menu-finalisation/`.

| Toolkit | Original first row | Updated first row | Updated text allocation / logical height |
| --- | --- | --- | --- |
| GTK3 3.24.49 | 24px; 12px inherited SemiBold | 32px; 14px Medium | 24px / 19px |
| GTK4 4.18.6 + libadwaita 1.7.6 | 32px; 12px Regular | 32px; 14px Medium | 24px / 18px |

GTK3 ignores the menu item's own CSS minimum in its native requisition. A minimum
of 24px on its immediate label, plus 4px vertical padding, gives a measured 32px
row. GTK4 model buttons use a 24px content minimum plus padding directly. These
are minimum sizes: the native regression enlarges text to 32px and verifies that
both the label and row grow. No fixed label height, translations, negative margins
or clipping suppression are used. The native test records Pango baseline, ink and
logical extents, font description, row height and label allocation at both scales.
It checks full ink/logical containment and natural text width.

**The originally reported clipped capital was not reproduced with the original
CSS in this environment.** Both original fixtures contained their glyph ink. The
confirmed defects are inconsistent inherited typography, GTK3 row requisition and
missing vertical content padding, rather than a proven font-ascent or parent-clip
failure. It would be incorrect to claim a confirmed root cause of the original
application-specific clipping. That application/compositor/font environment still
needs reproduction; the new regression protects the measured native cases.

Fontconfig resolves `Plus Jakarta Sans:weight=100` to the real Medium variable font.
Existing external-font installation and packaging conventions are retained.

## Review artifacts and reproduction

`artifacts/menu-finalisation/gtk{3,4}-{light,dark}-{1,2}x/` contains measurements,
raw screen captures, native popup surface close-ups, held interaction states,
submenus, and GTK4 dropdown/boundary cases. `before-gtk*-light-1x/` contains original
comparisons. Prefer `*-surface-0.png` for context/dropdown glyph inspection; X11
window-tree files identify each captured surface. Raw root-window captures can
omit ARGB popup windows or show black rectangles under Xvfb; direct native popup
captures retain the actual pixels. They are not HTML renders or composited images.
The existing factory capture workflow also supplies surrounding application views.

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson setup build --reconfigure
meson compile -C build
meson test -C build --print-errorlogs
MAJORIS_CAPTURE_PAGES=menus scripts/capture-visual-regressions.sh --both
```

The eight native menu tests cover both toolkits, both variants and 100%/200%
scaling. The source contract additionally verifies exact geometry, typography,
opacity and semantic colours. Existing semantic colour tests now read the menu's
canonical destructive token; the obsolete hash that prohibited all dark-reference
edits was removed while retaining the exact window SVG comparison and native dark
contracts. Shell contracts distinguish opaque menus from other translucent surfaces.

## Remaining validation limits

Shell is checked by the existing grammar/selector contracts, not a live GNOME Shell
session. Mutter/Wayland shadow composition, monitor work-area placement, live system
reduced-motion behaviour and application-specific CSS conflicts still require the
repository's GNOME VM checks. Native X11 boundary and submenu captures exercise GTK
placement, but cannot establish Wayland or multi-monitor behaviour. Raw Xvfb screen
captures do not prove compositor opacity or shadow blending. No warnings were
suppressed: existing generated-C/Vala deprecations and WSL GVFS/portal diagnostics
remain in the logs.

Final validation: all **56 Meson tests passed**, including native GTK3/GTK4 CSS parsing and the complete eight-case menu matrix. Generation consistency and token verification also passed. Review links are indexed in artifacts/menu-finalisation/README.md.
