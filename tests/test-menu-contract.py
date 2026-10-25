"""Menu source contract, supplementing the realized Pango/allocation matrix."""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'))
from design import html_value
variants={name:json.loads((root/'design'/('tokens'+('-dark' if name=='dark' else '')+'.json')).read_text()) for name in ('light','dark')}
for name,t in variants.items():
 def value(selector,prop):return html_value(t,selector,prop)
 for selector,prop,expected in [('.menu-item','min-height','32px'),('.menu-item','height','auto'),('.menu-item','padding','4px 8px'),('.menu-item','font-size','14px'),('.menu-item','font-weight','500'),('.menu-item','border-radius','4px'),('.popover','padding','8px'),('.popover','min-width','192px'),('.popover','border-radius','8px'),('.separator','height','1px'),('.separator','margin','4px 8px'),('.menu-item kbd','font-size','12px'),('.menu-item kbd','font-weight','400')]:
  assert value(selector,prop)==expected,(name,selector,prop,value(selector,prop))
 assert value('.popover','background')==('#28282C' if name=='dark' else '#FFFFFF')
 assert value('.menu-item:hover','background')==('#38383D' if name=='dark' else '#ECECEF')
 assert value('.menu-item:active','background')==('#424247' if name=='dark' else '#E2E2E6')
 assert value('.menu-item.destructive','color')==('#F06B79' if name=='dark' else '#DC3C4D')
print('Menu geometry, typography, opaque surfaces and semantic colours match both references')
