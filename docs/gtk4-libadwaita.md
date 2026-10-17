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
