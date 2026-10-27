"""Consolidate actual native metrics and screenshots, without image modification."""
import json,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'artifacts/universal-toolbar';geometry=out/'geometry';geometry.mkdir(parents=True,exist_ok=True)
source=root/'artifacts/toolbar-finalisation'
standard={};compact={};focus={};text={};factory={}
for version in ('3','4'):
 for scale in ('1','2'):
  for variant in ('light','dark'):
   name=variant+('-2x' if scale=='2' else '');path=source/name;key='gtk'+version+'-'+name
   def read(suffix):return json.loads((path/('gtk'+version+'-'+suffix+'.json')).read_text())
   standard[key]=read('measurements');compact[key]=read('compact');text[key+'-compact']=read('compact-text');focus[key]=read('focus-states');focus[key+'-compact-flat']=read('compact-focus');text[key]=read('text-metrics')
   if version=='4':factory[name]=json.loads((path/'factory-measurements.json').read_text())
   else:
    target=out/'gtk3'/name;target.mkdir(parents=True,exist_ok=True)
    for file in path.glob('gtk3-*.png'):shutil.copy2(file,target/file.name)
  for values in (standard,compact):assert values['gtk'+version+'-light'+('-2x' if scale=='2' else '')]==values['gtk'+version+'-dark'+('-2x' if scale=='2' else '')]
for name,values in [('toolbar-standard',standard),('toolbar-compact',compact),('focus-states',focus),('text-metrics',text),('factory',factory)]:
 (geometry/(name+'.json')).write_text(json.dumps(values,indent=2)+'\n')
for variant in ('light','dark','light-2x','dark-2x'):
 target=out/variant;target.mkdir(parents=True,exist_ok=True)
 for original,name in [('toolbars-navigation','navigation-example'),('toolbars-commands','commands-example'),('toolbars-editor','editor-example'),('toolbars-mixed','mixed-controls'),('toolbars-compact','compact-toolbar'),('toolbars','stacked-examples'),('toolbars-states','keyboard-focus'),('toolbars-narrow','narrow-window'),('toolbars-dynamic','dynamic-insertion'),('toolbars-popover','native-popover'),('toolbars','segmented-control')]:
  shutil.copy2(out/'factory'/variant/(original+'.png'),target/(name+'.png'))
print('Universal standard/compact geometry matches across palettes; native evidence consolidated')
