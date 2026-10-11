import json,os,subprocess,tempfile
import tinycss2
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    env={**os.environ,'XDG_CONFIG_HOME':d+'/config','XDG_DATA_HOME':d+'/data','XDG_STATE_HOME':d+'/state'}
    css=Path(d)/'config/gtk-4.0/gtk.css'; css.parent.mkdir(parents=True); css.write_text('original user CSS')
    command=['python3',str(root/'tools/dev-install.py')]
    subprocess.run(command+['install'],env=env,check=True)
    subprocess.run(command+['install'],env=env,check=True)
    subprocess.run(command+['install','--variant=light'],env=env,check=True)
    assert css.resolve()==root/'theme/Majoris/gtk-4.0/gtk.css'
    subprocess.run(command+['install','--variant=dark'],env=env,check=True)
    assert css.resolve().name=='gtk-dark.css'
    assert (css.parent/'colors-dark.css').is_file() and (css.parent/'assets/spinner-dark.svg').is_file()
    subprocess.run(command+['install','--variant=auto'],env=env,check=True)
    assert css.resolve()==root/'integration/gtk4-auto.css'
    assert css.resolve() not in [root/'theme/Majoris/gtk-4.0/gtk.css',root/'theme/Majoris/gtk-4.0/gtk-dark.css']
    assert tinycss2.parse_stylesheet(css.read_text(),skip_comments=True,skip_whitespace=True)==[],'Auto CSS must have no declarations or imports'
    assert css.is_symlink()
    journal=Path(d)/'state/majoris-theme/install.json'
    records=json.loads(journal.read_text())
    assets=Path(d)/'config/gtk-4.0/assets'
    assets.unlink()
    legacy=[r for r in records if r['path']!=str(assets)]
    journal.write_text(json.dumps(legacy))
    subprocess.run(command+['install'],env=env,check=True)
    migrated=json.loads(journal.read_text())
    assert migrated[:len(legacy)]==legacy,'Existing backups changed during asset migration'
    assert assets.is_symlink() and (assets/'spinner.svg').is_file()
    css.unlink(); css.write_text('subsequent edit')
    assert subprocess.run(command+['uninstall'],env=env,capture_output=True).returncode!=0
    assert css.read_text()=='subsequent edit'
    css.unlink(); css.symlink_to(root/'integration/gtk4-auto.css')
    subprocess.run(command+['uninstall'],env=env,check=True)
    assert css.read_text()=='original user CSS'
    assert not (Path(d)/'config/gtk-4.0/colors.css').exists()
print('Installer repeatability, conflict protection and restore passed')

# Each explicit mode is independently reversible, including pre-existing symlinks.
for mode in ('light','dark','auto'):
 for original_link in (False,True):
  with tempfile.TemporaryDirectory() as d:
   env={**os.environ,'XDG_CONFIG_HOME':d+'/config','XDG_DATA_HOME':d+'/data','XDG_STATE_HOME':d+'/state'}
   css=Path(d)/'config/gtk-4.0/gtk.css';css.parent.mkdir(parents=True)
   original=Path(d)/'original.css';original.write_text('original user CSS')
   if original_link:css.symlink_to(original)
   else:css.write_text(original.read_text())
   subprocess.run(command+['install','--variant='+mode],env=env,check=True)
   expected=root/('integration/gtk4-auto.css' if mode=='auto' else 'theme/Majoris/gtk-4.0/'+('gtk-dark.css' if mode=='dark' else 'gtk.css'))
   assert css.is_symlink() and css.resolve()==expected
   subprocess.run(command+['uninstall'],env=env,check=True)
   assert css.read_text()=='original user CSS' and css.is_symlink()==original_link
print('Light/dark/neutral-auto entrypoints, file and symlink backups, reversible mode transitions passed')
