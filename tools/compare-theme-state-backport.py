"""Backport source scope and complete uncropped screenshot/geometry comparison."""
import json
from pathlib import Path
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'artifacts';baseline=out/'pre-theme-state-backport'
for version in ('3','4'):
 for name in ('gtk.css','gtk-dark.css'):
  relative=Path(f'theme/Majoris/gtk-{version}.0')/name
  before=(baseline/relative).read_text();after=(ROOT/relative).read_text().split('/* Desktop Icons NG:',1)[0]
  lines=lambda value:[line.strip() for line in value.splitlines() if line.strip()]
  assert lines(before)==lines(after),(relative,'Regular application CSS changed')
for variant in ('light','dark'):
 assert json.loads((baseline/f'geometry-{variant}.json').read_text())==json.loads((out/f'geometry-{variant}.json').read_text()),(variant,'Geometry changed')
rows=[]
for variant in ('light','dark'):
 for old in sorted((baseline/'screenshots'/variant).glob('*.png')):
  final=out/'screenshots'/variant/old.name;assert final.is_file(),final
  a=Image.open(old).convert('RGB');b=Image.open(final).convert('RGB');assert a.size==b.size
  diff=ImageChops.difference(a,b);count=sum(n for n,c in diff.getcolors(a.width*a.height) if c!=(0,0,0))
  rows.append({'variant':variant,'file':old.name,'changed_pixels':count,'bbox':diff.getbbox(),'identical':count==0})
(out/'theme-state-backport-comparison.json').write_text(json.dumps({'regular_gtk_css_unchanged':True,'geometry_unchanged':True,'screenshots':rows},indent=2)+'\n')
for variant in ('light','dark'):
 subset=[r for r in rows if r['variant']==variant]
 print(variant,str(sum(r['identical'] for r in subset))+'/'+str(len(subset))+' full screenshots pixel-identical; complete geometry unchanged')
