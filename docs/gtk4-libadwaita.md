# GTK4/libadwaita

GTK theme settings alone are insufficient for libadwaita. Explicit light/dark development installation symlinks the selected gtk.css, gtk-dark.css and both colour files into the normal user override directory; relative imports resolve beside the symlink path. Existing files are journaled and backed up. No application appearance stylesheet masks theme failures.

The gallery uses Trixie's libadwaita 1.7 widgets including AlertDialog, SwitchRow and SpinRow. Deprecated but available ColorButton and FontButton intentionally exercise native legacy controls. CSS parsing and simple/dense border-box geometry are tested.
Native spinner vectors live in gtk-4.0/assets and are linked alongside user CSS. Re-running the installer adds new asset/font links while preserving existing backups. The real-node mappings include dialog.alert/floating-sheet and banner/revealer/widget; stock toolkit image backgrounds, preference subtitle opacity and nested menu-button styling require explicit cascade resets.

The factory contains two focus descriptions for titlebar buttons. Its generic
focus selector gives a coloured inner border, but its later explicit
state-verification example reserves a transparent border and shows an external
halo. Majoris follows that explicit example in both toolkits: a transparent 1px
reserved border, unchanged 32x32 plate and external 2px halo. Light uses
rgba(99,102,241,.24); dark uses rgba(129,140,248,.36). No regular control shadow
is added. The supplied HTML has not been changed.

Floating GTK4 CSD windows receive the authority's 1px outer edge, 8px radius and
window shadow on window.csd. GTK3 owns the corresponding decoration node.
Managed maximized/fullscreen/tiled and directional tiled GTK classes remove the
outer border allocation, shadow and radius. Actual maximize/fullscreen are
exercised with Openbox; tiled classes are diagnostic equivalents under X11.
Mutter/Wayland tiling, fractional scaling and compositor shadows require GNOME
VM acceptance. The outer edge reserves 1px on each side, without increasing the
internal 48px header allocation or the 32px controls and 16px glyphs.


Development `--variant=auto` backs up the existing gtk.css through the same
journal and links a neutral comment-only file. It imports neither light nor
dark CSS. Use the factory or `scripts/with-majoris-gtk4.sh PROGRAM` to attach the
unchanged StyleManager bridge. Auto installation alone does not globally attach
libraries to arbitrary applications. Changing light/dark/auto modes retains the
original backup; uninstall restores original files or symlinks and rejects later
user edits. Both explicit modes still select their fixed user CSS entrypoints.

The shared generated `desktopwindow` exception is emitted after native overrides
so active/backdrop desktop windows remain transparent, square, borderless and
shadowless. Native GTK3/4 style-render probes verify zero alpha without changing
normal application styling. Actual DING focus/wallpaper lifecycle is a GNOME VM
check, not a claim from those native probes.

This theme provides CSS and the GTK3/GTK4 bridges. The OS/session provides global
attachment/dispatcher policy, Shell extension activation, wallpaper and Mutter
lifecycle. No session-wide LD_PRELOAD or `/etc/environment` policy is installed
here. See [VM validation](theme-state-vm-checklist.md).

## Shared layout contract

Use opt-in classes on ordinary GTK containers. A `.card` owns the surface,
1px border, 8px radius and elevation. Its optional `majoris-card-header` owns
its existing header inset and bottom divider. `majoris-card-body` owns 16px
padding; `majoris-card-footer` owns 12px vertical / 16px horizontal padding
and a top `@border_soft` divider. Only append a footer when there is content.
Body and footer add no independent surface, radius or shadow. Body-only cards
are supported. Never also set 16px margins on the body container.

```vala
var card = new Gtk.Box (Gtk.Orientation.VERTICAL, 0);
card.add_css_class ("card");
var body = new Gtk.Box (Gtk.Orientation.VERTICAL, 8);
body.add_css_class ("majoris-card-body");
body.append (new Gtk.Button.with_label ("Start"));
card.append (body);
var footer = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 4);
footer.add_css_class ("majoris-card-footer");
footer.append (new Gtk.Button.with_label ("Cancel"));
card.append (footer);
var page = new Gtk.Box (Gtk.Orientation.VERTICAL, 16);
page.add_css_class ("majoris-page-content");
page.append (card);
var clamp = new Adw.Clamp ();
clamp.child = page;
var scroll = new Gtk.ScrolledWindow ();
scroll.child = clamp;
```

The inner page owns 24px gutters. Add `majoris-compact` to that same container
for 16px gutters; remove it to restore desktop spacing. An application's
`Adw.Breakpoint.apply` / `unapply` handlers (or equivalent allocation logic)
should toggle the class at its chosen available-width threshold. The factory
uses available page width below 650px and also changes its gallery to one
column. Do not add scroll padding or duplicate page margins. Edge-to-edge
content can omit the class. These classes never globally pad boxes or pages.

Native composition owns spacing: 16px between sections/cards, 8px between form
rows and icon/text pairs, 4px between compact adjacent controls. Use Box.spacing
or Grid.row_spacing/column_spacing; CSS padding defines component boundaries.

Prefer a genuine Adw.PreferencesGroup for preferences, including its native
heading, description and internal boxed list. A Gtk.ListBox with `boxed-list`
is appropriate for an explicitly composed group. Keep native ActionRow,
SwitchRow, ComboRow, EntryRow, PasswordEntryRow, SpinRow and ExpanderRow widgets.
Centre suffix controls with `valign = Gtk.Align.CENTER`. Do not add another
`card` class to a boxed list: it already owns a border and surface. Within a
larger card, place the group/list in the padded body as an intentionally inset
group; its separate list border is intentional, with no extra list shadow.
Use the list/group alone when a single flush boundary is wanted. Expanded
content uses native rows; do not wrap each nested row in another padded body.

