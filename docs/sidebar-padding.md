# Sidebar initial padding correction

The first heading previously added a 16px section margin to the 16px outer
sidebar padding. Native GTK3 and GTK4 measurements confirmed a 32px start.
The first visible heading now uses `majoris-sidebar-heading-first`, bringing
its painted heading box to 16px from the pane boundary. The heading's font ink
has its normal line-box offset; glyph pixels need not start exactly at 16px.

| Geometry | Before | After |
|---|---|---|
| Outer top / bottom / horizontal padding | 16 / 16 / 8px | unchanged |
| First heading top margin | 16px | 0px |
| Boundary to first heading box | 32px | 16px |
| Later heading top margin | 16px | unchanged |
| Heading bottom margin / horizontal padding | 8 / 8px | unchanged |
| Row painted minimum / gap | 32 / 4px | unchanged |

The shared modifier derives from `.side-label-first` in both canonical HTML
references, is extracted into both token files, and is generated into all four
GTK entrypoints. The references retain their three existing navigation groups.
All sidebar colours, fonts, interaction rules, widths and other components stay
unchanged.

The factory's `SidebarNavigation` helper composes native ListBox headers and
uses GTK's previous-visible-row callback argument. Visibility invalidation is
centralised here; insertion, removal and reordering also update native headers.
Static preview headings use the explicit modifier. The fixture adds
`sidebar-no-heading`, `sidebar-first-hidden` and `sidebar-first-removed` modes.
The latter two change the navigation dynamically after the window is created.
No negative margins, spacers, internal-node selectors or custom drawing are used.

## Verification and evidence

`tests/test-sidebar-padding.py` measures realised GTK3/GTK4 layouts in light
and dark at 100% and 200%. It checks padding, first/later heading margins,
heading bottom/horizontal insets, 32px rows, 36px pitch, section hiding/removal/
reordering and direct-row starts. Coordinates are relative to the sidebar;
GTK4 content-origin coordinates and GTK3 margin allocations are accounted for.
The real Vala pointer/keyboard test also checks initial headers and dynamically
hidden/removed first sections. Existing scrolling, disclosure, selection,
accessibility structure, RTL and adaptive tests remain enabled.

The scroll-demo startup now waits for GTK to publish a measured scroll range
instead of assuming layout finishes within a fixed delay; focus follows the
selected destination. This preserves the existing real wheel/Home checks.

Native screenshot evidence is in `artifacts/sidebar-padding/`: `before/light`
and `before/dark` preserve the preceding factory's full-frame sectioned view;
`light` and `dark` contain current `sidebar`, `sidebar-no-heading`,
`sidebar-first-hidden`, `sidebar-first-removed` and `sidebar-scroll` captures.
Both sectioned views use the same 900×650 logical window, native font and X11
capture configuration. `geometry/sidebar-padding-measurements.json` consolidates
before/after measurements; capture-side geometry JSON additionally records the
actual Vala fixture headers. Screenshots are native GTK, unmodified full frames.

Final full regression suite: **76/76 passed, zero skips**. Canonical token
verification and deterministic generation checks also pass. Each generated GTK
stylesheet differs from the preceding version by only the first-heading rule.

Regression results are recorded in `artifacts/sidebar-padding/suite.log` and
`targeted.log`; capture output is in `captures.log`. Native X11 checks do not
establish Wayland, fractional-scale or screen-reader session acceptance; the
existing limits in the sidebar finalisation report still apply.
