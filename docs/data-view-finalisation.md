# Data view finalisation — 26–27 October 2026

Grid/List/Details now have reusable opt-in GTK styling, two densities, canonical
light/dark references and tokens, and a dedicated native Data Views gallery.
The previous ColumnView example reuses the same cell component and compatible
`majoris-data-view` class. Its proportional-width tick callback has been removed
in favour of native resizable/expanding columns.

## Before and after

| Property | Before | Final |
|---|---|---|
| Primary data labels | 12px | 14px Medium / 500 |
| Selected label weight | Inherited, incompletely specified | Same 14px/500; no width/baseline shift |
| Secondary metadata | No reusable role | 12px/400 |
| Column headers | 11px Bold / 700, uppercase fixture | 12px SemiBold / 600, title case |
| Cell padding | 9px vertical / 12px horizontal | Standard 8/16px; compact 4/8px |
| List complete row | No shared target | 40px standard / 32px compact |
| Details complete row | No explicit complete-allocation target | 40px standard / 32px compact |
| Details complete header | Content/padding driven | 32px in both densities |
| Grid tile | No final shared family | 128×160px / 96×128px targets |
| Grid artwork | No separate contract | 96×96px / 64×64px |
| Grid rendered icon | Unspecified | 64px / 32px in the fixture |
| Tile inset / artwork-label gap | Unspecified | 8px / 8px |
| Grid minimum gap / outer inset | Unspecified | 16/16px standard; 8/8px compact |
| Grid label | Unspecified | 14px/500, natural Pango metrics, up to two lines |
| List/Details icon / gap | Not composed in the old table | 16×16px / 8px |
| Item decoration | Partial rules, legacy boxed alias | Flat surfaces; list radius4, grid radius8, details radius0 |
| Separators | Inconsistent cell/row ownership | Details 1px rows; optional body columns; subtle header dividers |
| Boxed container | Forced boxed-list in gallery | Explicit optional structural border/radius8 |
| Selection | Incomplete coverage | Full tile/row; continuous across table cells; no sidebar stripe |
| Hover / press | Incomplete families | Shared neutral roles; selected combinations retain indigo |
| Focus | Incomplete nested handling | Separate 2px treatment; one details-row focus surface |
| Disabled / backdrop | Mostly generic fallback | Explicit suppression/reduced emphasis; backdrop keeps selection |
| Interaction | Existing shared timing | Stationary 128ms cubic-bezier(.2,0,0,1) |
| Density switching | Absent | Explicit standard/compact toggle independent of width |
| Sorting | Static StringList table | Native name/date/type/size ascending/descending sorters |
| Column widths | Continuous proportional tick reset | Application defaults, Name expand, native resize handles |
| Selection through modes/sorting | Not demonstrated | Shared model and record-identity preservation |
| Large data | Three sample records | Separate 1,200-item native recycling fixture |

The new data roles preserve approved palettes: white/#202023 surfaces,
#EEF2FF/16%-indigo selection, #3730A3/#E0E7FF selected text and
#6366F1/#818CF8 focus. The broader primitive palette and unrelated controls have
not been redesigned. All source rules are in `gtk4-data.css.in` and
`gtk3-data.css.in`; complete-allocation minima are derived by `generate_data.py`.

## Native evidence

`artifacts/data-view-finalisation/` contains unmodified native screenshots,
including standard/compact grid/list/column in light/dark and at 200%; sorted,
multiselected, resized and inactive examples; narrow, RTL and enlarged-text
examples; GTK3 TreeView/IconView equivalents; and the updated original gallery.
`before/light/column.png` and `before/dark/column.png` preserve the previous
ColumnView gallery; compare the current `data.png` captures at the same gallery
window/font configuration. These are genuine GTK screenshots, not HTML renders.

`geometry/native-1x.json` and `native-2x.json` record all six native GTK4 density/
family combinations in both themes. Complete rows are 40/32px, headers 32px,
painted tiles 128×160/96×128px and artwork 96×96/64×64px. Native outer grid-cell
widths are reported separately because GTK distributes surplus. Labels use
14px Medium, metadata 12px regular and headers 12px SemiBold. Pango logical and
ink extents fit realised label allocations. Thumbnail pixels retain landscape,
portrait and square aspect ratios; delivery does not shift labels or tiles.

