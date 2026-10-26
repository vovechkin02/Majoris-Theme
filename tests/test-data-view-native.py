"""Measure real Vala factory views, Pango ink and rendered selection pixels."""
import os,json,subprocess,time
from PIL import Image
from data_native import Session,ROOT
scale=int(os.environ.get('GDK_SCALE','1'));reports=[]
with Session() as s:
 for variant in ('light','dark'):
  for family in ('grid','list','column'):
   for compact in (False,True):
    mode='data-'+family+('-compact' if compact else '')
    d=s.start(mode,variant);target=32 if compact else 40
    for c in d['cells']:
     assert c['text'] and c['tooltip']==c['name'],c
     if c['column']==0:assert c['text']==c['name'],c
     assert c['size']==(12 if c['column']>0 else 14),c
     assert c['weight']==(400 if c['column']>0 else 500),c
     assert 'Plus Jakarta Sans' in c['font'],c
     assert c['ink'][1]>=0 and c['ink'][1]+c['ink'][3]<=c['label'][3],c
     assert c['logical'][3]<=c['label'][3],c
     if family=='grid':
      assert c['bounds'][2:]==([96,128] if compact else [128,160]),c
      assert c['artwork'][2:]==([64,64] if compact else [96,96]),c
      assert c['lines']<=2,c
      assert c['artwork'][1]-c['bounds'][1]==8,c
      assert c['label'][1]-(c['artwork'][1]+c['artwork'][3])==8,c
     else:
      assert c['owner'][3]==target,c
      if c['column']==0:
       assert c['icon'][2:]==[16,16],c
       assert c['label'][0]-(c['icon'][0]+16)==8,c
    if family=='column':
     assert d['header_bounds'][3]==32,d['header_bounds']
     assert d['header_fonts']==[[12,600]]*4,d['header_fonts']
     want=(98,98,105) if variant=='light' else (169,169,176)
     for rgba in d['header_foregrounds']:assert tuple(round(v*255) for v in rgba[:3])==want and rgba[3]==1,rgba
    selected=[c for c in d['cells'] if c['selected'] and c['column']==0];assert selected,d
    xwd=ROOT/'artifacts/data-view-finalisation/geometry'/f'{mode}-{variant}-{scale}x.xwd';png=xwd.with_suffix('.png')
    subprocess.run(['xwd','-silent','-id',s.wid,'-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
    c=selected[0];rect=c['bounds'] if family=='grid' else c['owner'];x,y,w,h=rect
    sample=Image.open(png).convert('RGB').getpixel((round((x+w-8+s.inset[0])*scale),round((y+h-8+s.inset[1])*scale)))
    expected=(238,242,255) if variant=='light' else (43,43,68)
    assert max(abs(a-b) for a,b in zip(sample,expected))<=1,(mode,variant,sample,expected)
    if family=='grid':
     image=Image.open(png).convert('RGB')
     for item in (c for c in d['cells'] if c['id'] in (2,6,7)):
      ax,ay,aw,ah=item['artwork'];ax=round((ax+s.inset[0])*scale);ay=round((ay+s.inset[1])*scale);aw=round(aw*scale);ah=round(ah*scale)
      pixels=image.load();points=[(px,py) for py in range(ay,ay+ah) for px in range(ax,ax+aw) if pixels[px,py] in ((99,102,241),(199,210,254),(55,48,163))]
      assert points,('thumbnail missing',item)
      tw=max(x for x,y in points)-min(x for x,y in points)+1;th=max(y for x,y in points)-min(y for x,y in points)+1
      ratio=160/90 if item['id']==2 else 90/160 if item['id']==6 else 1
      assert abs(tw/th-ratio)<.06,(item['id'],tw,th,ratio)
      ix,iy,iw,ih=item['picture'];assert abs(iw/ih-ratio)<.06,('picture frame ratio',item)
      corner=image.getpixel((round((ix+s.inset[0])*scale),round((iy+s.inset[1])*scale)))
      surface=(255,255,255) if variant=='light' else (32,32,35)
      assert max(abs(a-b) for a,b in zip(corner,surface))<=1,('rounded thumbnail corner',item['id'],corner,surface)
    reports.append(d|{'variant':variant,'scale':scale,'selection_pixel':sample})
(ROOT/'artifacts/data-view-finalisation/geometry'/f'native-{scale}x.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Native grid/list/column allocations, densities, Pango ink, font weights, icons, headers and selection pixels passed')
