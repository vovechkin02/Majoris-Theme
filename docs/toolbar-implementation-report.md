# Toolbar finalisation implementation report

Implemented the opt-in toolbar family in Majoris-Theme only. No first-party
application repositories, symbolic SVGs or installation/GTK bridge mechanisms
were changed. The untracked `Majoris-Theme.zip` remains user-owned input.

## Source changes

| Files | Change |
| --- | --- |
| Both canonical widget-factory HTML references | Navigation/Command, grouping, states, segmented selection, narrow example and editor distinction |
| `design/tokens.json`, `design/tokens-dark.json` | Extracted toolbar geometry, typography and palette rules |
| `design/templates/gtk-toolbar.css.in` | Explicit opt-in containers/controls, groups, fields, separators and view switcher |
| `tools/generate_toolbar.py` | Canonical-value mapping and derived border-box arithmetic; GTK3 capability adaptation |
| `tools/generate-theme.py`, `tools/generate_dark.py` | Include the toolbar template in the existing light/dark pipeline |
| Four generated GTK3/GTK4 stylesheets | Reproducible component rules; prior selectors remain unchanged |
| `factory/src/toolbars.vala` | Native stacked toolbar page, location component, real menu choices, exclusive views, keyboard shortcuts and editor comparison |
| Factory application/window/Meson registration | Toolbars sidebar page and dedicated CLI normal/narrow/state/entry/popup windows |
| `tests/test-toolbar-contract.py` | Source authority, scope, derived dimensions and editor isolation |
| `tests/test-toolbar-native.py` | Eight native toolkit/palette/scale cases, complete allocations, text, state stability, popovers, exclusive keyboard selection and narrow focus scrolling |
| `tools/capture-visual.py` | Include new pages in the established native capture workflow |
| `tools/report-toolbar-finalisation.py` | Palette geometry comparison and consolidated JSON evidence |
| `docs/toolbar-design-system.md`, README | Reusable specification, Vala examples and application ownership |

## Measured geometry

Both GTK3 and GTK4, light and dark, at logical scales 1 and 2:

- Navigation and Command bars: **40px** complete.
- Icon buttons: **32×32px**, image allocation **16×16px**.
- Text button/search entry: **32px** high.
- Toolbar segmented group: **32px**, including padding/border.
- Within-group gap: **4px**; inter-group gap: **8px**.
- Icon-to-text gap: **8px**.
- Editor comparison: **40px** strip, **28px** flat action.
- Compiled Vala factory: normal width **1280px**, narrow width **480px**.
- Nested location bar remains **32px**; crumbs and visible entry remain **26px**.

The Vala probe uses complete allocated dimensions, not content-only `get_height()`
values. The latter omit CSS padding/borders and initially reported misleading
32px bars / 16px icon buttons despite correct complete allocations.

The narrow fixture must wrap explanatory labels; otherwise a long non-toolbar
label establishes an unrelated 544px window minimum. GTK3 additionally needs
`resize()` for a mapped window. Tests now assert a real 480px viewport and that
keyboard focus scrolls the command row horizontally into view.

The 1px divider is a background stripe inside the bar; it adds no height or
outside elevation. Derived 7px icon padding and 3px segmented padding are formulas
from the approved 32px/16px/24px boxes and borders, not new design spacing tokens.

## Interaction and typography evidence

Native state flags cover hover, pressed, focus, disabled and backdrop; positions,
text baseline and geometry remain stationary. Native GTK4 grouped toggles and
GTK3 radio-style buttons preserve exclusive selection; keyboard Space activation
is exercised. Both navigation and command triggers open real native popovers or
menus. Menu labels are independently asserted Medium and their glyphs measured.
Toolbar styles do not match the location crumbs or popup controls.

Pango evidence includes allocation, ink/logical rectangles, layout origin,
baseline, ascent/descent and resolved font. Search text includes Favorites, Files,
Format and descenders/punctuation; buttons include New Folder, Back, Forward,
Refresh, Locations and Sort. Actual menu text is also measured. A 40px native
Pango title tests natural toolbar growth rather than fixed-height clipping. It
is an allocation stress test, not proof that GNOME accessibility preferences are
forwarded under Xvfb's fixed-pixel CSS environment.

The symbolic icon set is checked against the installed icon theme. Visual review
caught an unavailable Preview name; the fixture now uses the existing
`view-reveal-symbolic` icon, without modifying or adding artwork.

## Validation and reproduction

The full repository suite passed **96 tests**, including existing menus, tabs,
headerbars, location components, SourceView, sidebar and data views. The final
focused nine-test toolbar suite also passed after complete text/icon checks.
Generation/token verification and light/dark native geometry comparison passed.
Compiler deprecations and WSL GVFS/portal warnings remain visible in logs.

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson compile -C build
meson test -C build --print-errorlogs
python3 tools/report-toolbar-finalisation.py
MAJORIS_CAPTURE_DIRECTORY=artifacts/toolbar-finalisation/factory MAJORIS_CAPTURE_PAGES=toolbars,toolbars-narrow,toolbars-states,toolbars-editing,toolbars-popover scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_DIRECTORY=artifacts/toolbar-finalisation/factory MAJORIS_CAPTURE_PAGES=toolbars,toolbars-narrow,toolbars-states,toolbars-editing,toolbars-popover MAJORIS_CAPTURE_SCALE=2 scripts/capture-visual-regressions.sh --both
```

Screenshots and consolidated geometry/focus/text reports are indexed at
`artifacts/toolbar-finalisation/README.md`. The specification includes a before/after
contract table; there was no previous reusable general toolbar component to
capture as an equivalent native baseline. No simulated before image was created.

## Limits and adoption

Applications must opt in and own composition, commands, accessibility names,
shortcuts, expansion and responsive/overflow policy. Existing applications do not
change automatically. GTK3 box spacing is set through native properties because
its CSS lacks GTK4 border-spacing; GTK3 location composition remains app-owned.

Xvfb captures and held backdrop states do not establish real GNOME/Wayland state
forwarding, reduced-motion preference propagation, accessibility preference
forwarding, fractional compositor scaling or screen-reader behaviour. Those remain
session/VM checks. Direct native popup surfaces accompany window captures because
root X11/ARGB captures can omit popup pixels. No HTML or image composites substitute
for the native evidence.
