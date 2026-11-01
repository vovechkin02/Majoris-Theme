# Layout spacing standard

Majoris owns the 0/4/8/16/32 logical-pixel scale. The HTML reference defines
`--spacing-none`, `--spacing-compact`, `--spacing-standard`, `--spacing-section`,
and `--spacing-major`. `tools/design.py` extracts the `spacing` token map;
both generators consume that same geometry. Colours do not change spacing.

| Relationship | Owner | Target |
|---|---|---:|
| Deliberately connected elements | Connected container | 0 |
| Label/input or progress bar/supporting text | Field/detail container | 4 |
| Independent controls, search/results, related actions | Content container | 8 |
| Functional groups and content/footer | Section container | 16 |
| Major page divisions | Page section container | 32 |

Control padding remains owned by the control. Sibling spacing belongs to the
parent layout. Container insets are separate from gaps. Never place margins on
both adjacent controls to implement a gap already owned by their parent.

## Native inheritance and selector ledger

Runtime inspection used GTK 4.18.6 and libadwaita 1.7.6. The native tests dump
CSS names, classes, parent hierarchy, visibility, explicit Box spacing and child
allocations. The factory's Layout & Spacing page also offers a gap inspector.

| Selector | Expected hierarchy and scope | Exclusions | Gap / property conflict |
|---|---|---|---|
| `preferencesgroup > box > box:not(.header)` | PreferencesGroup / outer vertical box / content vertical box | Header, heading labels, ActionRow internals | 8; internal Box spacing is 0 |
| Existing `preferencesgroup > box` | Group outer box, heading/content | Row interiors | Existing 8 |
| Existing `preferencespage > scrolledwindow > viewport > clamp > box` | Page group holder | Other scrolled content | Existing 16 |
| `window.dialog > box.dialog-vbox` | Gtk.Dialog native content/action wrapper | Adw.Dialog adaptive sheets | 16; Box property is additive |
| `window.dialog > box.dialog-vbox > box.dialog-action-box > box.dialog-action-area` | Gtk.Dialog native actions | Arbitrary horizontal boxes | 8; Box property is additive |
| `actionbar > revealer > box > box.start/end` | Gtk.ActionBar CenterBox start/end containers | Headerbar, toolbar, center widget internals | 8; native internal Box spacing is 0 |
| `box.majoris-*` | Explicitly marked application container | Unmarked boxes and widget interiors | See semantic table; property spacing must be 0 |
| `grid.majoris-form-layout` | Explicit form Grid | Internal structural grids | 8 in both axes; use zero row/column properties |
| Neutral FlowBox | Native row-spacing / column-spacing properties | Selectable item geometry unchanged | CSS border-spacing does not supply gaps in GTK 4.18.6; use native properties |

The PreferencesGroup content box contains its internal continuous boxed-list,
then arbitrary widgets added through `add()`. Spacing surrounds that list;
its rows keep their separators, radii, padding and heights. GTK omits hidden
children from layout. Revealing or inserting a child introduces one new gap.
A visible empty Box still participates in GTK layout and can therefore reserve
two adjacent parent gaps even with zero height. Hide or remove an empty
placeholder to omit it; the native tests demonstrate both states.
The supplied Files Tags and Manage Tags relevant hierarchies are reproduced in
native tests, with no Files CSS or source changes.

## Semantic classes for ambiguous layouts

Construct semantic Gtk.Box containers with `spacing: 0`.

| Class | Meaning |
|---|---|
| `majoris-control-stack` | 8px independent controls, vertical or horizontal |
| `majoris-action-group` | 8px related buttons |
| `majoris-compact-stack`, `majoris-field` | 4px compact controls or label/input |
| `majoris-section-stack`, `majoris-progress-list` | 16px sections or separate progress items |
| `majoris-major-stack` | 32px major page sections |
| `majoris-connected-group` | 0px connected composition |
| `majoris-form-layout` | 8px fields; nest a `majoris-field` box for each label/input pair |
| `majoris-dialog-content` | 8px content rhythm and 16px insets, opt-in only |
| `majoris-footer-layout` | 16px between body and distinct footer |
| `majoris-action-footer` | 8px between footer actions; parent owns body/footer separation |
| `majoris-progress-content` | 8px title, detail and actions |
| `majoris-progress-detail` | 4px progress bar/supporting text |

Do not combine conflicting gap classes on a single container. Compose nested
containers with separate ownership instead. Footer classes do not put a margin
on each child. A footer inside a PreferencesGroup is an ordinary independent
child (8px); for a distinct 16px footer, put body and footer in a
`majoris-footer-layout` parent rather than accumulating another margin.

```vala
var group = new Adw.PreferencesGroup();
group.add(new Gtk.SearchEntry());
group.add(results);  // automatic 8px, no class required
var actions = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
actions.add_css_class("majoris-action-group");
actions.append(new Gtk.Button.with_label("Apply"));
actions.append(new Gtk.Button.with_label("Reset"));
group.add(actions);  // 8px outside, independently 8px inside

var form = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
form.add_css_class("majoris-form-layout");
var field = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
field.add_css_class("majoris-field");
field.append(new Gtk.Label("Name"));
field.append(new Gtk.Entry());
form.append(field);
```

