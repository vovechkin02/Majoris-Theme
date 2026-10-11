"""Neutral development installation plus the unchanged native StyleManager bridge."""
import json,os,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if '--probe' in sys.argv:
 import ctypes,gi
 gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
 from gi.repository import Gtk,Adw,GLib
 Adw.init();bridge=ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so'));bridge.majoris_theme_attach()
 manager=Adw.StyleManager.get_default();window=Adw.Window();label=Gtk.Label(label='Auto development bridge');window.set_content(label);window.present()
 results=[]
 for dark in [False,True,False,True,False,True]:
  manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK if dark else Adw.ColorScheme.FORCE_LIGHT)
  loop=GLib.MainLoop();GLib.timeout_add(160,lambda:(loop.quit(),False)[1]);loop.run()
  colour=label.get_style_context().get_color();actual='#'+''.join(f'{round(v*255):02X}' for v in [colour.red,colour.green,colour.blue])
  assert actual==('#F4F4F5' if dark else '#1C1C1F'),(dark,actual)
  results.append({'dark':dark,'native_foreground':actual})
 window.destroy();print(json.dumps(results));sys.exit()
with tempfile.TemporaryDirectory(prefix='majoris-neutral-auto-') as tmp:
 env={**os.environ,'XDG_CONFIG_HOME':tmp+'/config','XDG_DATA_HOME':tmp+'/data','XDG_STATE_HOME':tmp+'/state','MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'GTK_A11Y':'none','GSK_RENDERER':'cairo'}
 css=Path(tmp)/'config/gtk-4.0/gtk.css';css.parent.mkdir(parents=True);css.write_text('/* Original user configuration */')
 command=[sys.executable,str(root/'tools/dev-install.py')]
 try:
  subprocess.run(command+['install','--variant=auto'],env=env,check=True,stdout=subprocess.DEVNULL)
  assert css.resolve()==root/'integration/gtk4-auto.css'
  child=subprocess.run([sys.executable,__file__,'--probe'],env=env,text=True,capture_output=True,check=True)
  assert 'Theme parser error' not in child.stderr and 'CRITICAL' not in child.stderr,child.stderr
  results=json.loads(child.stdout)
 finally:subprocess.run(command+['uninstall'],env=env,check=True,stdout=subprocess.DEVNULL)
 assert css.read_text()=='/* Original user configuration */' and not css.is_symlink()
out=root/'artifacts/auto-install-bridge.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(results,indent=2)+'\n')
print('Neutral auto installation and live GTK4 bridge both round trips passed; original user CSS restored')
