# Majoris Toolbar Design Specification

The general toolbar family is opt-in. Use `.majoris-toolbar` with either
`.majoris-toolbar-navigation` or `.majoris-toolbar-commands` on a horizontal GtkBox.
The existing `.majoris-editor-toolbar` stays independent: a 40px strip containing
28px flat controls. Adding the new family never upgrades editor controls to 32px.

## Contract

| Property | Navigation / Command |
| --- | --- |
| Complete height | 40px minimum at normal text size; larger text can grow |
| Content minimum / padding | 32px content + 4px top/bottom; 16px left/right |
| Standard icon button | 32×32px, 4px radius, existing Majoris elevation/states |
| Standard text action | 32px high, natural width, 14px/600 |
| Menu button / entry | 32px high, 14px/500 |
| Supporting text | `.majoris-toolbar-metadata`, 12px/400 |
| Symbolic artwork | 16×16px; SVG files remain unchanged |
| Icon-and-label gap | 8px |
| Within / between groups | 4px / 8px; optional 16px major-group spacing |
| Toolbar elevation | None |
| Bottom divider | Optional 1px background stripe painted inside the 40px box |
| Vertical separator | 1px soft-border line, 4px vertical inset within content |
| Motion | Existing 128ms cubic-bezier(.2,0,0,1), colours/border/shadow only |

| Surface | Light | Dark |
| --- | --- | --- |
| Navigation | #FFFFFF | #202023 |
| Commands | #F7F7F8 | #28282C |
| Divider | #E5E5E9 | #313136 |
| View-switcher container | #F2F2F4 | #242428 |
| Selected segment | #FFFFFF | #35353A |
| Focus | #6366F1 | #818CF8 |

Normal controls inherit existing Majoris default, hover, pressed, focus, disabled
and backdrop treatment. Ordinary Trash/Delete actions do not acquire window-close
red styling. Apply an existing destructive semantic class deliberately if needed.
Do not introduce a new destructive palette. Selected segments retain a persistent
surface while unselected hover uses the ordinary neutral tint. A single inset 2px
focus outline is independent of selection. Disabled controls have no hover/press
feedback; checked disabled segments retain their identifiable selected surface.

## Classes and ownership

- `.majoris-toolbar`: flat surface, complete-height geometry, UI typography.
- `.majoris-toolbar-navigation`, `.majoris-toolbar-commands`: surface variants.
- `.majoris-toolbar-divider`: optional painted bottom hairline; Commands includes it.
- `.majoris-toolbar-group`: transparent, unbordered horizontal action group.
- `.majoris-toolbar-major-groups`: optional 16px gap between major groups.
- `.majoris-toolbar-spacer`: neutral zero-minimum box; set `hexpand=true` in code.
- `.majoris-toolbar-control`: opt in an intended button or GtkMenuButton to 32px.
- `.majoris-toolbar-icon`: 32px icon-only treatment, in addition to control.
- `.majoris-toolbar-action`: icon-and-text control with an 8px content gap.
- `.majoris-toolbar-menu`: 14px/500 menu trigger, in addition to control.
- `.majoris-toolbar-field`: GtkEntry/GtkSearchEntry sizing; do not attach to crumbs.
- `.majoris-toolbar-view-switcher`: native exclusive toggle group, 32px overall.
- `.majoris-toolbar-separator`: native inline separator with soft-border colour.

Applications own horizontal orientation, expansion, accessible names/tooltips,
commands, navigation history, focus order, accelerator registration, and responsive
presentation. CSS does not implement navigation or collapse controls automatically.
Only explicit control classes receive new button geometry; no broad toolbar-button
descendant rule can restyle a nested breadcrumb or menu row.

## GTK4 / Vala composition

Construct GtkBoxes with spacing 0 under GTK4: scoped CSS border-spacing supplies
8px between groups, 4px within groups, and 8px inside an icon-and-label control.
Do not also add the same widget spacing or icon margins a second time.

```vala
var navigation = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
navigation.add_css_class("majoris-toolbar");
navigation.add_css_class("majoris-toolbar-navigation");
navigation.add_css_class("majoris-toolbar-divider");
var history = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
history.add_css_class("majoris-toolbar-group");
var back = new Gtk.Button.from_icon_name("go-previous-symbolic");
back.add_css_class("majoris-toolbar-control");
back.add_css_class("majoris-toolbar-icon");
back.valign = Gtk.Align.CENTER;
back.tooltip_text = "Back";
back.update_property(Gtk.AccessibleProperty.LABEL, "Back", -1);
history.append(back);
navigation.append(history);

var location = new MajorisThemeFactory.LocationBar(); // Or your existing component.
location.hexpand = true;
location.valign = Gtk.Align.CENTER;
navigation.append(location); // No toolbar-control class on location or crumbs.
var search = new Gtk.SearchEntry();
search.add_css_class("majoris-toolbar-field");
search.valign = Gtk.Align.CENTER;
navigation.append(search);
```

The LocationBar above is the repository's native fixture/reference component,
not a new installed application library. Existing applications should use their
own implementation of the documented location classes. Its 32px outer component,
26px crumbs and 26px entry remain authoritative, including existing typography,
9px/7px radius exceptions, transparent crumbs and native editing behaviour.
The toolbar fixture wires Ctrl+L/Alt+D to location entry and Ctrl+F to search;
applications own these shortcuts and their conflicts.

