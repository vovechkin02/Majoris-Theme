# Native menu rows and v2 mapping

The unmodified target mockup is retained at
`design/reference/majoris-full-theme-mockup-v2.html`. Only its requested context-menu
geometry and keycap contract are applied. Existing opaque native menu surfaces,
state colours and shadows remain; the mockup's translucent menu backgrounds are
not applied. Dropdowns, ordinary popovers, login and unrelated controls retain their
previous styling. GTK4's menu contents node is the sole padding owner: the
libadwaita section box's extra 6px inset is reset within menu popovers only.

| Mockup | Native implementation |
| --- | --- |
| Menu padding 4px | GTK3 `menu`; GTK4 `popover.menu > contents`; Shell `.popup-menu-content` |
| Separator 1px + 2px/8px margins | Menu-scoped separators only, semantic `border_soft` |
| Row minimum 32px, padding 4px/8px | GTK4 content minimum 24px; GTK3 child requisition minimum 24px |
| Keycap minimum 22px, padding 2px/6px, border bottom 2px | Native label content minimum 15px plus padding/borders; actual natural size can be 23px |
| Individual keys, 4px gap | `.majoris-menu-shortcut` with adjacent `.majoris-menu-keycap` native labels |
| 12px/600 typography | Real Plus Jakarta Sans SemiBold; metadata is not globally emboldened |
| Light keycap | White surface, `#D8D8DD` border, `#626269` text |
| Dark keycap | `#2A2A2F` surface, `#43434A` border, `#C7C8D0` text |

GTK3 `GtkAccelLabel` draws its accelerator internally. Its accelerator node permits
font/colour styling, but does not expose individual key widgets or a separate
border/padding allocation. Standard third-party GTK3 menus therefore retain a plain
accelerator at 12px/600. GTK4's standard `accelerator` node supports a single bordered
capsule around the combined shortcut, but not a capsule per constituent key.

Use the reusable rows for exact individual capsules in Majoris-controlled menus:

- `factory/src/menu-row.vala`: `MajorisThemeFactory.MenuRow`, compiled by the factory
  and installed as reusable source under `share/majoris-theme/integration/`.
- `integration/menu_rows.py`: `menu_row()`, for GTK3/GTK4 Python applications.
- Styling lives entirely in the generated theme. Applications add semantic classes
  and native widgets; they do not ship appearance CSS.

For GTK4/Vala, register the real application accelerator, insert a named custom
slot into the GMenu, and supply its native child:

```vala
application.set_accels_for_action("win.rename", {"F2"});
var item = new MenuItem("Rename", null);
item.set_attribute_value("custom", new Variant.string("rename"));
model.append_item(item);
var popover = new Gtk.PopoverMenu.from_model(model);
popover.add_child(new MajorisThemeFactory.MenuRow(
    "Rename", "win.rename", "F2", {"F2"}), "rename");
```

The row implements GtkActionable through GtkButton. Native action-enabled state,
focus, activation and popover keyboard navigation remain in GTK. It supplies a menu
item accessible role, action name and `KEY_SHORTCUTS` property; activation dismisses
the popover. Use native GMenu items for checked/radio entries and submenus. The
factory demonstrates both together. Caller-provided visible keys must describe the
registered accelerator; e.g. `Control+c` accessibility text and `{"Ctrl","C"}` keys.

For GTK3/Python, place `menu_row()` in a GtkMenu attached to its owning window.
Register real Gio actions and application accelerators. Also use a GtkAccelGroup
on the window/menu and `row.add_accelerator('activate', group, key, modifiers,
Gtk.AccelFlags.VISIBLE)` so GTK/ATK can associate the native action with its shortcut.
The default GtkMenuItem accessible object retains its menu role and action
semantics; the component supplies its name and a shortcut description. No custom
painting, GTK internals or event synthesis is used by the component. Xdotool is used
only by the regression tests to exercise real keyboard input.

Majoris Files and other applications must adopt this source/component contract to
obtain separate GTK3 keycaps or split GTK4 key groups. A CSS theme cannot rewrite
third-party menu widget trees. Do not claim universal individual-keycap parity.

Shell St accelerator labels can be styled as one capsule using `.popup-menu-accel`.
Individual keys require application/extension-provided St labels; no Shell internals
are patched. Quick Settings retains its original 8px padding. Live Shell, Wayland,
Mutter and screen-reader acceptance require the existing GNOME VM workflow; static
Shell grammar/selector validation does not establish those runtime results.
