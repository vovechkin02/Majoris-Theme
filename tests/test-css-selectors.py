from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
required={'gtk-3.0/gtk.css':['decoration','headerbar','button.titlebutton','popover.background','menu','menuitem','scrollbar slider'],
          'gtk-4.0/gtk.css':['window.csd','window.background','window.solid-csd','headerbar','windowcontrols','popover > contents','button.model','.boxed-list','.navigation-sidebar','scrollbar slider'],
          'gnome-shell/gnome-shell.css':['.popup-menu-content','.popup-menu-item','.panel-button','.quick-toggle','.modal-dialog','.search-entry']}
for file,selectors in required.items():
    css=(root/'theme/Majoris'/file).read_text()
    css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
    heads=[s.strip() for block in re.findall(r'([^{}]+)\{[^{}]*\}',css) for s in block.split(',')]
    for selector in selectors: assert any(selector==s or s.startswith(selector+':') or s.startswith(selector+' ') for s in heads),(file,selector)
    assert css.count('{')==css.count('}') and r'\n' not in css
    assert not re.search(r'(?:^|[;{])\s*(?:transform|translate)\s*:',css)
print('Selector coverage and stationary interaction checks passed; geometry test exercises native controls')