SearchEntry internals, SearchBar reveal geometry, ActionRow titles/subtitles,
toolbars, breadcrumbs, menus, sidebars and data views retain their established
rules. No global box, label, entry, button or ProgressBar margin is introduced.
Native FlowBox does not consume CSS border-spacing in GTK 4.18.6: measurements
with an 8px CSS declaration still produced a 0px child-allocation gap. Use its
row-spacing and column-spacing properties (8 standard, 4 compact) where intended.
The neutral factory example retains native default geometry.
Expander content can opt into the same container contract; the expander itself
retains native geometry. Neutral FlowBox remains neutral.

## Popovers, dialogs and progress

Popover outer contents retain their existing 8px inset. A direct anonymous
popover box may be a compact palette, an explicitly spaced form or connected
controls. CSS cannot inspect its spacing property. Mark a zero-spacing content
box `majoris-control-stack` for ordinary composition; menu and dropdown result
lists are excluded. Native menus keep row geometry and keyboard handling.

Adw.PreferencesDialog inherits page/group spacing. Adw.AlertDialog and
Gtk.AlertDialog retain their built-in message/response layouts. Adw.Dialog,
NavigationPage and ToolbarView do not identify the semantics of arbitrary
application content; their adaptive outer geometry is preserved. A normal
Gtk.Dialog has identifiable action containers, covered by scoped defaults.
Explicit application Box spacing there is additive and must be zero when
inheriting theme spacing, or the application must override CSS spacing to zero.

ProgressBar does not identify a progress presentation by itself. Nest title,
`majoris-progress-detail` (bar and supporting text), and actions inside a
`majoris-progress-content` box. Use `majoris-progress-list` around separate items.
Files' unmarked 6px progress stack is intentionally left unchanged until it
adopts semantic intent; the Theme cannot safely infer its role.

## Exact GTK limitations and application overrides

Native measurements establish that **Gtk.Box.spacing and CSS border-spacing
add**, rather than replace or take the maximum. A semantic 8px box with explicit
6/8/12px spacing produces 14/16/20px. Child margins also add: a 3px top margin
plus an 8px parent gap yields 11px. CSS cannot match a GObject property value,
so a theme cannot automatically preserve every explicit application gap while
also supplying a default to indistinguishable anonymous boxes. No runtime
mutation hooks are installed to work around that limitation.

Use spacing=0 for Theme-owned semantic containers. For intentional app geometry,
leave anonymous layouts alone, or override `border-spacing: 0` on a recognised
native layout when assigning explicit property spacing. For connected groups,
zero the property as well as CSS spacing. Existing `.linked` has zero CSS gap.
Do not apply semantic classes to a boxed-list itself to separate its rows.

The GTK4 bridge retains its existing USER + 1 priority (801), necessary to
switch variants when a legacy user gtk.css imports the light stylesheet at
USER priority. An intentional application override must therefore register its
provider at `GTK_STYLE_PROVIDER_PRIORITY_USER + 2` (802). APPLICATION priority
(600) cannot override this system integration. Native override tests exercise
802 without `!important`; no provider-precedence change is introduced:

```css
/* Application provider at GTK_STYLE_PROVIDER_PRIORITY_USER + 2 */
box.my-compact-form { border-spacing: 4px; }
preferencesgroup.my-special-group > box > box:not(.header) { border-spacing: 0; }
```

## GTK3 compatibility

GTK3 Box and Grid do not implement sibling layout through CSS border-spacing.
Copying the GTK4 selectors would produce ineffective claims. Native dialog
spacing, action areas, popover/menu and boxed-list contracts remain unchanged.
`majoris-dialog-content` supplies a supported 16px inset. For GTK3 sibling gaps,
use native Box spacing / Grid row-spacing and column-spacing properties using
the canonical scale. GTK3 has no libadwaita PreferencesGroup equivalent. This is
a documented CSS limitation, not a custom layout framework or runtime hook.

## Verification and evidence

Run the repository generator, `--check`, Meson compile and Meson tests.
`tests/test-spacing-native.py` records allocated boundaries, actual horizontal
and vertical gaps, explicit spacing, margins, padding, borders and hierarchies.
It tests light/dark, RTL, narrow/wide widths, 200% scaling and enlarged fonts,
hidden/revealed/dynamically inserted/removed children, connected controls,
continuous rows, page groups, native actionbars, progress/footer composition,
and application overrides. Screenshots are genuine X11 GTK captures of
Files-derived native fixtures, not the Files executable. Before screenshots
remove only the new group rule above the bridge provider for a controlled comparison.
See `artifacts/layout-spacing/summary.md` and the Files inventory for results.
