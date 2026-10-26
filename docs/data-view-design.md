# Majoris Data View Design Specification

Grid, List and Details are three presentations of native GTK data models.
Details means `Gtk.ColumnView`, not multi-pane column navigation. All families
are application opt-ins: installing the theme supplies presentation and does
not implement a file manager, sorting policy or thumbnail service.

## Integration classes

| GTK4 widget | Class | Compatibility |
|---|---|---|
| Gtk.GridView | `majoris-data-grid` | Native child owns state; inner `majoris-data-tile` paints |
| Gtk.ListView | `majoris-data-list` | Only direct rows receive standalone list padding |
| Gtk.ColumnView | `majoris-data-column` | Existing `majoris-data-view` remains an equivalent alias |
| Any of these | `majoris-density-compact` | Explicit density; independent of window width |
| Standalone ListView | `majoris-data-separators` | Optional 1px row dividers |
| Data view | `majoris-data-boxed` | Optional 1px structural border and 8px corners |
| Inner item Box | `majoris-data-cell` | Composition and inherited colour |
| Grid inner Box | `majoris-data-tile` | Fixed target, naturally grows for larger text |
| Artwork container | `majoris-data-artwork` | Stable image/placeholder allocation |
| Gtk.Picture | `majoris-data-thumbnail` | 4px corner treatment; aspect-preserving picture |
| Metadata Label | `majoris-data-metadata` | Secondary 12px/400 text |

GTK3 TreeView supports `majoris-data-view` for details and
`majoris-data-list` for lists; IconView supports `majoris-data-grid`.
The old broad descendant row rules have been replaced by native-widget-scoped
aliases. Preference rows, boxed preference lists, sidebars, menu rows and tabs
receive none of the new data-view rules. A ColumnView's internal ListView does
not acquire the standalone-list class or a second padding/background layer.

## Typography and geometry

Plus Jakarta Sans primary labels use **14px/500 in every state**, including
selection. Metadata uses 12px/400. Header labels use 12px/600 in title case.
No selection stripe, weight increase or independent filename rectangle is used.

| Measurement in logical px | Standard | Compact |
|---|---:|---:|
| Complete List row | 40 | 32 |
| List horizontal / vertical inset | 16 / 8 | 8 / 4 |
| Complete Details row | 40 | 32 |
| Details cell horizontal / vertical inset | 16 / 8 | 8 / 4 |
| Complete Details header | 32 | 32 |
| Header horizontal / vertical inset | 16 / 4 | 8 / 4 |
| List/Details icon and gap | 16×16 / 8 | 16×16 / 8 |
| Grid tile target | 128×160 | 96×128 |
| Grid artwork target | 96×96 | 64×64 |
| Typical file icon | 64 | 32 |
| Tile internal inset / artwork-label gap | 8 / 8 | 8 / 8 |
| Grid minimum horizontal/vertical gap | 16 | 8 |
| Grid outer inset target | 16 | 8 |
| Grid filename | At most two natural Pango lines | Same |

List rows have no gap and a 4px radius. Details rows have zero radius and a
continuous selection surface across all cells. Details row separators are 1px;
body column separators follow `show_column_separators`, while header separators
remain subtle. Grid tiles have 8px corners. Items have no decorative border or
shadow. An optional boxed view adds its own structural border outside these
item measurements; set its widget overflow to hidden to clip structural corners.

These are complete allocations, not content minima. `generate_data.py` derives
GTK content minima from the canonical HTML: List uses 24px content plus 16px/8px
vertical padding; Details uses 23px/23px content plus padding and one row hairline;
headers use 23px content plus 8px padding and a parent-owned 1px line. The toolkit
may grow these sizes for larger text. It must not clip text to enforce a target.

## Grid layout and thumbnails