`geometry/states.json` and corresponding native PNGs validate actual rendered
hover, pressed, selected, selected-hover, selected-pressed, focused,
focused-selected, disabled and genuine inactive-window selection. Diagnostic
flags are identified separately from real input tests. Selection retains500
weight and geometry; focus/selection remain independently visible.

`geometry/interactions.json` records real X11 pointer and keyboard actions:
all four sortable headers in both directions, record-identity preservation,
resize persistence, mode/density switching, Ctrl/Shift selection, select-all,
activation, narrow/RTL/enlarged-text layouts and stress recycling. The observed
1,200-item grid initially created 385 tile widgets, created 386 by the end-jump,
and unbound 384; it did not construct 1,200 widgets. Only the active view binds
its model. Factory unbind resets all record-dependent state.

`geometry/gtk3-1x.json` / `gtk3-2x.json` record native TreeView rows/headers/fonts
and supported list/grid/detail equivalents, including real selected pixels.
Focused GTK3 IconView specificity and native renderer alpha compositing were
also checked: GTK3 selections are flattened over the approved data surface,
and symbolic previews use their style context for correct dark contrast. The final focused matrix and thumbnail/record-cleanup runs pass as recorded in
`final-verification.log`, `thumbnails-final.log`, and `final-current.log`. Native
modifier input waits for distinct allocated compact rows before clicking, so
recycled widgets are not sampled before GTK completes their layout.

GTK3 item-height and multiline
IconView differences are documented instead of represented as exact GTK4 parity.

The implementation exposed and corrected native composition issues: renderer
padding versus complete row heights, vertical expansion shifting grid artwork,
non-grid icons hidden by thumbnail binding, temporary string lifetimes in Vala,
window-decoration insets affecting narrow resize targets, and excessive hidden
view widget pools. No drawing-area replacement or per-row appearance provider
was introduced. Existing tests retain their assertions, with obsolete table
font/palette expectations replaced by the approved scoped data contract.

The consolidated [measurement index](../artifacts/data-view-finalisation/geometry/measurement-summary.json)
includes native sizes, actual thumbnail pixel ratios, header foregrounds,
font/ink metrics, interaction events, selection colours and the non-data CSS comparison.

## Validation

The full Meson suite and deterministic token/CSS checks are recorded in
`suite.log`; focused iteration logs are supplementary. **83/83 tests passed, with zero failures or skips**. The final header-colour
refinement additionally passed both native scale matrices, exact opaque
foreground checks, CSS parsing and real header interaction tests (`header-final.log`).
Deterministic generation/token checks pass, and parsed non-data declarations
match Git HEAD in all four entrypoints (`geometry/non-data-css.json`). Capture commands and integration examples
are in [the design specification](data-view-design.md) and `docs/testing.md`.

Real GNOME system text settings, fractional scaling, Wayland, high contrast and
screen-reader announcements require session acceptance beyond Xvfb/Openbox.
Enlarged native Pango text is tested, but is not claimed to exercise an OS
accessibility setting. GTK3 retains native renderer limitations rather than
adding a bespoke data-view framework. Thumbnail generation, caching, file
operations, editing and application drag-and-drop policies remain app-owned.

Final native state refresh: 54 cases passed in `states-final.log`. Final bound-text,
thumbnail-corner, enlarged-caption and input checks passed in `final-current.log`.
All review captures and the consolidated measurement index have been refreshed.


## Focus consistency follow-up — 27 October 2026

The Details-only broad focus-within rule has been removed after real-input
verification. All three GTK4 families now use native keyboard-visible focus,
including descendant focus on a continuous Details row. Metadata clipping was
not reproduced at the approved 12px/400; typography and geometry are unchanged.
See [focus states, Pango measurements and Files follow-up](data-view-focus-validation.md).
