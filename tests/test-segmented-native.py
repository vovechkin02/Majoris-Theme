"""Native GTK4 segmented geometry, real dialog nodes and rendered evidence.
Run under dbus-run-session/xvfb-run; GDK_SCALE=2 and GDK_DPI_SCALE=1.25 supported.
"""
import os,ctypes,json,subprocess,re
from PIL import Image,ImageChops
from pathlib import Path
os.environ.setdefault('GSK_RENDERER','cairo')
import gi
gi.require_version('Gtk','4.0');gi.require_version('Adw','1');gi.require_version('GdkX11','4.0')
from gi.repository import Gtk,Adw,Gdk,GdkX11,GLib,Graphene
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light');scale=int(os.environ.get('GDK_SCALE','1'))
suffix=('-2x' if scale==2 else '')+('-text-125' if os.environ.get('GDK_DPI_SCALE')=='1.25' else '')
out=root/'artifacts/segmented-control-standardisation'/(variant+suffix);out.mkdir(parents=True,exist_ok=True)
Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris')
ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
Gtk.Settings.get_default().set_property('gtk-icon-theme-name','Majoris')
Gtk.IconTheme.get_for_display(Gdk.Display.get_default()).add_search_path(str(root/'icons'))
w=Adw.Window(title='Majoris segmented corner validation');w.set_default_size(1000,700)
body=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=12);body.set_margin_top(20);body.set_margin_start(20);body.set_margin_end(20);w.set_content(body)
def settle():
 l=GLib.MainLoop();GLib.timeout_add(180,lambda:(l.quit(),False)[1]);l.run()
def nodes(x):
 yield x
 c=x.get_first_child()
 while c:yield from nodes(c);c=c.get_next_sibling()
def group(count,selected,cls='majoris-segmented',icons=False):
 box=Gtk.Box();box.add_css_class(cls);box.set_halign(Gtk.Align.START);buttons=[]
 for i in range(count):
  b=Gtk.ToggleButton(label=['General','Metadata','Permissions','Open With'][i])
  if icons:b.set_child(Gtk.Image.new_from_icon_name(['view-grid-symbolic','view-list-symbolic','view-dual-symbolic','view-paged-symbolic'][i]))
  if buttons:b.set_group(buttons[0])
  buttons.append(b);box.append(b)
 buttons[selected].set_active(True);body.append(box);return box,buttons
custom,buttons=group(3,0);two,_=group(2,1);four,four_buttons=group(4,3);four_buttons[2].set_sensitive(False)
toolbar,tb=group(4,0,'majoris-toolbar-segmented',True)
legacy,_=group(3,1,'majoris-toolbar-view-switcher',True)
stack=Gtk.Stack()
for name in ('General','Metadata','Permissions'):stack.add_titled(Gtk.Label(label=name),name,name)
switch=Gtk.StackSwitcher(stack=stack);switch.set_halign(Gtk.Align.START);body.append(switch);body.append(stack)
vs=Adw.ViewStack()
for name in ('General','Metadata','Permissions','Open With'):
 p=vs.add_titled(Gtk.Label(label=name),name,name);p.set_icon_name('document-properties-symbolic')
adw=Adw.ViewSwitcher(stack=vs,policy=Adw.ViewSwitcherPolicy.WIDE);adw.set_halign(Gtk.Align.START);body.append(adw);body.append(vs)
bar=Adw.ViewSwitcherBar(stack=vs,reveal=True);body.append(bar)
w.present();settle()
lib=ctypes.CDLL('libgtk-4.so.1');lib.gtk_snapshot_to_node.argtypes=[ctypes.c_void_p];lib.gtk_snapshot_to_node.restype=ctypes.c_void_p
lib.gsk_render_node_write_to_file.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p];lib.gsk_render_node_write_to_file.restype=ctypes.c_int
lib.gsk_render_node_unref.argtypes=[ctypes.c_void_p]
def render(widget,name):
 snap=Gtk.Snapshot();Gtk.WidgetPaintable.new(widget).snapshot(snap,widget.get_allocated_width(),widget.get_allocated_height())
 node=lib.gtk_snapshot_to_node(hash(snap));assert node,name
 path=out/(name+'.node');assert lib.gsk_render_node_write_to_file(node,str(path).encode(),None);lib.gsk_render_node_unref(node)
 return path.read_text()
def capture(name):
 path=out/(name+'.xwd');subprocess.run(['xwd','-silent','-id',str(w.get_surface().get_xid()),'-out',str(path)],check=True)
 subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
def geometry():
 return {name:{'width':x.get_allocated_width(),'height':x.get_allocated_height(),'padding':[x.get_style_context().get_padding().top,x.get_style_context().get_padding().right],'border':x.get_style_context().get_border().top,'segments':[[c.get_width(),c.get_height()] for c in nodes(x) if isinstance(c,Gtk.ToggleButton)]} for name,x in subjects.items()}
