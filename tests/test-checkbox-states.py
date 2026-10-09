"""Real CheckButtons in six states, both schemes, GTK3 and GTK4; no app CSS."""
import gi,sys,subprocess,json
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1];version=sys.argv[1]
gi.require_version('Gtk',version+'.0');from gi.repository import Gtk,Gdk,GLib
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init()
else:Gtk.init([])
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(350,lambda:(loop.quit(),False)[1]);loop.run()
out=root/'artifacts/checkbox-probes';out.mkdir(parents=True,exist_ok=True)
for variant in ('light','dark'):
 provider=Gtk.CssProvider();provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 if version=='4':
  Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
  Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
  window=Adw.Window();window.set_title('Majoris checkbox probe');window.set_default_size(420,320)
 else:
  Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
  window=Gtk.Window(title='Majoris checkbox probe');window.set_default_size(420,320)
 box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=12)
 for prop in ('margin_top','margin_bottom','margin_start','margin_end'):getattr(box,'set_'+prop)(24)
 probes=[]
 for name in ['unchecked','checked','indeterminate','disabled unchecked','disabled checked','focus']:
  check=Gtk.CheckButton(label=name)
  check.set_active(name in ['checked','disabled checked']);check.set_inconsistent(name=='indeterminate');check.set_sensitive(not name.startswith('disabled'))
  if version=='4':box.append(check)
  else:box.pack_start(check,False,False,0)
  probes.append(check)
 if version=='4':window.set_content(box);window.present()
 else:window.add(box);window.show_all()
 settle();probes[-1].grab_focus();probes[-1].set_state_flags(Gtk.StateFlags.FOCUSED|(Gtk.StateFlags.FOCUS_VISIBLE if version=='4' else Gtk.StateFlags.NORMAL),False);settle()
 assert probes[2].get_inconsistent() and not probes[2].get_active()
 assert probes[1].get_active() and not probes[4].get_sensitive()
 assert all(c.get_allocated_height()>=16 for c in probes)
 wid=subprocess.check_output(['xdotool','search','--name','^Majoris checkbox probe$'],text=True).splitlines()[0]
 xwd=out/f'gtk{version}-{variant}.xwd';png=xwd.with_suffix('.png')
 subprocess.run(['xwd','-silent','-id',wid,'-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
 colours=Image.open(png).convert('RGB').getcolors(1000000)
 assert sum(n for n,c in colours if all(abs(c[i]-[79,70,229][i])<=2 for i in range(3)))>=2,(version,variant,'mixed p600 mark missing from actual native output')
 (out/f'gtk{version}-{variant}.json').write_text(json.dumps({'states':[c.get_label() for c in probes],'mixed_mark':'#4F46E5','rendered':str(png),'application_css':False},indent=2)+'\n')
 window.destroy();settle()
 if version=='4':Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),provider)
 else:Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),provider)
print('GTK'+version+' actual checkbox renders contain p600 mixed mark in light and dark; all six native states captured')
