"""Native GTK3/4 menu rows. Import after selecting Gtk's GI version.

The application owns Gio actions and accelerator registration. This module owns
only native widget composition, shortcut semantics and menu dismissal.
"""
from gi.repository import Gtk


def menu_row(text, keys, *, action=None, shortcut='', icon=None, activate=None):
    gtk4 = Gtk.get_major_version() == 4
    row = Gtk.Button() if gtk4 else Gtk.MenuItem()
    def style(widget, name):
        widget.add_css_class(name) if gtk4 else widget.get_style_context().add_class(name)
    style(row, 'majoris-menu-row')
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    def append(container, child, expand=False):
        if gtk4:
            container.append(child)
        else:
            container.pack_start(child, expand, expand, 0)
    label = Gtk.Label(label=text, xalign=0, hexpand=True)
    append(box, label, True)
    caps = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    style(caps, 'majoris-menu-shortcut')
    caps.set_valign(Gtk.Align.CENTER)
    for key in keys:
        cap = Gtk.Label(label=key)
        style(cap, 'majoris-menu-keycap')
        append(caps, cap)
    append(box, caps)
    if gtk4:
        row.set_child(box)
        row.set_accessible_role(Gtk.AccessibleRole.MENU_ITEM)
        row.update_property([Gtk.AccessibleProperty.LABEL, Gtk.AccessibleProperty.KEY_SHORTCUTS], [text, shortcut.replace('<Control>', 'Control+').replace('<Alt>', 'Alt+').replace('<Shift>', 'Shift+')])
        if action:
            row.set_action_name(action)
        def clicked(widget):
            if activate:
                activate(widget)
            pop = widget.get_ancestor(Gtk.Popover)
            if pop:
                pop.popdown()
        row.connect('clicked', clicked)
    else:
        row.add(box)
        accessible = row.get_accessible()
        accessible.set_name(text)
        accessible.set_description('Keyboard shortcut: ' + shortcut)
        if action:
            row.set_action_name(action)
        if activate:
            row.connect('activate', activate)
    return row
