# Native Paned 1px divider verification

The default Majoris splitter allocates exactly **1 logical pixel**, horizontally
and vertically. Its painted line fills that boundary; there is no transparent
gutter. The exception is the explicit native `wide_handle=true` option: 16px
allocation with a crisp 1px line positioned 8px from the separator origin.

## Implementation

Both canonical HTML references expose `--gutter:1px`, `--wide-gutter:16px` and
`gap:0`. GTK3/GTK4 templates consume those tokens; all four light/dark stylesheets
are generated. Only native `paned > separator` hierarchies change.

The templates explicitly reset inherited directional padding/negative margins,
wide backgrounds and state images. This matters even when adjoining child bounds
already show a 1px gap: the imported GTK theme can retain an overlapping padded
handle or paint its own selected-state colour. GTK3 keyboard focus uses the native
separator's `:selected` state. Focus/drag use Majoris Indigo (#6366F1 light,
#818CF8 dark); the neutral line is #E5E5E9 / #313136. Focus changes colour, with no
2px outline, second line or layout change. Hover strengthens colour. Disabled and
backdrop restore the subtle border. The existing stationary 128ms colour
transition remains.

## Native evidence

Tests run under Debian WSL, X11/Xvfb, using GTK 3.24.49, GTK 4.18.6 and libadwaita 1.7.6. Screenshots
are unmodified `xwd` window captures converted to PNG. Pixel checks inspect those
physical screenshots, rather than downsampling a WidgetPaintable texture.

| Measurement | Result |
|---|---|
| Horizontal default separator | 1 x 150 logical px |
| Initial start child | x=0, width=220 logical px |
| Initial end child | x=221, width=467 logical px |
| Vertical default separator after window resize | 818 x 1 logical px |
| Default transparent gutter | 0 logical px |
| GTK4 separator-node padding / border | 0 on all sides (also explicitly reset in GTK3 CSS) |
| Default / hover / active / keyboard focus | 1px split-axis allocation |
| RTL, window resize and nested splits | 1px split-axis allocation |
| Explicit wide, both orientations | 16px split-axis allocation |
| Normal and focus paint at 100% scale | 1 physical px |
| Normal and focus paint at 200% scale | 2 physical px = 1 logical px |

The [consolidated measurements](../artifacts/phase2-controls/paned-divider-summary.json) cover all 18 final profiles.
Each profile writes `paned.json` containing separator dimensions, start/end child
rectangles, real hover/active/focus allocations, paint measurements and colour.
For example: [GTK4 light geometry](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned.json),
[GTK4 dark at 200%](../artifacts/phase2-controls/gtk4/dark/cairo-2x/paned.json),
[GTK3 light geometry](../artifacts/phase2-controls/gtk3/light/default-1x/paned.json).

Representative genuine native screenshots:

- [Horizontal light](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned.png)
- [Horizontal dark](../artifacts/phase2-controls/gtk4/dark/cairo-1x/paned.png)
- [Vertical](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-vertical.png)
- [Hovered](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-horizontal-hover.png)
- [Keyboard focused](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-horizontal-focus.png)
- [Sidebar/content](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-sidebar-content.png)
- [Content/preview](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-content-preview.png)
- [Nested horizontal/vertical](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-nested.png)
- [Explicit wide focused](../artifacts/phase2-controls/gtk4/light/cairo-1x/paned-wide-focus.png)

The ignored `artifacts/` directory holds local test outputs; rerunning the native
matrix recreates them. Source, tests and this report remain tracked.

## Interaction and Files scope

Real `xdotool` pointer drags acquire the measured separator centre, press, move
and release; tests assert that native positions change while allocation stays
1px. F8 plus arrow keys also changes native positions. Both orientations, RTL,
window resizing, inner/outer nested panes, minimum-child constraints, native
shrink/resize settings and normal/wide switching are exercised. Wide dragging and
keyboard operation are independently tested.

A 1px pointer target is harder for a person to acquire than the previous 8px
layout gutter. The tests establish successful centre acquisition, not human
usability or a hidden 8px target. Directional padding/negative margins are reset;
no additional invisible target or custom event controller is installed. The
explicit 16px wide handle remains available to applications needing that option.

Sidebar/content/preview captures reproduce the native hierarchy with resizable
panes. They are fixtures, not a launched Files application. No Files executable,
source or separate screenshot attachment was supplied, so application-specific
responsive layout and actual Files UI conformance remain unverified. No Files
source or application-specific CSS was changed.

## Verification

The final Phase 2 run passed **21/21**: the source contract, 18 native profiles
and both GTK CSS parsers. Profiles include GTK3 light/dark at 1x/2x, and GTK4
light/dark at 1x/2x under Cairo, GL and the default renderer, plus enlarged fonts.
See [final matrix log](../build/meson-logs/paned-complete.txt).

Compilation passed. Token extraction and stylesheet generation completed;
`generate-theme.py --check` passed. Both canonical token JSON files match the
HTML extraction. A parsed before/after comparison of all four generated CSS files
confirmed that every changed selector belongs to Paned; generic separators and
other components are unchanged. `git diff --check` passed.

The full 165-test regression run completed with **159 passed / 6 failed** while
the implementation was being refined. Four failures were intermediate Paned
contract/focus-paint issues, corrected and covered by the final 21/21 run above.
All unrelated native/component regressions passed, including menus, toolbars,
sidebar, data views, preferences, switches, segmented controls and layout spacing.
See [complete regression log](../build/meson-logs/testlog.txt).

Two pre-existing failures remain and were reproduced separately:
`design-tokens` reports that minimize/maximize/close/restore SVGs differ from the
HTML artwork, and `theme-tree` rejects existing non-16px icon viewBoxes. These
were already documented in the repository's Phase 2 and spacing reports; no icon
files were changed. Token-only extraction preserves that artwork rather than
silently replacing it. The full `verify-design-tokens.py` check therefore still
fails on those SVGs, despite both canonical token comparisons passing.
See [isolated icon failures](../build/meson-logs/paned-icon-baseline.txt).
No tests were disabled, skipped or marked expected-failure.
