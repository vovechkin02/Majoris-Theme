"""Real GTK switch allocations, native input, libadwaita rows and unedited captures."""
import os,sys,json,subprocess,ctypes,re
from pathlib import Path
import gi
version=sys.argv[1] if len(sys.argv)>1 else '4'
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk,Gdk,GLib
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light');scale=os.environ.get('GDK_SCALE','1')
out=root/'artifacts/switch-standardisation'/('gtk'+version)/variant/('scale-'+scale+('-large-font' if os.environ.get('MAJORIS_LARGE_FONT') else ''));out.mkdir(parents=True,exist_ok=True)
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris');ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
 Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
else:
 Gtk.init([]);provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')));Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,800)
settings=Gtk.Settings.get_default();settings.set_property('gtk-enable-animations',False)
if os.environ.get('MAJORIS_LARGE_FONT'):settings.set_property('gtk-font-name','Plus Jakarta Sans 18')
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(150,lambda:(loop.quit(),False)[1]);loop.run()
def append(parent,child):parent.append(child) if version=='4' else parent.pack_start(child,False,False,0)
def descendants(w):
 if version=='4':
  child=w.get_first_child()
  while child:
   yield child;yield from descendants(child);child=child.get_next_sibling()
def allocation(w):return [w.get_allocated_width(),w.get_allocated_height()]
w=Adw.Window(title='Majoris switch test') if version=='4' else Gtk.Window(title='Majoris switch test')
w.set_default_size(600,400);box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16)
for edge in ('top','bottom','start','end'):getattr(box,'set_margin_'+edge)(16)
w.set_content(box) if version=='4' else w.add(box)
sw=Gtk.Switch();sw.set_halign(Gtk.Align.START);sw.set_valign(Gtk.Align.CENTER);append(box,sw)
append(box,Gtk.Button(label='Button 4px'));append(box,Gtk.CheckButton(label='Checkbox 4px'))
if version=='4':
 group=Adw.PreferencesGroup();row=Adw.SwitchRow(title='Native SwitchRow');group.add(row)
 disabled=Adw.SwitchRow(title='Disabled row',active=True,sensitive=False);group.add(disabled)
 action=Adw.ActionRow(title='ActionRow');suffix=Gtk.Switch(valign=Gtk.Align.CENTER);action.add_suffix(suffix);action.set_activatable_widget(suffix);group.add(action);append(box,group)
 w.present()
else:w.show_all()
settle()
wid=subprocess.check_output(['xdotool','search','--name','^Majoris switch test$'],text=True).splitlines()[-1]
def capture(name):
 settle();path=out/(name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
def pointer():
 if version=='4':
  ok,bounds=sw.compute_bounds(box);x=bounds.get_x()+sw.get_width()/2;y=bounds.get_y()+sw.get_height()/2
 else:
  x,y=sw.translate_coordinates(box,0,0);x+=sw.get_allocated_width()/2;y+=sw.get_allocated_height()/2
 subprocess.run(['xdotool','mousemove','--window',wid,str(int((x+16)*int(scale))),str(int((y+16)*int(scale)))],check=True);settle()
records={}
if version=='4':
 lib=ctypes.CDLL('libgtk-4.so.1');lib.gtk_snapshot_to_node.argtypes=[ctypes.c_void_p];lib.gtk_snapshot_to_node.restype=ctypes.c_void_p
 lib.gsk_render_node_write_to_file.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p];lib.gsk_render_node_write_to_file.restype=ctypes.c_int
 lib.gsk_render_node_unref.argtypes=[ctypes.c_void_p]
def render(widget,name):
 snap=Gtk.Snapshot();Gtk.WidgetPaintable.new(widget).snapshot(snap,widget.get_allocated_width(),widget.get_allocated_height())
 node=lib.gtk_snapshot_to_node(hash(snap));assert node
 path=out/(name+'.node');assert lib.gsk_render_node_write_to_file(node,str(path).encode(),None);lib.gsk_render_node_unref(node)
 return path.read_text()