GTK GridView owns columns, recycling, navigation and scrolling. The fixture uses
`min_columns=1`, `max_columns=12`; GTK chooses the actual column count from the
available width. It does not manually position tiles. Native outer cells may
receive surplus horizontal space. A centred inner tile retains the 128px/96px
content target, so artwork never stretches to fill that surplus. Measurement
reports distinguish `owner` (native cell) from `bounds` (painted inner tile).
Visible tile gaps can exceed the minimum when native cells distribute surplus.
Incomplete final rows keep GTK's column alignment.

GTK4 expresses half the gap as each native child's margin and subtracts that
half-gap from root padding, yielding the intended minimum outer inset. Inner
artwork does not expand vertically: otherwise one-line filenames would shift
artwork relative to two-line filenames. Filename height reserves two lines measured by Pango with the current font
and native text attributes, never an estimated character-height constant.
This keeps artwork top-aligned when short and long names share an enlarged-text
row, while permitting the native tile and row to grow. Labels wrap/ellipsise naturally, stay
centred and retain the full filename for accessibility and tooltips.

`Gtk.Picture.content_fit=CONTAIN` preserves landscape, portrait and square image
ratios. A native AspectFrame allocates the Picture itself to the fitted rectangle,
so its 4px corners clip the visible thumbnail, including letterboxed images,
rather than only the square artwork slot. A stable artwork allocation contains either a centred icon or a picture;
loading, missing and replaced thumbnails do not alter tile bounds or text
position. The fixture's three local SVG images are representative thumbnails,
not modifications to the symbolic icon artwork. A single delivery timer changes
a record property; each bound grid cell observes that property and disconnects
its handler on unbind. No thumbnail generator/cache is part of the theme.
Source execution finds assets under `factory/data/thumbnails`; installation
places them under `share/majoris-theme/thumbnails`. Applications can set
`MAJORIS_DATA_ASSET_ROOT` for this gallery fixture.

## Shared colours and states

| Role | Light | Dark |
|---|---|---|
| Surface | #FFFFFF | #202023 |
| Primary / secondary text | #1C1C1F / #626269 | #F4F4F5 / #A9A9B0 |
| Hover / pressed | #ECECEF / #E2E2E6 | #303035 / #38383D |
| Selected surface | #EEF2FF | rgba(99,102,241,.16) |
| Selected text | #3730A3 | #E0E7FF |
| Selected hover / pressed | #E0E7FF / #C7D2FE | Indigo alpha .22 / .28 |
| Focus | #6366F1 | #818CF8 |
| Separator | #E5E5E9 | #313136 |
| Header | #F2F2F4 | #28282C |

These roles are extracted from `.data-views` in both canonical HTML references
and emitted as shared `@majoris_data_*` colours. Each family consumes the same
roles. Default items are transparent. Hover/pressed feedback is neutral unless
selected; selected combinations retain a stronger indigo tint. Focus is a
separate 2px inset treatment and can appear on an unselected item. Details cell
focus is represented once on its containing row via native focus-within state.
Disabled items reduce emphasis and suppress hover/pressed surfaces. Backdrop
retains the selected surface and reduces text emphasis.

Only stationary colour and shadow/focus transitions run, for 128ms with
`cubic-bezier(.2,0,0,1)`. GTK animation settings disable transitions. No dimensions,
position, font weights or baselines animate. Header buttons have default, hover,
pressed, focus and disabled-sort treatments; native sort indicators retain a
16px symbolic content and width without growing the 32px header. GTK may
allocate the indicator a taller slot within the 23px header content area; the
native report distinguishes that slot from its symbolic content.

## Native model and interaction example

```vala
var sorted = new Gtk.SortListModel(records, null);
var selected = new Gtk.MultiSelection(sorted);
var list = new Gtk.ListView(selected, list_factory);
list.add_css_class("majoris-data-list");
var grid = new Gtk.GridView(selected, grid_factory);
grid.add_css_class("majoris-data-grid");
grid.min_columns = 1;
grid.max_columns = 12;
var details = new Gtk.ColumnView(selected);
details.add_css_class("majoris-data-column");
details.show_row_separators = true;
details.show_column_separators = false;
// Density belongs on the opted-in root, never its internal list.
details.add_css_class("majoris-density-compact");
var name = new Gtk.ColumnViewColumn("Name", name_factory);
name.fixed_width = 192; // application default, not a theme constraint
name.expand = true;
name.resizable = true;
name.sorter = name_sorter;
details.append_column(name);
sorted.sorter = details.sorter;
```

