"""GTK3 actual named-theme loading, preference toggles and GNOME auto adaptation."""
import gi,os,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if '--child' not in sys.argv:
 with tempfile.TemporaryDirectory(prefix='majoris-gtk3-selection-') as d:
  data=Path(d)/'data/themes';data.mkdir(parents=True);(data/'Majoris').symlink_to(root/'theme/Majoris')
  env={**os.environ,'XDG_CONFIG_HOME':d,'XDG_DATA_HOME':str(Path(d)/'data'),'GSETTINGS_BACKEND':'memory'}
  for variant in ('light','dark','auto'):
   child={**env,'GTK_THEME':'Majoris'+(':dark' if variant=='dark' else '')}
   if variant=='auto':
    child.pop('GTK_THEME',None);child['LD_PRELOAD']=str(root/'build/libmajoris-gtk3-theme.so')
   subprocess.run([sys.executable,__file__,'--child',variant],env=child,check=True)
 sys.exit()
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gio,GLib
Gtk.init([]);Gtk.Settings.get_default().set_property("gtk-enable-animations",False);window=Gtk.Window();window.set_default_size(600,400);button=Gtk.Button(label='Named native theme');window.add(button);window.show_all()
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(200,lambda:(loop.quit(),False)[1]);loop.run()
def check(dark):
 settle();state=Gtk.StateFlags.NORMAL;button.set_state_flags(state,True)
 c=button.get_style_context().get_background_color(state)
 assert tuple(round(v*255) for v in (c.red,c.green,c.blue))==((40,40,44) if dark else (255,255,255)),(dark,c.to_string())
 # Dark imports need explicit foreground resets for Adwaita's specific states.
 # Light's established native foreground treatment is preserved unchanged.
 for flag in ((Gtk.StateFlags.NORMAL,Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,Gtk.StateFlags.INSENSITIVE) if dark else (Gtk.StateFlags.NORMAL,)):
  button.set_state_flags(flag,True)
  colour=button.get_style_context().get_color(flag)
  assert tuple(round(v*255) for v in (colour.red,colour.green,colour.blue))==((244,244,245) if dark else (28,28,31)),(dark,flag,colour.to_string())
 button.set_state_flags(Gtk.StateFlags.NORMAL,True)
variant=sys.argv[-1]
if variant=='auto':
 settings=Gio.Settings.new('org.gnome.desktop.interface');original=settings.get_string('color-scheme')
 try:
  for v in ('default','prefer-dark','default'):
   settings.set_string('color-scheme',v);check(v=='prefer-dark')
 finally:settings.set_string('color-scheme',original)
else:check(variant=='dark')
window.destroy();print('GTK3 native '+variant+' selection passed')
