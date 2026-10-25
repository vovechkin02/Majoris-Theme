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
