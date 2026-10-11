"""All generated GTK variants must own both desktop-window focus states."""
from css_contract import *
selectors=['window.desktopwindow','window.desktopwindow:backdrop','window.desktopwindow.background','window.desktopwindow.background:backdrop','.desktopwindow','.desktopwindow:backdrop']
for version in ('3','4'):
 for variant in ('light','dark'):
  css=rules(version,variant)
  for selector in selectors:
   for prop,value in {'background-color':'transparent','background-image':'none','border-color':'transparent','border-width':'0','border-radius':'0','box-shadow':'none'}.items():expect(css,selector,prop,value)
  # Equal-specificity window.csd rules must precede the desktop compatibility block.
  source=(ROOT/f'theme/Majoris/gtk-{version}.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')).read_text()
  assert source.rfind('window.desktopwindow')>source.rfind('window.csd {')
print('GTK3/4 light/dark desktop window normal/backdrop transparency contracts passed')
