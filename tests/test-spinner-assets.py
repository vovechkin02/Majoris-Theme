"""Verify the dark spinner's baked colours in actual native rendered windows."""
import gi,os,sys,subprocess,time,tempfile
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1];version=sys.argv[1]
gi.require_version('Gtk',version+'.0');from gi.repository import Gtk,Gdk,GLib
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init();window=Adw.Window();window.set_title('Majoris spinner asset probe')
else:
 Gtk.init([]);window=Gtk.Window(title='Majoris spinner asset probe')
window.set_default_size(200,200);Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
provider=Gtk.CssProvider();provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0/gtk-dark.css'))
if version=='4':Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
else:Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
spinner=Gtk.Spinner();spinner.set_halign(Gtk.Align.CENTER);spinner.set_valign(Gtk.Align.CENTER);spinner.start()
if version=='4':window.set_content(spinner);window.present()
else:window.add(spinner);window.show_all()
loop=GLib.MainLoop();GLib.timeout_add(500,lambda:(loop.quit(),False)[1]);loop.run()
wid=subprocess.check_output(['xdotool','search','--name','^Majoris spinner asset probe$'],text=True).splitlines()[0]
out=root/'artifacts/spinner-probes';out.mkdir(parents=True,exist_ok=True)
xwd=out/('gtk'+version+'.xwd');png=xwd.with_suffix('.png')
subprocess.run(['xwd','-silent','-id',wid,'-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
colours=Image.open(png).convert('RGB').getcolors(1000000)
assert colours is not None
for colour in [(52,54,93),(129,140,248)]:
 assert sum(n for n,c in colours if all(abs(c[i]-colour[i])<=2 for i in range(3)))>=2,(version,colour,'Dark SVG colour absent from realized GtkSpinner')
assert spinner.get_allocated_width()==20 and spinner.get_allocated_height()==20
window.destroy();print('GTK'+version+' dark spinner asset rendered at 20x20 with both exact stroke colours')
