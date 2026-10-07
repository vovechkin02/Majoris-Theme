import os,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    env={**os.environ,'XDG_CONFIG_HOME':d+'/config','XDG_DATA_HOME':d+'/data','XDG_STATE_HOME':d+'/state'}
    css=Path(d)/'config/gtk-4.0/gtk.css'; css.parent.mkdir(parents=True); css.write_text('original user CSS')
    command=['python3',str(root/'tools/dev-install.py')]
    subprocess.run(command+['install'],env=env,check=True)
    subprocess.run(command+['install'],env=env,check=True)
    assert css.is_symlink()
    css.unlink(); css.write_text('subsequent edit')
    assert subprocess.run(command+['uninstall'],env=env,capture_output=True).returncode!=0
    assert css.read_text()=='subsequent edit'
    css.unlink(); css.symlink_to(root/'theme/Majoris/gtk-4.0/gtk.css')
    subprocess.run(command+['uninstall'],env=env,check=True)
    assert css.read_text()=='original user CSS'
    assert not (Path(d)/'config/gtk-4.0/colors.css').exists()
print('Installer repeatability, conflict protection and restore passed')
