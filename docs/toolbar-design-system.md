# Universal Majoris Toolbar Design Specification

`Majoris.Ui.Toolbar` is one GTK4 container for application-owned native controls.
It has the compositional role of WinForms ToolStrip, while using ordinary GTK
widgets, signals, GActions, ownership and size negotiation. File navigation,
formatting and playback are examples of content, not component types.

## Geometry and appearance

| Property | Standard | Compact |
| --- | --- | --- |
| Complete normal-text strip | 40px | 40px |
| Controls | 32px | 28px, vertically centred |
| Icon button | 32×32px | 28×28px |
| Symbolic artwork | 16×16px | 16×16px |
| Control radius | 4px | 4px |
| Outer padding | 4px vertical, 16px horizontal | Same |
| Within a group / between groups | 4px / 8px | Same |
| Major group separation | Optional 16px | Same |
| Icon-to-label gap | 8px | Same |
| Segmented container | 32px, radius 8px, inner segments 24px/radius 4px | Same |
| Bottom divider | Optional 1px painted inside allocation | Same |

The content minimum is 32px, plus 8px padding. Compact items occupy 28px inside
that same content area, giving 6px above/below. Large text can grow the strip.
Text buttons have natural widths. Border-box generation derives 30px/26px content
heights and 7px/5px icon padding from the canonical 32px/28px controls, accounting
for two 1px borders. Segmented padding is derived as 3px around a 24px segment
inside a 32px container with two 1px borders. These are calculations, not new
spacing tokens. A vertical separator has restrained 4px content insets.

| Colour | Light | Dark |
| --- | --- | --- |
| Universal surface | #FFFFFF | #202023 |
| Divider | #E5E5E9 | #313136 |
| Text | #1C1C1F | #F4F4F5 |
| Secondary text | #626269 | #A9A9B0 |
| Focus | #6366F1 | #818CF8 |
| Segmented surface | #F2F2F4 | #242428 |
| Selected segment | #FFFFFF | #35353A |

Raised items retain existing Majoris backgrounds, borders and subtle control
shadows. Flat items are transparent without default elevation, with neutral hover
and pressed feedback and persistent checked treatment. Both may share one strip.
A 2px indigo focus outline identifies focus independently of selection. Disabled
and backdrop states retain the existing semantics. Transitions remain 128ms and
stationary: no scaling, translation, resizing or baseline movement. Existing GTK
reduced-motion handling applies; applications should honour GTK settings.

Typography uses Plus Jakarta Sans: action labels 14px/600, menus, selectors and
secondary labels 14px/500, metadata 12px/400. Real fonts and natural Pango layout
supply ascent and descent; no text offsets or synthetic boldening are used.

## Install and consume

The Meson build installs `libmajoris-ui-gtk4.so` (SONAME 0),
`majoris-ui-gtk4.h`, `majoris-ui-gtk4.vapi`, its GTK4 `.deps`, and
`majoris-ui-gtk4.pc`. The core links GTK4 only, independently of the factory,
libadwaita and both existing theme bridges. Header/VAPI are the public APIs;
no GIR is provided. Use the normal Meson prefix and library search paths:

```sh
meson setup build --prefix=/usr
meson compile -C build
# Stage/review a package without installing onto the running system:
DESTDIR="$PWD/artifacts/package-stage" meson install -C build
```

Consumer `meson.build`:

```meson
project('toolbar-example', 'vala', 'c')
ui = dependency('majoris-ui-gtk4')
executable('toolbar-example', 'main.vala', dependencies: ui)
```

A nonstandard prefix needs its `lib/pkgconfig` (or multiarch equivalent) in
`PKG_CONFIG_PATH`, `share/vala/vapi` in valac's VAPI search path, and its library
directory in the runtime loader search path. Library installation does not activate
the theme or replace `libmajoris-gtk4-theme` / `libmajoris-gtk3-theme`.
The user-local theme symlink installer is distinct from library/package installation.
Without Majoris CSS the class remains a functional native GtkBox with ordinary
GTK controls; the exact Majoris dimensions and spacing require the theme.

## Public API and ownership

