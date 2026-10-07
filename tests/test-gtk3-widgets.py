"""Exercise GTK3 selectors on realized widgets, checking native computed styling."""
from pathlib import Path
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk,GLib
root=Path(__file__).resolve().parents[1]
Gtk.init([])
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
provider=Gtk.CssProvider(); provider.load_from_path(str(root/'theme/Majoris/gtk-3.0/gtk.css'))
Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
window=Gtk.Window(); window.set_default_size(600,300)
bar=Gtk.HeaderBar(); bar.set_show_close_button(True); bar.set_decoration_layout(':minimize,maximize,close'); window.set_titlebar(bar)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8); window.add(box)
button=Gtk.Button(label='Native GTK3 default'); box.pack_start(button,False,False,0)
entry=Gtk.Entry(); box.pack_start(entry,False,False,0)
for widget in [Gtk.CheckButton(label='Check'),Gtk.RadioButton(label='Radio'),Gtk.Switch(),Gtk.SpinButton.new_with_range(0,100,1),Gtk.ProgressBar(),Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL,0,100,1)]: box.pack_start(widget,False,False,0)
popover=Gtk.Popover.new(button); popover.add(Gtk.Label(label='Native popover'))
menu=Gtk.Menu(); menu.append(Gtk.MenuItem(label='Native menu item'))
window.show_all()
loop=GLib.MainLoop(); GLib.timeout_add(250,lambda:(loop.quit(),False)[1]); loop.run()
for widget in [button,entry]:
    context=widget.get_style_context()
    border=context.get_border(Gtk.StateFlags.NORMAL)
    assert border.left==1 and border.right==1
    assert widget.get_allocated_height()==32,(type(widget).__name__,widget.get_allocated_height())
color=button.get_style_context().get_color(Gtk.StateFlags.NORMAL)
assert round(color.red*255)==28 and round(color.green*255)==28 and round(color.blue*255)==31,color.to_string()
window.destroy()
print('Realized GTK3 button/entry geometry, borders and text color passed; radius remains a visual check')