def measure(name):
 settle();records[name]={'track':allocation(sw),'active':sw.get_active(),'sensitive':sw.get_sensitive()}
 assert allocation(sw)==[40,22],(name,allocation(sw))
 if version=='4':
  slider=next(c for c in descendants(sw) if c.get_css_name()=='slider');records[name]['thumb']=allocation(slider)
  assert allocation(slider)==[17,16],records[name]
 capture(name)
 context=sw.get_style_context();padding=context.get_padding() if version=='4' else context.get_padding(sw.get_state_flags());border=context.get_border() if version=='4' else context.get_border(sw.get_state_flags())
 assert [padding.top,padding.right,padding.bottom,padding.left]==[2]*4
 assert [border.top,border.right,border.bottom,border.left]==[1]*4
 if version=='4':
  text=render(sw,name)
  assert re.search(r'outline: [^;]+ / 4;',text),(name,text)
  records[name]['radius']=4
  if name=='focused':
   assert 'outline-width: 2' in text or re.search(r'widths: 2',text),text
  if not sw.get_sensitive():
   assert text.count('opacity {')==1 and 'opacity: 0.58;' in text,text
  ok,bounds=slider.compute_bounds(sw);assert ok
  records[name]['thumb_bounds']=[bounds.get_x(),bounds.get_y(),bounds.get_width(),bounds.get_height()]
  assert bounds.get_y()==0 and bounds.get_x()>=0 and bounds.get_x()+bounds.get_width()<=34,records[name]
# Native baseline comparison changes only the track radius in a temporary provider.
comparison=Gtk.CssProvider();comparison.load_from_data(b'switch { border-radius: 8px; }')
if version=='4':Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),comparison,1000)
else:Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),comparison,1000)
capture('before-radius-8px')
if version=='4':Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),comparison)
else:Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),comparison)
measure('unchecked');pointer();measure('hovered')
subprocess.run(['xdotool','mousedown','1'],check=True);measure('pressed');subprocess.run(['xdotool','mouseup','1'],check=True);settle();assert sw.get_active();measure('checked');measure('checked-hovered')
subprocess.run(['xdotool','mousedown','1'],check=True);measure('checked-pressed');subprocess.run(['xdotool','mouseup','1'],check=True);settle()
# Restore checked state after this additional native toggle.
sw.set_active(True)
subprocess.run(['xdotool','click','1'],check=True);settle();assert not sw.get_active()
sw.grab_focus();subprocess.run(['xdotool','windowfocus',wid,'key','Tab','key','shift+Tab','key','space'],check=True);settle();assert sw.get_active();measure('focused')
for active in (False,True):
 sw.set_active(active);sw.set_sensitive(False);measure('disabled-'+str(active).lower());sw.set_sensitive(True)
sw.set_direction(Gtk.TextDirection.RTL);measure('rtl');sw.set_direction(Gtk.TextDirection.LTR)
if version=='4':
 row_switch=next(c for c in descendants(row) if isinstance(c,Gtk.Switch))
 row.grab_focus();subprocess.run(['xdotool','key','space'],check=True);settle();assert row.get_active()
 capture('adw-switch-row')
 for child in descendants(disabled):
  if isinstance(child,Gtk.Switch):
   assert render(child,"disabled-row-switch").count("opacity {")==1
   assert "opacity: 0.58;" in render(child,"disabled-row-switch")
   assert disabled.get_opacity()==1
   for thumb in descendants(child):
    if thumb.get_css_name()=='slider':assert thumb.get_opacity()==1
 dialog=Adw.PreferencesDialog(title='Switch preferences');page=Adw.PreferencesPage();group=Adw.PreferencesGroup()
 for active in (False,True):group.add(Adw.SwitchRow(title=str(active),active=active))
 page.add(group);dialog.add(page);dialog.present(w);settle()
 dialog_switch=next(c for c in descendants(group) if isinstance(c,Gtk.Switch));dialog_row=next(c for c in descendants(group) if isinstance(c,Adw.SwitchRow));dialog_row.grab_focus()
 subprocess.run(['xdotool','key','space'],check=True);settle();assert dialog_switch.get_active()
 capture('preferences-dialog');dialog.close()
(out/'switch-dimensions.json').write_text(json.dumps(records,indent=2)+'\n')
w.destroy();print('Native switch geometry/input passed',version,variant,scale)
