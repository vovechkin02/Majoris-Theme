"""Real GTK allocation contract through the existing StyleManager bridge."""
import ctypes, json, os, gi
from pathlib import Path
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib
root = Path(__file__).resolve().parents[1]
os.environ['MAJORIS_THEME_ROOT'] = str(root/'theme/Majoris')
Adw.init()
ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
Gtk.Settings.get_default().set_property('gtk-enable-animations', False)
window = Adw.Window()
scroll = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER)
page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
page.add_css_class('majoris-page-content')
scroll.set_child(page)
window.set_content(scroll)
card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
card.add_css_class('card')
page.append(card)
parts = {}
for name in ('header', 'body', 'footer'):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    box.add_css_class('majoris-card-'+name)
    label = Gtk.Label(label=name, xalign=0)
    box.append(label)
    card.append(box)
    parts[name] = (box, label)
group = Adw.PreferencesGroup()
row = Adw.ActionRow(title='Native preferences', subtitle='Subtitle')
suffix = Gtk.Button(icon_name='go-next-symbolic', valign=Gtk.Align.CENTER)
suffix.add_css_class('image-button')
row.add_suffix(suffix)
group.add(row)
parts['body'][0].append(group)
boxed = Gtk.ListBox(selection_mode=Gtk.SelectionMode.NONE)
boxed.add_css_class('boxed-list')
for i in range(2):
    boxed.append(Adw.ActionRow(title='Grouped row'))
parts['body'][0].append(boxed)

def settle():
    loop = GLib.MainLoop()
    GLib.timeout_add(120, lambda: (loop.quit(), False)[1])
    loop.run()

def bounds(widget, parent):
    ok, rect = widget.compute_bounds(parent)
    assert ok
    return [round(rect.get_x()), round(rect.get_y()), round(rect.get_width()), round(rect.get_height())]

results = []
window.present()
try:
    for width in (360, 390, 650, 900, 1200):
        window.set_default_size(width, 780)
        compact = width < 650
        if compact: page.add_css_class('majoris-compact')
        else: page.remove_css_class('majoris-compact')
        allocations = []
        for scheme in (Adw.ColorScheme.FORCE_LIGHT, Adw.ColorScheme.FORCE_DARK, Adw.ColorScheme.FORCE_LIGHT):
            Adw.StyleManager.get_default().set_color_scheme(scheme)
            settle()
            gutter = 16 if compact else 24
            assert page.get_allocated_width() - card.get_allocated_width() == gutter * 2
            assert parts['body'][0].get_allocated_width() - parts['body'][1].get_allocated_width() == 32
            padding = parts['body'][0].get_style_context().get_padding()
            assert (padding.top, padding.bottom, padding.left, padding.right) == (16, 16, 16, 16)
            padding = parts['footer'][0].get_style_context().get_padding()
            assert (padding.top, padding.bottom, padding.left, padding.right) == (12, 12, 16, 16)
            assert parts['footer'][0].get_allocated_height() - parts['footer'][1].get_allocated_height() == 25
            assert bounds(parts['header'][1], card)[0] == bounds(parts['body'][1], card)[0]
            assert suffix.get_allocated_width() == suffix.get_allocated_height() == 32
            image = suffix.get_child()
            # Gtk.Image fills the button content box; symbolic artwork keeps its natural 16px size.
            assert image.measure(Gtk.Orientation.HORIZONTAL, -1)[:2] == (16, 16)
            assert image.measure(Gtk.Orientation.VERTICAL, -1)[:2] == (16, 16)
            first, last = boxed.get_row_at_index(0), boxed.get_row_at_index(1)
            assert first.get_style_context().get_border().bottom == 1
            assert last.get_style_context().get_border().bottom == 0
            row_padding = row.get_style_context().get_padding()
            list_padding = first.get_style_context().get_padding()
            assert (row_padding.left, row_padding.right) == (list_padding.left, list_padding.right)
            s = bounds(suffix, row)
            assert abs(s[1] + s[3]/2 - row.get_height()/2) <= 1, (s, row.get_height())
            assert window.get_allocated_width() == width, (width, window.get_allocated_width())
            allocations.append([bounds(card, page), bounds(suffix, row)])
        assert allocations[0] == allocations[1] == allocations[2], allocations
        results.append({'width': width, 'compact': compact, 'allocations': allocations[0]})
finally:
    window.destroy()
out = root/'artifacts/layout-native.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2)+'\n')
print('Native layout, suffix centring, icon size and switching parity: five widths')
