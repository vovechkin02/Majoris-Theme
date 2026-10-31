"""Consolidate completed native Phase 2 evidence; never modify screenshots."""
from pathlib import Path
import json,shutil
root=Path(__file__).resolve().parents[1];out=root/'artifacts/phase2-controls';geometry=out/'geometry';geometry.mkdir(parents=True,exist_ok=True)
controls=['calendar','linkbutton','editablelabel','paned','flowbox','expander','searchbar'];reports={name:{} for name in controls};fonts={};renderers={};inputs={};pixels={};focus={}
for toolkit in ['gtk4','gtk3']:
 for path in sorted((out/toolkit).glob('*/*/interactions.json')):
  profile=path.parent;key='/'.join(profile.relative_to(out).parts)
  inputs[key]=json.loads(path.read_text());renderers[key]=json.loads((profile/'renderer.json').read_text());fonts[key]=json.loads((profile/'text-metrics.json').read_text());pixels[key]=json.loads((profile/'glyph-pixels.json').read_text());focus[key]=json.loads((profile/'focus-indicators.json').read_text()) if (profile/'focus-indicators.json').exists() else {'available':False,'reason':'See native state screenshots'}
  for name in controls:
   file=profile/(name+'.json');reports[name][key]=json.loads(file.read_text()) if file.exists() else {'available':False,'reason':'Gtk.EditableLabel is GTK4-only'}
for name,values in {**reports,'text-metrics':fonts,'renderers':renderers,'interactions':inputs,'glyph-pixels':pixels,'focus-indicators':focus}.items():(geometry/(name+'.json')).write_text(json.dumps(values,indent=2)+'\n')
for variant in ['light','dark','light-2x','dark-2x']:
 target=out/variant;target.mkdir(exist_ok=True)
 for name in ['calendar','links','editable-label','paned','flowbox','expander','searchbar']:
  shutil.copy2(out/'factory'/variant/('phase2-'+name+'.png'),target/(name+'.png'))
states=out/'states';states.mkdir(exist_ok=True)
for state in ['hover','pressed','focus','disabled','backdrop']:
 shutil.copy2(out/'gtk4/light/cairo-1x'/('link-'+state+'.png'),states/(state+'.png'))
shutil.copy2(out/'gtk4/light/cairo-1x/flowbox.png',states/'selection.png')
comparison=out/'comparison';comparison.mkdir(exist_ok=True)
shutil.copy2(out/'comparison-before/light/phase2-calendar.png',comparison/'previous.png');shutil.copy2(out/'factory/light/phase2-calendar.png',comparison/'final.png')
summary={'native_profiles':len(inputs),'primary_gtk4':sum(k.startswith('gtk4/') for k in inputs),'compatibility_gtk3':sum(k.startswith('gtk3/') for k in inputs),'renderer_types':sorted({v['actual'] for v in renderers.values()})}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
