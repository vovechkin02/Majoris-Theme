"""Contracts against the authoritative effective dark cascade, not screenshot labels."""
import hashlib,json,re,sys
from pathlib import Path
import tinycss2
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'))
from design import extract,html_value,icons
assert hashlib.sha256((root/'design/reference/majoris-widget-factory-dark.html').read_bytes()).hexdigest()=='0d316633f2130435052c5a43301963d6d9a260e44c940c1d03515fc3a87c1a74'
assert icons(root/'design/reference/majoris-widget-factory-dark.html')==icons(),'Dark reference must retain all four exact window SVGs'
stored=json.loads((root/'design/tokens-dark.json').read_text());assert stored==extract('dark')
light=json.loads((root/'design/tokens.json').read_text())
assert stored['color']['background']=='#18181B' and light['color']['background']!='#18181B'
assert all(stored[k]==light[k] for k in ('radius','window','motion','motion_css','font'))
assert stored['shadow']['control']!=light['shadow']['control']
assert stored['shadow']['card']!=stored['shadow']['pop']!=stored['shadow']['window']
expected={'background':'#18181B','surface':'#202023','surface_secondary':'#28282C','hover':'#303035','active':'#38383D','border':'#3B3B40','border_soft':'#313136','text':'#F4F4F5','text_secondary':'#A9A9B0','text_tertiary':'#7F7F88'}
assert all(stored['color'][k]==v for k,v in expected.items())
def rules(css):
 result={}
 for rule in tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True):
  if rule.type!='qualified-rule':continue
  ds={d.name:tinycss2.serialize(d.value).strip() for d in tinycss2.parse_declaration_list(rule.content,skip_comments=True,skip_whitespace=True) if d.type=='declaration'}
  for sel in tinycss2.serialize(rule.prelude).split(','):result.setdefault(sel.strip(),{}).update(ds)
 return result
contracts=[('headerbar','background-color','.headerbar','background'),('button.suggested-action:hover','background-color','.btn.primary:hover','background'),('button.suggested-action:active','background-color','.btn.primary:active','background'),('button.destructive-action:hover','background-color','.btn.danger:hover','background'),('button.destructive-action:active','background-color','.btn.danger:active','background'),('.sidebar','background-color','.sidebar','background'),('.sidebar row:selected','color','.nav.active','color'),('.majoris-data-view row:selected','color','.table-row.selected','color'),('scale slider','box-shadow','.thumb','box-shadow'),('switch slider','background-color','.switch:after','background'),('tooltip','background-color','.tooltip','background'),('tooltip label','color','.tooltip','color'),('tooltip','box-shadow','.tooltip','box-shadow'),('menuitem:hover','background-color','.menu-item:hover','background'),('card','box-shadow','.card','box-shadow')]
for version in ('3','4'):
 css=(root/f'theme/Majoris/gtk-{version}.0/gtk-dark.css').read_text();native=rules(css)
 for selector,prop,htmlsel,htmlprop in contracts:
  if selector=='card':selector='.card'
  assert native[selector][prop]==html_value(stored,htmlsel,htmlprop),(version,selector,prop,native[selector][prop],html_value(stored,htmlsel,htmlprop))
 assert native['.boxed-list']['box-shadow']=='none'
 assert native['windowcontrols > button:hover']['box-shadow']=='none'
 assert native['windowcontrols > button:backdrop']['color']=='#666670'
 if version=='4': assert native['banner']['padding']=='0' and native['banner']['border']=='none'
 if version=='4': assert native['banner > revealer > widget']['background-color']==html_value(stored,'.banner','background')
 if version=='4': assert native['toast']['background-color']==html_value(stored,'.toast','background')
 if version=='4': assert native['statuspage image.icon']['color']==html_value(stored,'.status .icon','color')
 assert native['spinner']['-gtk-icon-source']=='url("assets/spinner-dark.svg")'
 svg=(root/f'theme/Majoris/gtk-{version}.0/assets/spinner-dark.svg').read_text()
 assert 'stroke="#34365D"' in svg and 'stroke="#818CF8"' in svg and 'stroke-width="2"' in svg
 for decls in native.values():
  if 'transition' in decls:assert not any(p in decls['transition'] for p in ('margin','padding','transform','min-height','min-width'))
  for key in ('border-radius',):
   if key in decls: assert not re.search(r'\b(?:10|12|16|20|999)px\b',decls[key]),decls
print('Dark extraction, palette, semantic shadows, stationary motion, radii and native selector contracts passed')