Clock integration: use these page/card classes, native spacing values and
ordinary `image-button` / `flat` buttons with 16px symbolic icons. Keep generic
controls theme-owned. Specialized content such as progress rings and a World
Clock map may use custom drawing. No Clock-specific theme CSS is required.

## Document tabs and editors

Use `majoris-document-tabs` on Adw.TabBar, `majoris-editor-toolbar` on an editor
action Box and `majoris-statusbar` on the status Box. SourceView applications
request `majoris-light` / `majoris-dark` from StyleSchemeManager and explicitly
update automatic scheme selection when StyleManager.dark changes. Behaviour,
user font preferences and third-party scheme selection remain application-owned.
[Complete Vala examples, installation and accessibility](editor-components.md).


## GTK4 location bar

Use `majoris-location-bar` on a horizontal container, `majoris-location-crumb`
on its native breadcrumb buttons and `majoris-location-current` on the current
folder button. Separators use `majoris-location-separator`. Switch a Gtk.Stack
to an expanding Gtk.Entry with `majoris-location-entry`, adding
`majoris-location-editing` to the outer container while editing.
`majoris-high-contrast` on that container opts into stronger borders and text.
The outer field, breadcrumbs and internal entry use the standard 4px control
radius. The composite field shares the normal Entry surface, border and subtle
control shadow. Its complete height is 32px: 24px child content + 2px transparent
child border + 4px outer padding + 2px outer border. Native text can grow it.
Breadcrumbs stay flat and use 14px/500; the current folder uses 14px/600.
Editing uses the normal Entry border and focus shadow only on the outer field
while the inner entry has focus. Breadcrumb :focus-visible is independent. Semantic surfaces, text, hover, pressed and focus
colours follow the existing light/dark theme and StyleManager bridge.

Keep Back, Forward, Up, Home and Copy outside the pill as ordinary 32px icon
buttons, without `flat`, breadcrumb or editor-toolbar classes. Reuse
`majoris-document-tabs` on Adw.TabBar. No extra appearance CssProvider is needed.

The theme cannot add navigation behaviour to Majoris Files. Application code
must build crumbs, validate paths, manage history, select the full path on
Ctrl+L / Alt+D or empty-space activation, confirm on Enter and cancel on Escape,
focus loss or outside clicks. Use a labelled, keyboard-accessible empty target
separate from crumb handlers; reserve at least 48px. Constrain the breadcrumb
viewport, ellipsize labels and scroll long paths. The factory's absolute paths
are simulated; it performs no filesystem operations and accepts syntactically
valid absolute paths rather than checking whether folders exist.

Open the native demonstration from Headerbars or run
`./scripts/run-factory.sh --light --page=location` (also `--dark`).
`--page=location-editing` starts editing for capture; `MAJORIS_CONTENT_WIDTH=480`
exercises narrow layouts. The fixture includes labelled held hover, pressed,
focus, disabled, long-path, contrast, editing and backdrop states. Held flags
are CSS diagnostics; verify real pointer, Tab and screen-reader interaction too.
Use the application scheme menu for Light → Dark → Light.

## Finalised navigation sidebars

The [sidebar integration guide](sidebar-design.md) defines 224px as an app-owned
starting width, 32px/4px rows, 16px symbolic icons, section headers, native
expanders, badges, RTL, scrolling and NavigationSplitView breakpoint handling.
Use `majoris-sidebar-native-divider` with a split view that already supplies
separation. Preserve the chosen row across native focus restoration, and avoid
global accelerators that swallow list/disclosure keys. The theme supplies
presentation; application code supplies navigation structure and behavior.


### Composite location field in the universal Toolbar

Use `append_widget` for the composite and `append_control` for a SearchEntry;
never designate its internal crumbs as Toolbar controls. The Toolbar keeps its
existing 40px/4px/8px geometry and 4px spacing; no extra margins or provider are
needed. The composite uses existing control-radius, field surface, border,
shadow and focus definitions, with a transparent 4px inner entry.

```vala
var toolbar = new Majoris.Ui.Toolbar();
var location = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
location.add_css_class("majoris-location-bar");
location.hexpand = true;
location.valign = Gtk.Align.CENTER;
var modes = new Gtk.Stack();
modes.hexpand = true;
modes.hhomogeneous = false;
var crumbs = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
var folder = new Gtk.Button.with_label("Documents");
folder.add_css_class("majoris-location-crumb");
folder.add_css_class("majoris-location-current");
crumbs.append(folder);
// In a real app, put crumbs in a horizontal scrolling viewport and reserve
// the accessible empty-space target. See LocationBar in the native factory.
modes.add_named(crumbs, "crumbs");
var path = new Gtk.Entry();
path.add_css_class("majoris-location-entry");
path.hexpand = true;
modes.add_named(path, "entry");
location.append(modes);
toolbar.append_widget(location);
var search = new Gtk.SearchEntry();
search.placeholder_text = "Search files";
toolbar.append_control(search);
// Application-owned switch to editing:
location.add_css_class("majoris-location-editing");
modes.visible_child_name = "entry";
path.grab_focus();
path.select_region(0, -1);
```

The factory preserves simulated history and path editing. It does not implement
filesystem completion, suggestions, volumes or network navigation; applications
retain those behaviours and can attach native completion/popovers to the entry.
[Native standardisation measurements and screenshots](location-bar-standardisation.md).
