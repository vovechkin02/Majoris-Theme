"""Verify actual Meson staged outputs and standard system data discovery."""
import os, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='majoris-theme-stage-') as directory:
 env={**os.environ,'DESTDIR':directory}
 subprocess.run(['meson','install','-C',str(root/'build'),'--no-rebuild'],env=env,check=True,stdout=subprocess.DEVNULL)
 data=Path(directory)/'usr/share'
 for name in ('majoris-light','majoris-dark'):
  assert (data/f'gtksourceview-5/styles/{name}.xml').is_file()
  assert (data/f'majoris-theme/design/sourceview/{name}.xml.in').is_file()
 assert (data/'applications/com.majoris.ThemeFactory.desktop').is_file()
 assert (Path(directory)/'usr/bin/majoris-theme-factory').is_file()
 for variant in ('gtk.css','gtk-dark.css'):
  assert (data/'themes/Majoris/gtk-4.0'/variant).is_file()
 probe="""import gi;gi.require_version('GtkSource','5')
from gi.repository import GtkSource
m=GtkSource.StyleSchemeManager.get_default()
assert all(m.get_scheme(id) for id in ('majoris-light','majoris-dark'))
"""
 subprocess.run([sys.executable,'-c',probe],env={**os.environ,'XDG_DATA_HOME':directory+'/empty','XDG_DATA_DIRS':str(data)+':/usr/share'},check=True)
print('DESTDIR /usr packaging and standard SourceView scheme discovery passed')
