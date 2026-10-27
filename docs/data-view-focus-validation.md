# Data-view focus and metadata validation — 27 October 2026

## Confirmed cause and change

Details had an extra `row:focus-within` inset shadow after the shared
`:focus-visible` rules. Real pointer selection sets FOCUS_WITHIN even when GTK
has not requested keyboard visibility. That rule therefore painted a Details
focus ring after a plain mouse click while Grid and standalone List did not.

Removed only that extra rule from `design/templates/gtk4-data.css.in` and
regenerated both GTK4 entrypoints. The shared `:focus-visible` rule already
covers the actual row, including a keyboard-focused descendant. Existing
`cell:focus-visible` resets prevent a second Details cell outline. The native
checkbutton retains its own small control affordance; it does not outline the
whole cell. No application focus-modality bookkeeping or CSS provider was added.

Selection colours, selected-hover/pressed colours, 14px/500 filenames,
12px/400 metadata, 12px/600 headers, 2px focus, radii, row/tile/artwork dimensions,
accessibility growth, transitions, separators, resizing and selection models
remain unchanged. No token, GTK3 theme, sidebar, document-tab, menu or window
control artwork changes were necessary.

## Native hierarchy and actual input

The GTK 4.18.6 / libadwaita 1.7.6 fixture reports these mapped node paths:

- Grid: `scrolledwindow/gridview/child/box/label`; native `child` owns state,
  its inner `.majoris-data-tile` paints the 8px-radius focus surface.
- List: `scrolledwindow/listview/row/box/label`; native `row` paints the
  4px-radius surface.
- Details: `scrolledwindow/columnview/listview/row/cell/box/label`; the internal
  ListView row paints one continuous surface across cells, with zero row radius.
- Descendant diagnostic: `row/cell/box/checkbutton/check` in Details,
  or `row/box/checkbutton/check` in List.

The tests use actual X11 mouse/key events under Xvfb/Openbox, not held focus
flags. Numeric masks: FOCUSED=32, SELECTED=4, FOCUS_VISIBLE=8192,
FOCUS_WITHIN=16384, DIR_LTR=128; PRELIGHT=2 can vary with pointer position.
Representative selected Details-row observations in the light 100% run:

| Interaction | Native row flags | Effective row ring |
|---|---:|---|
| Plain mouse selection | 16550 (includes PRELIGHT) | None |
| Down selects and focuses next item | 24740 | 2px indigo |
| Ctrl+Down moves focus away from selected item | selected row 132; focused row 24736 | Focused row only |
| Focus moved to toolbar, selection retained | 132 | None |
| Keyboard return via Tab | focused row 24736; selected row 132 | Focused row only |
| Ctrl-click multiselection | selected unfocused row 132; focused row 24740 | Native keyboard-visible row only |
| Shift-click range | selected rows 132; endpoint 24740 | Native keyboard-visible endpoint only |
| Another window activated | selected rows 132 | None; selection tint persists |
| Disabled view | selected row 140 | None; reduced contrast |
| Tab into child checkbutton | row 24708; child 24736 | Continuous row, no cell ring |

GTK propagates keyboard visibility to ancestors even when they are not themselves
FOCUSED. Modifier-key input can retain FOCUS_VISIBLE, so Ctrl/Shift selection
may retain a genuine keyboard indicator. It is not a ring caused by selection.
Do not override GTK visibility merely because the last selection used a mouse.
The native reports record this behaviour for every family, theme and scale.

The automated pixel checks verify the focus owner, accent colour at the inset
edge, absence of a thicker band, no duplicate cell ring, selection surfaces and
selected font weight. Tests also preserve selected identities through all three
view switches, verify keyboard return, multiple/range selection, and disable
misleading interaction feedback. Existing native state tests cover hover/pressed
and selected combinations; existing geometry tests cover both densities and
large accessibility text.

GTK3 keeps native TreeView/TreeSelection cursor and renderer focus. It has no
GTK4 FOCUS_VISIBLE state and does not promise identical pointer-modality rings.
Extended GTK3 tests verify mouse cursor placement, Home/Down/Shift selection,
selection retained while inactive and keyboard focus return at both scales.
No bespoke GTK3 renderer or navigation system was introduced.

## Metadata measurements: no clipping reproduced

The ColumnView metadata diagnostic displays all requested strings, without
ellipsizing the measured strings, in wider diagnostic columns. The default
fixture's column widths are unchanged. Both densities and themes were measured
at scale factors 1 and 2 using the installed Plus Jakarta Sans variable font:

