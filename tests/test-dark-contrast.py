"""Informational contrast measurements preserve the supplied palette."""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools'))
from design import extract,html_value
t=extract('dark')
def rgb(s):
 if s.startswith('#'):return [int(s[i:i+2],16)/255 for i in (1,3,5)]
 import re
 v=[float(x) for x in re.findall(r'[\d.]+',s)]
 return [v[i]/255*v[3]+int(t['color']['surface'][1+i*2:3+i*2],16)/255*(1-v[3]) for i in range(3)]
def luminance(v):return sum(w*(c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4) for w,c in zip((.2126,.7152,.0722),v))
pairs={k:(t['color'][k],t['color']['surface']) for k in ('text','text_secondary','text_tertiary')}
for name,sel in [('navigation','.nav.active'),('banner','.banner'),('toast','.toast'),('tooltip','.tooltip')]:pairs[name]=(html_value(t,sel,'color'),html_value(t,sel,'background'))
ratios={}
for name,(fg,bg) in pairs.items():
 a,b=sorted((luminance(rgb(fg)),luminance(rgb(bg))));ratios[name]=round((b+.05)/(a+.05),2)
 assert ratios[name]>2,'Clearly unusable contrast: '+name
(root/'artifacts').mkdir(exist_ok=True)
(root/'artifacts/dark-contrast.json').write_text(json.dumps({'policy':'informational; only <=2:1 fails as clearly unusable; no palette rewrite','ratios':ratios},indent=2)+'\n')
print(json.dumps(ratios,indent=2))
