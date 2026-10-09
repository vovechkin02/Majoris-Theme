"""Full-frame surgical baseline comparison. Original and final images remain untouched."""
import json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'artifacts';results=[]
for variant in ['light','dark']:
 for p in sorted((out/'screenshots'/variant).glob('*.png')):
  old=out/'baseline-final-fixes'/variant/p.name
  item={'variant':variant,'file':p.name}
  if not old.exists():item['status']='new diagnostic'
  else:
   a=Image.open(old).convert('RGB');b=Image.open(p).convert('RGB')
   assert a.size==b.size,(p,a.size,b.size)
   diff=ImageChops.difference(a,b);count=sum(n for n,c in diff.getcolors(a.width*a.height) if c!=(0,0,0))
   item.update(changed_pixels=count,percent=round(100*count/(a.width*a.height),5),bbox=diff.getbbox(),status='identical' if count==0 else 'changed')
  results.append(item)
(out/'final-fixes-baseline-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
for variant in ['light','dark']:
 rows=[x for x in results if x['variant']==variant];print(variant,{key:sum(x['status']==key for x in rows) for key in ['identical','changed','new diagnostic']})