- `append_control`, `prepend_control`, `insert_control(widget, position)` designate
  only the supplied control and centre it; positions are zero-based, past-end appends.
- `remove_control` unparents an item; callers can retain/reuse it and its callbacks.
- `move_control(widget, position)` reorders an existing direct child.
- `append_widget` inserts an arbitrary native composite without traversing or styling
  its internals. Ordinary GtkBox methods remain available.
- `append_group()` returns `ToolbarGroup`; its `append_control`, `append_widget`
  and `remove_control` support arbitrary child counts. Empty groups hide themselves.
- `append_separator()` and `append_spacer()` return native widgets. The spacer uses
  `hexpand`, never fixed margins. API mutations suppress leading/trailing/redundant
  separators. Use the component/group methods for automatic cleanup; direct GtkBox
  mutation or hiding arbitrary children leaves visibility policy with the application.
- `compact` selects density; `divider` selects the inset bottom stripe.
- `Toolbar.set_item_flat(widget, bool)` switches an individual item's treatment.

Button/MenuButton, Entry/SearchEntry and DropDown controls receive only their
explicit toolbar classes. Custom progress bars, spinners, scales and supporting
labels use ordinary GTK layout; label metadata can opt into
`majoris-toolbar-metadata`. Icon-only buttons are detected. For custom icon-and-text
button children, use a horizontal box with an 8px gap and mark the button
`majoris-toolbar-action`; set image pixel size 16. Set accessible labels on icon-only
controls. Removing widgets follows GTK reference ownership; it does not disconnect
application signals or undo intentionally applied item classes.

## Vala examples

These snippets are placed inside a normal Gtk.Application activation handler.
All three use the same class. The application supplies window/content parenting.

Files-style composition:

```vala
var toolbar = new Majoris.Ui.Toolbar();
toolbar.divider = true;
var history = toolbar.append_group();
var back = new Gtk.Button.from_icon_name("go-previous-symbolic");
history.append_control(back);
history.append_control(new Gtk.Button.from_icon_name("go-next-symbolic"));
toolbar.append_separator();
// Substitute an application's existing breadcrumb composite unchanged here.
var location = new Gtk.Entry();
location.hexpand = true;
toolbar.append_control(location);
var search = new Gtk.SearchEntry();
toolbar.append_control(search);
back.clicked.connect(() => { /* application navigation */ });
```

Notepad-style formatting:

```vala
var toolbar = new Majoris.Ui.Toolbar();
toolbar.compact = true;
var formatting = toolbar.append_group();
foreach (var name in new string[] {"Bold", "Italic", "Underline"}) {
    var item = new Gtk.ToggleButton.with_label(name);
    Majoris.Ui.Toolbar.set_item_flat(item);
    formatting.append_control(item);
}
var alignment = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
alignment.add_css_class("majoris-toolbar-segmented");
alignment.valign = Gtk.Align.CENTER;
var left = new Gtk.ToggleButton.with_label("Left");
var right = new Gtk.ToggleButton.with_label("Right");
right.group = left;
left.active = true;
alignment.append(left);
alignment.append(right);
toolbar.append_widget(alignment);
```

Media-player composition:

```vala
var toolbar = new Majoris.Ui.Toolbar();
toolbar.append_control(new Gtk.Button.from_icon_name("media-playback-start-symbolic"));
toolbar.append_control(new Gtk.Button.from_icon_name("media-playback-pause-symbolic"));
var progress = new Gtk.ProgressBar();
progress.valign = Gtk.Align.CENTER;
progress.hexpand = true;
toolbar.append_widget(progress);
var time = new Gtk.Label("01:24 / 04:00");
time.add_css_class("majoris-toolbar-metadata");
toolbar.append_widget(time);
var mode = new Gtk.DropDown.from_strings({"Normal", "Repeat", "Shuffle"});
toolbar.append_control(mode);
```

The native factory adds volume, a spinner, native menu models, actual Majoris
LocationBar, search, and a dynamic Extra action toggle that inserts/removes Queue.
The editor example combines compact flat buttons with generic text segments;
the file example has icon-only segments. Icon-and-text segments can use ordinary
GtkBox children with spacing 8 and GtkImage pixel_size 16. Group native toggles with
`group`; the theme does not emulate selection or dispatch application events.