subjects={'custom-segmented':custom,'two-segments':two,'four-segments':four,'toolbar-segmented':toolbar,'legacy-toolbar':legacy,'gtk-stack-switcher':switch,'adw-view-switcher':adw,'view-switcher-bar':bar}
baseline=geometry()
# Reconstruct only former radii to compare native allocations and pixels.
old=Gtk.CssProvider();old.load_from_data(b'.majoris-segmented, viewswitcher, stackswitcher, .majoris-toolbar-segmented, .majoris-toolbar-view-switcher { border-radius:8px; } .majoris-segmented button, viewswitcher button, stackswitcher button, .majoris-toolbar-segmented > button, .majoris-toolbar-view-switcher > button { border-radius:4px; }')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),old,1000);settle();capture('before');assert geometry()==baseline
before_node=render(custom,'before-custom')
assert re.search(r'outline: [^;]+ / 8;',before_node)
Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),old);settle();capture('after');assert geometry()==baseline
before=Image.open(out/'before.png').convert('RGBA');after=Image.open(out/'after.png').convert('RGBA')
assert ImageChops.difference(before,after).convert('RGB').getbbox(),'Radius change must alter native pixels'
for name,x in subjects.items():
 ok,bounds=x.compute_bounds(w);assert ok
 rect=(round(bounds.get_x()*scale),round(bounds.get_y()*scale),round((bounds.get_x()+bounds.get_width())*scale),round((bounds.get_y()+bounds.get_height())*scale))
 after.crop(rect).save(out/(name+'.png'))
after_node=render(custom,'after-custom')
assert re.findall(r'(?:color|font|glyphs): [^;]+;',before_node)==re.findall(r'(?:color|font|glyphs): [^;]+;',after_node),'Native colors, fonts or glyphs changed'
radius_evidence={}
for name,x in subjects.items():
 text=render(x,name)
 if name!='view-switcher-bar':
  assert re.search(r'outline: [^;]+ / 4;',text),(name,'outer radius')
  assert re.search(r'(?:outline|clip): [^;]+ / 2;',text),(name,'selected radius')
  radius_evidence[name]={'outer':4,'inner':2,'source':'native GSK rounded outlines'}
# Inset focus cannot change dimensions or neighboring allocations.
assert baseline['toolbar-segmented']['height']==32
assert baseline['custom-segmented']['padding']==[2,2]
assert baseline['toolbar-segmented']['padding']==[3,3]

# Selected segment retains its geometry in all native visual states.
buttons[1].set_active(True)
for name,flag in [('hover',Gtk.StateFlags.PRELIGHT),('pressed',Gtk.StateFlags.ACTIVE),('disabled',Gtk.StateFlags.INSENSITIVE),('focused',Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE)]:
 buttons[1].set_state_flags(flag,False);settle()
 text=render(buttons[1],'selected-'+name)
 assert re.search(r'(?:outline|clip): [^;]+ / 2;',text),(name,'selected state corner')
 assert buttons[1].get_allocated_height()==28
 buttons[1].unset_state_flags(flag)
# Native selection and keyboard navigation (no custom controller).
for i,name in enumerate(('selected-first','selected-middle','selected-last')):
 buttons[i].set_active(True);settle();assert sum(b.get_active() for b in buttons)==1;capture(name)
 assert all(geometry()[k]['height']==v['height'] for k,v in baseline.items())
buttons[1].grab_focus();w.set_focus_visible(True);settle();capture('keyboard-focus');assert all(geometry()[k]['height']==v['height'] for k,v in baseline.items())
focus={'visible':w.get_focus_visible(),'focused':buttons[1].has_focus(),'height_unchanged':all(geometry()[k]['height']==v['height'] for k,v in baseline.items())}
assert focus['visible'] and focus['focused']
# Dispatch actual X11 pointer and keyboard events to the native controls.
def key(key):subprocess.run(['xdotool','key','--window',str(w.get_surface().get_xid()),key],check=True);settle()
buttons[0].set_active(True);settle()
ok,bounds=buttons[2].compute_bounds(w);assert ok
subprocess.run(['xdotool','mousemove','--window',str(w.get_surface().get_xid()),str(round((bounds.get_x()+bounds.get_width()/2)*scale)),str(round((bounds.get_y()+bounds.get_height()/2)*scale)),'click','1'],check=True);settle();assert buttons[2].get_active()
key('Tab');key('shift+Tab');buttons[0].grab_focus();key('Right');key('space')
assert sum(b.get_active() for b in buttons)==1
stack.set_visible_child_name('Permissions');vs.set_visible_child_name('Open With');settle()
assert stack.get_visible_child_name()=='Permissions' and vs.get_visible_child_name()=='Open With'
assert not four_buttons[2].get_sensitive()
d=Adw.PreferencesDialog(title='File Properties')
for name in ('General','Metadata','Permissions','Open With'):
 page=Adw.PreferencesPage(title=name,icon_name='document-properties-symbolic');g=Adw.PreferencesGroup(title=name);g.add(Adw.ActionRow(title='Native file properties',subtitle='Segmented controls: 4px outer / 2px inner'));page.add(g);d.add(page)
d.present(w);settle();capture('preferences-dialog')
real=[x for x in nodes(d) if isinstance(x,Adw.ViewSwitcher)]
assert real,'PreferencesDialog must expose actual native view switchers'
hierarchy=[{'type':type(x).__name__,'node':x.get_css_name(),'classes':x.get_css_classes()} for x in nodes(d)]
for i,x in enumerate(real):
 if x.get_width()>0 and x.get_mapped():
  text=render(x,'preferences-switcher-'+str(i))
  assert re.search(r'outline: [^;]+ / 4;',text)
  assert re.search(r'(?:outline|clip): [^;]+ / 2;',text)
  radius_evidence['preferences-switcher-'+str(i)]={'outer':4,'inner':2,'source':'realized PreferencesDialog GSK node'}
(out/'radius-validation.json').write_text(json.dumps(radius_evidence,indent=2))
(out/'segmented-dimensions.json').write_text(json.dumps(baseline,indent=2))
(out/'focus-states.json').write_text(json.dumps(focus,indent=2))
(out/'preferences-hierarchy.json').write_text(json.dumps(hierarchy,indent=2))
print('Native segmented allocations, selection, focus and PreferencesDialog verified:',out)
d.close();w.destroy()