`/home/administrator/.local/share/fonts/Majoris/PlusJakartaSans/PlusJakartaSans.ttf`

Fontconfig resolves `Plus Jakarta Sans | Regular`; Pango resolves
`Plus Jakarta Sans 9` (9pt = 12px at 96dpi). Effective CSS remains 12px/400.
Logical measurements below are in GTK logical pixels and remain the same at
100% and 200%; physical device pixels double at scale 2.

| Text | Ink rectangle x,y,w,h | Logical rectangle x,y,w,h |
|---|---|---|
| 18 bytes | 0,3,46,13 | 0,0,47,16 |
| ABCDEFGHIJKLMNOPQRSTUVWXYZ | 0,3,208,11 | 0,0,209,16 |
| gjpqy | 0,3,33,13 | 0,0,34,16 |
| 10/27/2026 02:41:48 AM | 0,3,139,11 | 0,0,140,16 |

The realised metadata label is 16px high, with layout offset (0,0) and layout
baseline approximately 12.4561px. The cell content allocation is 23px high;
complete rows remain 40px standard / 32px compact. An allocated baseline of -1
means the centered label was not assigned a baseline by the container. The
report records its actual layout baseline separately.

Every requested string's complete vertical ink fits the label and each row/cell
ancestor after applying the label position and layout offset. Capital glyphs
and descenders fit; no negative margins, translations, arbitrary baseline shifts,
extra row padding or typography changes were made.

The diagnostic records GTK Xft settings (normal requests: antialias=1,
hinting=1, hintmedium, 96dpi) and repeats with process-local legacy Xft requests
for hinting/antialiasing disabled. The captured raster output and measured
extents were identical in this GTK4 Cairo-renderer environment. This does not
establish a comparison of two independently confirmed rasterizer modes: legacy
Xft requests may be ignored by this stack. It does establish that those requests
do not reproduce clipping here. No conclusion about Majoris Files' renderer,
fontconfig configuration or the unknown original screenshot pipeline is inferred.

## Tests and evidence

Generation: `python3 tools/generate-theme.py` and `--check`.
Regression command: `meson test -C build --num-processes 4 --print-errorlogs`.
The six targeted focus/metadata/GTK3 tests passed at 100% and 200%.
The full suite passed all **87 tests**, with zero failures, skips or timeouts.
The regression outcome is recorded in `artifacts/data-focus-full-suite.log`.

`artifacts/data-view-focus/` contains genuine, unmodified native captures:

- `light/` and `dark/`: Grid/List/Details mouse-selected, keyboard-focused,
  selected+focused, keyboard-unselected, selected-unfocused, keyboard-return,
  multiple selection, Shift range, inactive-window and disabled captures.
- `details-keyboard-descendant.png` and `list-keyboard-descendant.png` show
  actual focus inside child controls.
- `details-metadata.png`, `details-metadata-compact.png` and
  `details-metadata-unhinted.png` show the text diagnostic.
- `light-2x/` and `dark-2x/` contain corresponding 200% captures.
- `geometry/focus-state-report.json` and `focus-state-report-2x.json` contain
  each interaction's mapped hierarchy, raw flags, explicit visibility/within
  booleans, selection identities, effective ring pixels and active-window state.
- `geometry/metadata-text-metrics.json` and `metadata-text-metrics-2x.json`
  contain ink/logical bounds, layout offsets, both baselines, label/cell/ancestor
  bounds and overflow, resolved fonts, Fontconfig file, scale and GTK Xft settings.

The existing data-view finalisation reports retain full standard/compact geometry
and GTK3 native evidence. Screenshot artifacts are gitignored local outputs;
the fixtures, tests and this explanation are tracked sources for reproduction.

## Remaining Majoris Files and desktop checks

No theme-owned glyph-clipping defect was reproduced. Majoris Files should log
its actual metadata widget's Pango ink/logical extents, layout offset and baseline;
confirm the resolved font file/face at 12px/400; inspect fixed widget heights,
line-height rules, renderer y-padding, ancestor overflow and snapshot clips;
and compare original-resolution captures before any resampling or compression.
A screenshot with uneven small-text edges alone does not demonstrate clipping.
Check font substitution, actual font-rendering options, text scaling, scale
factor and fractional transforms in the application/session.

Files should use the opt-in native families and avoid an application CSS override
that introduces broad focus-within rings or separate cell outlines. Real
GNOME/Mutter/Wayland, fractional scaling, portal-driven changes and end-to-end
screen-reader acceptance remain unverified. The supplied task described the
original screenshot but did not provide its pixels or exact runtime environment.