## CSS composition and isolation

`.majoris-toolbar` is the sole canonical container. Optional modifiers are
`.majoris-toolbar-compact`, `.majoris-toolbar-divider`, and
`.majoris-toolbar-major-groups` (16px instead of 8px between direct children).
Direct children are separated by 8px; group children by 4px. GTK4 uses CSS
`border-spacing` with native box spacing 0, avoiding duplicate padding/gaps.
Group, separator, spacer, control, icon, action, menu, field, select, metadata,
item-flat and segmented classes are reusable building blocks. An explicitly
designated `majoris-toolbar-scale` fits a native volume slider into the strip;
turn off its value label or allow extra height when that label is needed.

Only explicitly marked controls receive toolbar sizes. There is no broad
`.majoris-toolbar button` rule. Do not apply control classes to location crumbs,
menu rows or other composite internals. Use `append_widget(location_bar)` to retain
its 32px shell, 26px crumbs/entry and existing radius exceptions. Native menu/popover
contents retain normal Majoris menu typography and row sizing.

## Responsive behaviour, focus and accessibility

The container supplies no application-specific overflow policy. A caller may hide
secondary actions, compose overflow menus or wrap the strip in a GtkScrolledWindow:

```vala
var scroll = new Gtk.ScrolledWindow();
scroll.hscrollbar_policy = Gtk.PolicyType.EXTERNAL;
scroll.vscrollbar_policy = Gtk.PolicyType.NEVER;
scroll.propagate_natural_height = true;
scroll.child = toolbar;
```

EXTERNAL supports native focus scrolling without an extra visible scrollbar.
The factory demonstrates a real 480px window. Standard controls retain dimensions;
flexible location/search space and scrolling cooperate. Native keyboard focus and
exclusive toggles handle tab/arrow/Space navigation. Applications supply shortcut
controllers, accessible names, callbacks and actions. The factory uses Ctrl+L /
Alt+D for its location component and Ctrl+F for search. Enlarged fonts may increase
strip height; do not impose a maximum or clip content to maintain 40px.

## Compatibility and GTK3

| Previous usage | New application usage | Compatibility |
| --- | --- | --- |
| Navigation / Command classes and different surfaces | `Toolbar()` with neutral surface | Old classes alias common strip geometry/surface; no purpose colours |
| Independent editor toolbar | `Toolbar { compact = true }` plus flat items | Legacy editor CSS retains its exact 28px flat appearance |
| `majoris-toolbar-view-switcher` | `majoris-toolbar-segmented` | Both names share one CSS implementation |

Existing applications need not migrate immediately. The legacy editor rules remain
in the editor generator; they are compatibility styling, not a new public widget
type. New application APIs contain no NavigationToolbar, CommandToolbar or
EditorToolbar. Migration changes construction and opt-in item classes, not actions.

GTK3 receives equivalent opt-in CSS for standard/compact controls, flat items,
groups and segmented aliases. There is no GTK3 wrapper library. Compose native
GtkBox rows with spacing 8, groups with spacing 4 and segmented boxes with spacing 2;
CSS border-spacing is omitted because GTK3 does not implement it. Centre controls
with `valign`, set native GtkImage pixel size 16, use GtkRadioButton with indicator
mode off for exclusive segments, GtkComboBoxText with `majoris-toolbar-select`
instead of GtkDropDown, and native `hexpand` spacers. GTK3 scrolled boxes should
receive the scroller's focus horizontal adjustment. Location composition stays
application-owned; do not compile the GTK4 subclass against GTK3.

## Sources and evidence

Canonical light/dark HTML supplies shared border-box tokens. `generate_toolbar.py`
derives standard/compact dimensions; `gtk-toolbar.css.in` is included by the normal
light/dark GTK3/4 generator. Regenerate with extract-design-tokens.py and
generate-theme.py; verify with verify-design-tokens.py and generate-theme.py --check.

See [implementation report](toolbar-implementation-report.md) and native evidence
in [artifacts/universal-toolbar](../artifacts/universal-toolbar/README.md).
