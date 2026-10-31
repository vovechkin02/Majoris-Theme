import gi,json,ctypes,os,sys
from pathlib import Path
gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
from gi.repository import Gtk,Adw,GLib
Adw.init();root=Path(__file__).resolve().parents[1];os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris');ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
w=Adw.Window(default_width=650);page=Adw.PreferencesPage();w.set_content(page)
g=Adw.PreferencesGroup(title='Information',description='Group description');g.set_header_suffix(Gtk.Button(label='Add',valign=Gtk.Align.CENTER));page.add(g)
for subtitle in ('','19 bytes'):
 r=Adw.ActionRow(title='Size',subtitle=subtitle);g.add(r)
r=Adw.ActionRow(title='Type',subtitle='Plain text document');r.add_css_class('property');r.set_subtitle_selectable(True);g.add(r)
g.add(Adw.EntryRow(title='Entry'));g.add(Adw.SwitchRow(title='Switch'))
w.present();loop=GLib.MainLoop();GLib.timeout_add(400,lambda:(loop.quit(),False)[1]);loop.run()
def tree(x):
 c=x.get_first_child();children=[]
 while c:children.append(tree(c));c=c.get_next_sibling()
 d=dict(type=x.__class__.__name__,node=x.get_css_name(),classes=list(x.get_css_classes()),allocation=[x.get_allocated_width(),x.get_allocated_height()],children=children)
 if isinstance(x,Gtk.Label):
  ink,logical=x.get_layout().get_pixel_extents();d.update(text=x.get_text(),font=x.get_layout().get_context().get_font_description().to_string(),ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.x,logical.y,logical.width,logical.height],offset=x.get_layout_offsets())
 return d
print(json.dumps(tree(page if '--page' in sys.argv else g),indent=2));w.destroy()
