import sys
from pathlib import Path
import gi
version=sys.argv[1]
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk
Gtk.init([]) if version=='3' else Gtk.init()
root=Path(__file__).resolve().parents[1]
errors=[]
for name in ('colors.css','gtk.css','gtk-dark.css'):
    provider=Gtk.CssProvider()
    provider.connect('parsing-error',lambda p,s,e:errors.append(f'{name}: {e.message}'))
    try: provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0'/name))
    except Exception as e: errors.append(str(e))
assert not errors,'\n'.join(errors)
print('GTK'+version+' native CSS parser passed')
