"""Real GTK3 fixture; appearance comes from the installed Majoris theme."""
import gi,sys
from pathlib import Path
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GLib
Gtk.Settings.get_default().set_property('gtk-theme-name','Majoris')
Gtk.Settings.get_default().set_property('gtk-icon-theme-name','Majoris')
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
win=Gtk.Window(title='Majoris GTK3 native visual regression');win.set_default_size(1000,760)
bar=Gtk.HeaderBar(title='GTK3 / native headerbar');bar.set_has_subtitle(False);bar.set_show_close_button(True);win.set_titlebar(bar)
body=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16);body.set_border_width(24);scroller=Gtk.ScrolledWindow();scroller.set_overlay_scrolling(True);scroller.add(body);win.add(scroller)
body.pack_start(Gtk.Label(label='Native GTK3 controls and held toolkit states. No appearance overrides.'),False,False,0)
for label,style in [('Normal',''),('Primary','suggested-action'),('Destructive','destructive-action'),('Flat','flat')]:
    line=Gtk.Box(spacing=12);body.pack_start(line,False,False,0)
    for state,flag in [('Default',Gtk.StateFlags.NORMAL),('Hover',Gtk.StateFlags.PRELIGHT),('Pressed',Gtk.StateFlags.ACTIVE),('Focus',Gtk.StateFlags.FOCUSED),('Disabled',Gtk.StateFlags.INSENSITIVE)]:
        b=Gtk.Button(label=label+' / '+state)
        if style:b.get_style_context().add_class(style)
        line.pack_start(b,False,False,0)
        if state=='Disabled':b.set_sensitive(False)
        else:GLib.timeout_add(300,lambda b=b,flag=flag:(b.set_state_flags(flag,False),False)[1])
line=Gtk.Box(spacing=12);body.pack_start(line,False,False,0)
e=Gtk.Entry();e.set_text('Majoris text entry');line.pack_start(e,False,False,0)
c=Gtk.ComboBoxText();c.append_text('Dropdown');c.set_active(0);line.pack_start(c,False,False,0)
line.pack_start(Gtk.SpinButton.new_with_range(0,100,1),False,False,0)
line=Gtk.Box(spacing=12);body.pack_start(line,False,False,0)
for active in [False,True]:
    check=Gtk.CheckButton(label='Checked' if active else 'Unchecked');check.set_active(active);line.pack_start(check,False,False,0)
    switch=Gtk.Switch();switch.set_active(active);line.pack_start(switch,False,False,0)
radio=Gtk.RadioButton.new_with_label_from_widget(None,'Radio');line.pack_start(radio,False,False,0)
p=Gtk.ProgressBar();p.set_fraction(.68);body.pack_start(p,False,False,0)
level=Gtk.LevelBar.new_for_interval(0,8);level.set_mode(Gtk.LevelBarMode.DISCRETE);level.set_value(6);body.pack_start(level,False,False,0)
notebook=Gtk.Notebook();notebook.append_page(Gtk.Label(label='Native content'),Gtk.Label(label='General'));notebook.append_page(Gtk.Label(label='Details'),Gtk.Label(label='Details'));body.pack_start(notebook,False,False,0)
spinner=Gtk.Spinner();spinner.start();spinner.set_halign(Gtk.Align.START);body.pack_start(spinner,False,False,0)
for i in range(30):body.pack_start(Gtk.Label(label='Native overlay scrollbar row %d'%i),False,False,0)
if '--scrolled' in sys.argv:GLib.timeout_add(700,lambda:(scroller.get_vadjustment().set_value(scroller.get_vadjustment().get_upper()-scroller.get_vadjustment().get_page_size()),False)[1])
win.connect('destroy',Gtk.main_quit);win.show_all();win.set_focus(None)
GLib.timeout_add(15000,lambda:(Gtk.main_quit(),False)[1]);Gtk.main()