`DataCell` and `DataViewsFixture` in `factory/src/data-views.vala` are working
composition examples. List/Name cells use a horizontal Box with spacing 8,
centred 16px icon and a flexible, start-aligned ellipsising Label. Grid cells use
a vertical Box with spacing 8, artwork and a two-line Label. No appearance CSS
provider is installed by these components; they use the generated theme.

The fixture supplies native SingleSelection/MultiSelection controls, a shared
sorted model, segmented Grid/List/Details switching and standard/compact toggles.
Only the active view binds the shared model, avoiding hidden-view widget pools.
Factories implement setup/bind/unbind; unbind clears labels, images, record
references and thumbnail notifications. The stress fixture contains 1,200 items
and still uses these native recycled factories.

Name, modification date, type and numeric size have real GTK sorters. The
application snapshots selected record identities before sorter changes and
restores them through the native selection model after reordering. Switching
presentation/density likewise preserves identity. This is application behaviour,
not CSS. Columns start at 192/160/128/96px, with Name expanding. Native resize
handles own later widths; no tick callback reconciles them continuously.

## GTK3 differences

GTK3 retains native TreeView/TreeSelection and IconView cell renderers.
Its focused `.view` selection selectors explicitly override native Adwaita
focus specificity. GTK3 renderer selection is precomposited over the approved
data surface: its native painter can otherwise composite translucent selection
over the window surface instead. This preserves the intended light/dark colours.
Symbolic preview pixbufs are loaded using the view style context so dark icons
retain proper contrast. Renderer
vertical padding is application-owned (8px/4px). GTK3 TreeView style properties
account for native grid/focus spacing: 4px vertical separation with horizontal
grid lines, 5px without them, and horizontal separation 32px/16px. The tested
complete detail/list rows are 40px/32px and headers 32px. Native icons use a 16px
renderer and an 8px column spacing. Renderer font metrics and native sorting are
validated; selection remains owned by TreeSelection.

GTK3 IconView uses native item width, padding, spacing and cell renderers with
96px/64px artwork regions and 64px/32px rendered icons. Native renderer wrapping
and item heights are less expressive than GTK4's two-line Gtk.Label composition;
exact GTK4 tile-height and two-line truncation parity are not claimed for GTK3.
No custom GTK3 drawing framework is introduced. Thumbnail generation and richer
per-record presentation remain application responsibilities.

## Validation and limits

Run `meson test -C build --num-processes 4 --print-errorlogs`. The added tests
cover canonical/scoped contracts; GTK3/GTK4 at 100% and 200%; realised item/header
allocations; primary/header Pango metrics; selected weight/baseline stability;
landscape/portrait/square pixel aspect ratios; async replacement without movement;
all interaction states; and native pointer/keyboard sorting, resizing, modifier
selection, select-all, activation, mode switching, scrolling and recycling.
Native relative coordinates account for window decoration insets.

`MAJORIS_DATA_REPORT=/path/report.json` records cells, artwork, labels, Pango ink,
logical extents, baselines, accessible instance roles, native owner allocations,
selection, sort order, resize widths and factory counters. Diagnostic state
captures hold real GTK state flags; they are distinct from the actual input
interaction test. Backdrop tests activate a separate native window.

Enlarged-text fixtures use native Pango attributes, preserving growth instead of
clipping. Absolute CSS pixel fonts do not necessarily follow legacy Xft DPI;
real GNOME system text scaling, fractional scaling, Wayland/Mutter, high contrast,
screen-reader announcements and third-party integration remain session acceptance
checks. Accessible names/roles are preserved in native widgets and instance-role
reports; this is not an end-to-end screen-reader certification. See the
[finalisation report](data-view-finalisation.md) for evidence and before/after values.
