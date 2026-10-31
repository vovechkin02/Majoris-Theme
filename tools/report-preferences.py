"""Collect measured preferences evidence without modifying native captures."""
import json
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[1]
base=root/'artifacts/actionrow-finalisation';out=base/'geometry';out.mkdir(parents=True,exist_ok=True)
for name in ('actionrow-allocations','preferences-group-geometry','typography-metrics','interaction-states','label-reset-investigation'):
 records={str(p.parent.relative_to(base)):json.loads(p.read_text()) for p in base.glob('*/*/'+name+'.json')}
 (out/(name+'.json')).write_text(json.dumps(records,indent=2)+'\n')
renderers={str(p.parent.relative_to(base)):json.loads(p.read_text()) for p in base.glob('*/*/renderer-comparison.json')}
comparisons={}
for variant in ('light','dark'):
 for scale in (1,2):
  a=base/variant/f'cairo-{scale}x';b=base/variant/f'gl-{scale}x'
  if not (a/'typography-metrics.json').exists() or not (b/'typography-metrics.json').exists():continue
  left=json.loads((a/'typography-metrics.json').read_text());right=json.loads((b/'typography-metrics.json').read_text())
  same=left==right;assert same,('Renderer geometry differs',variant,scale)
  im1=Image.open(a/'long-subtitles.png').convert('RGB');im2=Image.open(b/'long-subtitles.png').convert('RGB');assert im1.size==im2.size
  difference=ImageChops.difference(im1,im2);histogram=difference.convert('L').histogram();fraction=1-histogram[0]/sum(histogram)
  comparisons[f'{variant}-{scale}x']={'same_text_metrics':same,'changed_pixel_fraction':fraction,'interpretation':'Raster differences alone do not establish corrupted glyphs; review unedited PNGs.'}
(out/'renderer-comparison.json').write_text(json.dumps({'runs':renderers,'cairo_gl_comparison':comparisons,'limitation':'Xvfb rendering does not reproduce the physical desktop GPU/Wayland environment.'},indent=2)+'\n')
print('Collected native preference measurements and renderer comparison:',out)
