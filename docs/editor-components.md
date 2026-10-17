# Native document and editor components

Majoris applications opt in to three GTK4 components. The original widget
factory remains authoritative for established controls; the unchanged
[supplemental showcase](../design/reference/editor-v1/Majoris-Theme-Complete-Widget-Showcase-v1.html)
specifies the additions. No Notepad, Shell, GDM or icon asset was changed.

| Class | Native widget | Theme-owned presentation |
|---|---|---|
| `majoris-document-tabs` | `Adw.TabBar` | 38px strip including divider, flat surface, neutral hover/press, selected text and 2px underline, compact close controls and visible focus |
| `majoris-editor-toolbar` | Horizontal `Gtk.Box`, optionally inside a horizontally scrolling container | 40px including bottom divider, 28px actions, flat states, 4px radii, restrained checked tint |
| `majoris-statusbar` | Horizontal `Gtk.Box` | 34px including top divider, secondary surface, 28px flat selectors and quiet text |

Dimensions are default-font logical pixels. Native content minima can grow for
large accessibility fonts; the theme does not clip labels to enforce fixed
heights. Controls are focusable, preserve native accessible names/tooltips and
never translate or resize on interaction. Applications provide actions, title,
icons, modified-state indicators, close confirmation, content, accelerators,
separators and spacing. The theme adds no permanent New Tab strip action.

```vala
var documents = new Adw.TabView ();
var tabs = new Adw.TabBar ();
tabs.view = documents;
tabs.autohide = false;
tabs.expand_tabs = false; // native compact width negotiation and overflow
tabs.add_css_class ("majoris-document-tabs");
var page = documents.append (new Gtk.Label ("Document content"));
page.title = "notes.md";
page.icon = new ThemedIcon ("text-x-generic-symbolic");
// Unsaved state is application policy; these are native visual mechanisms.
page.needs_attention = true;
page.indicator_icon = new ThemedIcon ("document-save-symbolic");
page.indicator_tooltip = "Unsaved changes";

var toolbar = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 4);
toolbar.add_css_class ("majoris-editor-toolbar");
var bold = new Gtk.ToggleButton ();
bold.icon_name = "format-text-bold-symbolic";
bold.tooltip_text = "Bold";
bold.valign = Gtk.Align.CENTER;
toolbar.append (bold);
var separator = new Gtk.Separator (Gtk.Orientation.VERTICAL);
separator.valign = Gtk.Align.CENTER;
toolbar.append (separator);

var status = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 4);
status.add_css_class ("majoris-statusbar");
var position = new Gtk.Label ("Ln 1, Col 1");
position.hexpand = true;
position.xalign = 0;
status.append (position);
var encoding = new Gtk.MenuButton ();
encoding.label = "UTF-8";
encoding.valign = Gtk.Align.CENTER;
// Supply a native Popover or menu_model with the application's actions.
status.append (encoding);
```

Align toolbar/status controls vertically to CENTER. Use Box.spacing=4 within
an action group and 8 between groups, and centre vertical separators. Styling
supports direct buttons/menu buttons or one direct Box grouping level; it does
not style buttons inside their popovers. Place a wide toolbar inside a
ScrolledWindow using horizontal EXTERNAL / vertical NEVER policies to permit
native horizontal scrolling without increasing its visual height. At narrow
widths, application Breakpoints or equivalent native allocation logic should
hide/reflow lower-priority status groups. Do not force a minimum window width
or shrink hit targets further. GtkNotebook retains its distinct existing CSS.

The installed libadwaita 1.7 nodes are `tabbar > revealer > .box`, with
`tabbox > tabboxchild > tab`, `.tab-title`, `.tab-close-button`,
`.tab-indicator` and native `indicator` nodes. Selection is `tab:selected`,
not GtkNotebook's `tab:checked`. Hover, active, focus-visible, backdrop and
attention use native states. The attention indicator's inherited translation
is explicitly reset to `none`. Native tab closing, pinned tabs, reordering,
scrolling, accessible tab relations and drag/drop are retained.

## Source schemes and font ownership

`majoris-light` (Majoris Light) and `majoris-dark` (Majoris Dark) are generated
from `design/sourceview/*.xml.in`. Their editor surfaces derive from existing
semantic tokens. The XML templates own the supplemental syntax palette;
comments use readable secondary text rather than the mockup's fainter swatch.
Neither scheme sets a font. Dark syntax colours are independently chosen.

Normal installation puts both XMLs in `${prefix}/share/gtksourceview-5/styles`
(`/usr/share/gtksourceview-5/styles` for the standard prefix), and stages source
templates and extension tokens in `share/majoris-theme/design/sourceview`.
Development installation links only the two owned files in
`$XDG_DATA_HOME/gtksourceview-5/styles`; the styles directory and third-party
schemes remain intact. Conflicting files are journalled/backed up, repeated
installation is safe, and uninstall refuses user changes before restoring
original files. Run `scripts/install-dev.sh --variant=light|dark|auto` and the
existing uninstall helper. Both schemes remain available in every GTK variant.

```vala
var buffer = new GtkSource.Buffer (null);
var source = new GtkSource.View.with_buffer (buffer);
source.monospace = true; // explicit native font opt-in, independently configurable
var manager = GtkSource.StyleSchemeManager.get_default ();
var appearance = Adw.StyleManager.get_default ();
// Own/disconnect this notification with the application's document lifecycle.
appearance.notify["dark"].connect (() => {
    buffer.style_scheme = manager.get_scheme (
        appearance.dark ? "majoris-dark" : "majoris-light");
});
buffer.style_scheme = manager.get_scheme (
    appearance.dark ? "majoris-dark" : "majoris-light");
```

Only connect scheme selection when the user chose automatic Majoris colours.
Changing StyleManager does not change SourceView schemes automatically; the
application owns that decision and must preserve explicitly selected third-party
schemes. The factory follows the existing appearance action and uses installed
IDs, with a checkout search-path fallback to the same generated assets.

Two necessary existing-theme corrections preserve editor ownership: ordinary
selection colours now target standard text controls and non-source TextViews,
leaving SourceView's dynamic scheme provider free to style its selection;
GTK4's explicit `textview.monospace` opt-in now overrides the universal UI font.
Ordinary UI remains Plus Jakarta Sans. Application font overrides can target
the editor specifically at an appropriate CSS-provider priority; there is no
global monospace or hardcoded source font in the schemes.

## Native differences and validation limits

Native TabBar widths negotiate with titles, icons and available space; the
HTML's approximate 220px maximum is not a GTK CSS max-width. Use expand_tabs=false
for the demonstrated compact policy. Pinned tabs are icon-only. Native attention
may add an indicator and native underline; it is not a fake dirty pseudo-class.
Close buttons are 22px including their transparent border, retain libadwaita's
reserved allocation/fade and keyboard-close semantics. They never receive the
window-close destructive colour. Detached drag previews live outside TabBar's
CSS ancestry, so they retain libadwaita's native drag-preview treatment instead
of introducing an unscoped `dnd tab` override. Actual pointer drag/drop and
cross-window transfer require the GNOME VM check.

The installed SourceView Relax NG schema accepts the emitted XML. Metadata and
underline-colour extensions supported by some bundled schemes are omitted so
the distributable schemes validate against Trixie's on-disk schema. Errors and
warnings still have readable foregrounds and supported underlines.

See [testing](testing.md#editor-component-validation) and the
[implementation report](editor-implementation-report.md) for native evidence,
visual comparisons, scaling results and outstanding session checks.