```vala
var commands = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
commands.add_css_class("majoris-toolbar");
commands.add_css_class("majoris-toolbar-commands");
var primary = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
primary.add_css_class("majoris-toolbar-group");
commands.append(primary);
var spacer = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
spacer.add_css_class("majoris-toolbar-spacer");
spacer.hexpand = true;
commands.append(spacer);
var views = new Gtk.Box(Gtk.Orientation.HORIZONTAL, 0);
views.add_css_class("majoris-toolbar-view-switcher");
views.valign = Gtk.Align.CENTER;
Gtk.ToggleButton? first = null;
foreach (var name in new string[]{"Grid", "List", "Columns", "Gallery"}) {
    var button = new Gtk.ToggleButton.with_label(name);
    if (first == null) { first = button; button.active = true; }
    else button.group = first;
    button.tooltip_text = name;
    views.append(button);
}
commands.append(views);
```

For icon-only segments, put a 16px GtkImage inside each toggle, with
`halign=valign=CENTER`, and provide a meaningful accessible label. Icon-and-text
buttons similarly use a horizontal GtkBox and a vertically centered 16px image.
The button provides surrounding allocation; the SVG has no intrinsic padding.

The segmented allocation is derived: 24px segment + 3px padding on each side +
1px border on each side = 32px. Each segment has a 20px content minimum and 2px
vertical padding; 16px images center within it and 14px labels fit naturally.
The 3px and 7px icon-button padding values are native border-box arithmetic, not
new general spacing tokens: 16px icon + 7px each side + 1px borders = 32px.

Do not insert a separate horizontal GtkSeparator below a toolbar and count it as
40px: that would add a pixel. Use the painted divider class. For native separators
inside an appropriate group/overlay, set orientation and alignment in code; use
`valign=CENTER` for a horizontal line, and retain natural 1px thickness. The fixture
uses an inline vertical separator, not a floating card or elevated group surface.

## Menus, narrow windows and GTK3

Apply toolbar-control/menu classes only to the trigger. Build its normal native
GtkPopover/GtkPopoverMenu separately. Popover rows do not receive toolbar classes;
they retain the existing menu radius, padding, typography, keycaps and shadow.
The fixture demonstrates a Locations menu and a Sort/View menu with real Gio
choices. Text/background styling is not applied through generic descendant rules.

At narrow widths the fixture uses a GtkScrolledWindow per row with horizontal
policy EXTERNAL and vertical policy NEVER. The scroll window itself has no fixed
width and propagates natural height. Keyboard focus reveals offscreen controls.
No extra visible horizontal scrollbar is added. This is one sample policy;
applications may instead collapse groups into native overflow menus or hide
secondary controls. Do not encode a Files-specific collapse policy in theme CSS.

GTK3 uses the same opt-in classes and palettes, but CSS cannot set GtkBox spacing.
Set widget spacing explicitly: 8px on the toolbar, 4px on a group, 8px in an
icon-and-label box and 2px inside the view switcher (16px for major separation).
Use GtkRadioButtons with `draw_indicator=false`/`set_mode(false)` for native exclusive
icon segments. Use real GtkMenu where appropriate. Associate a container's focus
horizontal adjustment with its scrolled viewport when needed. Resize an already
mapped GTK3 test window with `resize()`, not just `set_default_size()`.
The GTK4-specific location implementation is not ported or simulated for GTK3.

Reduced motion is GTK-owned: honour GtkSettings `gtk-enable-animations`. The theme
uses native CSS transitions; it does not introduce animation timers or custom
rendering. Fixture timers only hold native review states or run measurement probes.

## Validation and before/after

| Before | After |
| --- | --- |
| General bars were application-owned GtkBoxes | Explicit Navigation / Command component classes |
| Height/insets varied by application | Measured 40px minimum, 4px/16px padding |
| Group spacing was ad hoc | 4px / 8px / optional 16px contract |
| Generic segments could enlarge a toolbar | Independent measured 32px toolbar segment group |
| Breadcrumbs risked broad button overrides | Only explicit toolbar-control classes get sizing |
| Editor was the only specialised toolbar | Editor remains 40px / 28px flat, alongside general bars |

Canonical HTML component rules are extracted into both token JSON files. The
existing generator appends `gtk-toolbar.css.in` to both GTK versions and palettes;
GTK3-only CSS capability adaptation remains in that same pipeline. Typography,
surfaces, spacing and border-box derivation read the canonical design rules.

Native matrix tests inspect actual 40px bars, 32px controls/switcher, 16px images,
8px icon-label and inter-group gaps, 4px in-group gaps, stationary text baselines,
native keyboard selection, menus, narrow scrolling and enlarged text growth.
The compiled factory probe independently checks normal, 480px narrow and location
entry modes. Existing menu/tab/sidebar/data/headerbar/editor tests remain intact.

See `artifacts/toolbar-finalisation/README.md` for native GTK3/GTK4 captures and
JSON measurements. Full GNOME/Wayland focus, backdrop, fractional scaling and
screen-reader validation still need the repository's VM workflow. Xvfb state
captures hold native flags; they are not proof of compositor state forwarding.
Direct popup captures accompany main-window views because root X11 captures can
omit ARGB popup content. No HTML screenshots substitute for native validation.
