"""Optional original-theme clipping probe. Never substitutes for current tests."""
import os,sys,json,subprocess,time,atexit
from pathlib import Path
os.environ['GSK_RENDERER']='cairo'
import gi
gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
from gi.repository import Gtk,Adw,Gdk,GLib,Pango
root=Path(__file__).resolve().parents[1];variant=os.environ.get('MAJORIS_VARIANT','light')
source=root/'artifacts/tab-finalisation/baseline-theme/gtk-4.0'
out=root/'artifacts/tab-finalisation/before'/variant;out.mkdir(parents=True,exist_ok=True)
Adw.init();provider=Gtk.CssProvider();provider.load_from_path(str(source/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);atexit.register(wm.terminate)
for attempt in range(40):
 if 'window id' in subprocess.check_output(['xprop','-root','_NET_SUPPORTING_WM_CHECK'],text=True):break
 time.sleep(.05)
w=Adw.Window(title='Majoris original tab clipping probe');w.set_default_size(1200,250)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL);w.set_content(box)
view=Adw.TabView(vexpand=True);bar=Adw.TabBar(view=view,autohide=False,expand_tabs=False);bar.add_css_class('majoris-document-tabs');box.append(bar);box.append(view)
for text in ['Favorites','Files','Find','Format','Documents','Downloads','Preferences','New Folder','gyp;!?']:
 page=view.append(Gtk.Label(label='Original generated theme — native Adw.TabBar'));page.set_title(text)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(250,lambda:(loop.quit(),False)[1]);loop.run()
def nodes(widget):
 yield widget
 child=widget.get_first_child()
 while child:yield from nodes(child);child=child.get_next_sibling()
w.present();settle();records=[]
for i in range(view.get_n_pages()):
 view.set_selected_page(view.get_nth_page(i));settle()
 for label in nodes(bar):
  if not isinstance(label,Gtk.Label) or not label.get_text():continue
  ink,logical=label.get_layout().get_pixel_extents();x,y=label.get_layout_offsets();metrics=label.get_pango_context().get_metrics(None,None)
  records.append(dict(text=label.get_text(),font=label.get_pango_context().get_font_description().to_string(),allocation=[label.get_allocated_width(),label.get_allocated_height()],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.width,logical.height],layout_origin=[x,y],baseline=label.get_layout().get_baseline()/Pango.SCALE,ascent=metrics.get_ascent()/Pango.SCALE,descent=metrics.get_descent()/Pango.SCALE,vertically_clipped=y+ink.y<0 or y+ink.y+ink.height>label.get_allocated_height()))
view.set_selected_page(view.get_nth_page(0));settle()
wid=subprocess.check_output(['xdotool','search','--name','^Majoris original tab clipping probe$'],text=True).splitlines()[0]
path=out/'original-favorites.xwd';subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
(out/'original-measurements.json').write_text(json.dumps({'strip_height':bar.get_allocated_height(),'labels':records},indent=2)+'\n')
print('Original native strip:',bar.get_allocated_height(),'clipped labels:',sum(item['vertically_clipped'] for item in records));w.destroy()
