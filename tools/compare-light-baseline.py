"""Compare original and final full frames; no images are rewritten."""
import json
from pathlib import Path
from PIL import Image,ImageChops
root=Path(__file__).resolve().parents[1];baseline=root/'artifacts/baseline-light/screenshots';final=root/'artifacts/screenshots/light'
results=[]
for p in sorted(final.glob('*.png')):
 old=baseline/p.name
 if not old.exists():results.append({'file':p.name,'status':'new'});continue
 a=Image.open(old).convert('RGB');b=Image.open(p).convert('RGB');
 if a.size!=b.size:
  results.append({'file':p.name,'status':'size changed','before':a.size,'after':b.size});continue
 diff=ImageChops.difference(a,b);hist=diff.convert('L').histogram();changed=a.width*a.height-hist[0]
 results.append({'file':p.name,'changed_pixels':changed,'percent':round(changed/(a.width*a.height)*100,5),'bbox':diff.getbbox()})
(root/'artifacts/light-baseline-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
