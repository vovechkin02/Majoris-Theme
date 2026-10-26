"""Rendered native GTK state flags; input behavior has a separate real-event test."""
import os,time,json,subprocess
from PIL import Image
from data_native import Session,ROOT
out=ROOT/'artifacts/data-view-finalisation/geometry';reports=[]
expected={'light':{'hover':(236,236,239),'pressed':(226,226,230),'selected':(238,242,255),'selected-hover':(224,231,255),'selected-pressed':(199,210,254),'focus':(255,255,255),'disabled':(255,255,255)},'dark':{'hover':(48,48,53),'pressed':(56,56,61),'selected':(43,43,68),'selected-hover':(47,47,80),'selected-pressed':(51,52,93),'focus':(32,32,35),'disabled':(32,32,35)}}
with Session() as s:
 for variant in ('light','dark'):
  for family in ('grid','list','column'):
   for state in ('hover','pressed','selected','selected-hover','selected-pressed','focus','focus-selected','disabled','backdrop'):
    os.environ['MAJORIS_DATA_STATE']=state
    d=s.start('data-'+family+('-backdrop' if state=='backdrop' else ''),variant);time.sleep(1.2);d=s.read(lambda r:state!='backdrop' or not r['active'])
    identity=1 if 'selected' in state or state=='backdrop' else 0
    c=next(c for c in d['cells'] if c['id']==identity and c['column']==0);assert c['weight']==500 and c['size']==14,c
    assert c['role']!='GTK_ACCESSIBLE_ROLE_WIDGET',c
    x,y,w,h=c['bounds'] if family=='grid' else c['owner'];x+=s.inset[0];y+=s.inset[1]
    path=out/f'{family}-{variant}-{state}.xwd';png=path.with_suffix('.png');subprocess.run(['xwd','-silent','-id',s.wid,'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(png)],check=True)
    image=Image.open(png).convert('RGB');actual=image.getpixel((round(x+w-8),round(y+h-8)));want=expected[variant]['selected' if state in ('backdrop','focus-selected') else state]
    assert max(abs(a-b) for a,b in zip(actual,want))<=2,(family,variant,state,actual,want,c)
    if state in ('focus','focus-selected'):
     edge=image.getpixel((round(x+1),round(y+h/2)));focus=(99,102,241) if variant=='light' else (129,140,248);assert max(abs(a-b) for a,b in zip(edge,focus))<=2,(family,edge,focus)
    assert c['bounds'][3]==(160 if family=='grid' else 24 if family=='list' else 23),c
    reports.append({'family':family,'variant':variant,'state':state,'pixel':actual,'role':c['role'],'flags':c['flags'],'font_size':c['size'],'weight':c['weight'],'bounds':c['bounds'],'label':c['label'],'baseline':c['baseline']})
 os.environ.pop('MAJORIS_DATA_STATE',None)
for family in ('grid','list','column'):
 for variant in ('light','dark'):
  subset=[r for r in reports if r['family']==family and r['variant']==variant]
  assert len({r['baseline'] for r in subset})==1,subset
  assert len({r['label'][1]-r['bounds'][1] for r in subset})==1,subset
(out/'states.json').write_text(json.dumps(reports,indent=2)+'\n')
print('All three families: rendered hover, pressed, persistent selection combinations, focus, disabled and real inactive-window selection passed')
