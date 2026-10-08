"""Native light/dark/automatic switching on the same realized GTK4 widgets."""
import ctypes,json,os,tempfile,gi,time
from pathlib import Path
gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
from gi.repository import Gtk,Adw,Gio,GLib
root=Path(__file__).resolve().parents[1]
os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris')
# Private in-memory settings prevent any desktop preferences being changed.
settings=Gio.Settings.new('org.gnome.desktop.interface')
original=settings.get_string('color-scheme')
Adw.init();manager=Adw.StyleManager.get_default()
bridge=ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so'));bridge.majoris_theme_attach()
window=Adw.Window();label=Gtk.Label(label='Native theme switching probe');window.set_content(label);window.present()
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(220,lambda:(loop.quit(),False)[1]);loop.run()
def colour():
 c=label.get_style_context().get_color();return '#'+''.join(f'{round(v*255):02X}' for v in (c.red,c.green,c.blue))
results=[]
try:
 for scheme,dark in [(Adw.ColorScheme.FORCE_LIGHT,False),(Adw.ColorScheme.FORCE_DARK,True),(Adw.ColorScheme.FORCE_LIGHT,False)]:
  manager.set_color_scheme(scheme);settle()
  tokens=json.loads((root/('design/tokens-dark.json' if dark else 'design/tokens.json')).read_text())
  assert manager.get_dark()==dark
  assert colour()==tokens['color']['text'],(dark,colour(),tokens['color']['text'])
  results.append({'mode':scheme.value_nick,'dark':manager.get_dark(),'rendered_label_colour':colour()})
 manager.set_color_scheme(Adw.ColorScheme.DEFAULT);settle()
 for preference in ('prefer-dark','default','prefer-dark','default'):
  settings.set_string('color-scheme',preference);Gio.Settings.sync();settle()
  results.append({'mode':'system','preference':preference,'dark':manager.get_dark(),'rendered_label_colour':colour(),'supports_system':manager.get_system_supports_color_schemes()})
  if manager.get_system_supports_color_schemes(): assert manager.get_dark()==(preference=='prefer-dark'),results[-1]
finally:
 settings.set_string('color-scheme',original);Gio.Settings.sync();window.destroy()
(root/'artifacts/variant-switching.json').write_text(json.dumps({'backend':'memory; original setting restored in finally','results':results},indent=2)+'\n')
print(json.dumps(results,indent=2))
