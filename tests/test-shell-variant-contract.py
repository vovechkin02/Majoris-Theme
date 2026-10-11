"""Exact values and light/dark round trips; white selected children remain valid."""
import sys,copy
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'))
from shell_contract import validate
css={v:(root/'theme/Majoris/gnome-shell'/('gnome-shell-dark.css' if v=='dark' else 'gnome-shell.css')).read_text() for v in ['light','dark']}
parsed={v:validate(source,v) for v,source in css.items()}
keys=lambda rules:{(sel,key) for sel,props in rules.items() for key in props if key in ('color','background-color','border-color','border')}
assert keys(parsed['light'])==keys(parsed['dark']),'Both variants must explicitly own the same colour-sensitive selectors'
for sequence in [('light','dark','light'),('dark','light','dark')]:
 loaded={}
 for variant in sequence:
  for selector,props in parsed[variant].items():loaded.setdefault(selector,{}).update(props)
  validate(loaded,variant)
  assert {sel:props for sel,props in loaded.items()}==parsed[variant],'Stale source properties survived the variant transition'
for variant,selector,prop,bad in [('dark','#panel','background-color','#FFFFFF'),('dark','.quick-settings','background-color','#FFFFFF'),('dark','.search-entry','background-color','#FFFFFF'),('light','#panel .panel-button StLabel','color','#FFFFFF'),('light','.quick-toggle StIcon','color','#FFFFFF'),('light','.quick-settings .icon-button:insensitive StIcon','color','#FFFFFF')]:
 broken=copy.deepcopy(parsed[variant]);broken[selector][prop]=bad
 try:validate(broken,variant)
 except AssertionError:pass
 else:raise AssertionError(('Specific regression was accepted',variant,selector,prop))
assert (root/'theme/Majoris-Dark/gnome-shell/gnome-shell.css').read_text()==css['dark']
print('Exact light/dark Shell values, descendant foregrounds, selected white children, insensitive controls and both source round trips passed')
