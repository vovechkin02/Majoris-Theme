"""Real GTK window style rendering: opaque normal window, transparent desktop class."""
import gi,sys,json
from pathlib import Path
import cairo
root=Path(__file__).resolve().parents[1];version=sys.argv[1]
gi.require_version('Gtk',version+'.0');from gi.repository import Gtk,Gdk,GLib
if version=='3':Gtk.init([])
else:Gtk.init()
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(120,lambda:(loop.quit(),False)[1]);loop.run()
out=root/'artifacts/desktop-window-probes';out.mkdir(parents=True,exist_ok=True);results=[]
for variant in ('light','dark'):
 provider=Gtk.CssProvider();provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 if version=='3':Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
 else:Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
 window=Gtk.Window();window.set_decorated(False);window.set_default_size(200,160)
 if version=='3':window.show_all()
 else:window.present()
 context=window.get_style_context();context.add_class('csd');settle()
 for desktop in (False,True,False):
  if desktop:context.add_class('desktopwindow')
  else:context.remove_class('desktopwindow')
  for state in (Gtk.StateFlags.NORMAL,Gtk.StateFlags.BACKDROP):
   window.set_state_flags(state,True);settle();window.set_state_flags(state,True)
   surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,200,160);cr=cairo.Context(surface)
   Gtk.render_background(context,cr,0,0,200,160);Gtk.render_frame(context,cr,0,0,200,160);surface.flush()
   alpha=bytes(surface.get_data())[3::4]
   if desktop:assert max(alpha)==0,(version,variant,state,'desktop paint remains',max(alpha))
   else:assert alpha[80*200+100]==255,(version,variant,state,'control window must stay opaque')
   name=f'gtk{version}-{variant}-'+('desktop' if desktop else 'regular')+('-backdrop' if state==Gtk.StateFlags.BACKDROP else '-active')
   surface.write_to_png(str(out/(name+'.png')))
   results.append({'variant':variant,'desktop':desktop,'state':'backdrop' if state==Gtk.StateFlags.BACKDROP else 'active','maximum_alpha':max(alpha),'center_alpha':alpha[80*200+100]})
 window.destroy();settle()
 if version=='3':Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),provider)
 else:Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),provider)
(out/f'gtk{version}.json').write_text(json.dumps(results,indent=2)+'\n')
print('GTK'+version+' native desktop paints transparent in both schemes/states; removing class restores opaque application backgrounds')
