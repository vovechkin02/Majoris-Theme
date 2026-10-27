"""Actual X11 input plus rendered pixels; never synthesize focus flags."""
import os,time,json,subprocess
from PIL import Image
from data_native import Session,ROOT
scale=int(os.environ.get('GDK_SCALE','1'));evidence=[]
base=ROOT/'artifacts/data-view-focus';geometry=base/'geometry';geometry.mkdir(parents=True,exist_ok=True)
VISIBLE=1<<13;WITHIN=1<<14;FOCUSED=1<<5

def rows(d):return [c for c in d['cells'] if c['column']==0]
def focus_rows(d):return [c for c in rows(d) if c['flags']&VISIBLE]
def settled(s):time.sleep(.26);return s.read()
def capture(s,d,family,variant,state,ring):
 out=base/(variant+('-2x' if scale==2 else ''));out.mkdir(parents=True,exist_ok=True)
 name=('details' if family=='column' else family)+'-'+state
 png=out/(name+'.png');xwd=png.with_suffix('.xwd')
 s.command('mousemove',0,0);time.sleep(.15);d=s.read()
 subprocess.run(['xwd','-silent','-id',s.wid,'-out',str(xwd)],check=True)
 subprocess.run(['magick',str(xwd),str(png)],check=True)
 image=Image.open(png).convert('RGB');accent=(99,102,241) if variant=='light' else (129,140,248)
 samples=[]
 for c in rows(d):
  x,y,w,h=c['bounds'] if family=='grid' else c['owner'];x+=s.inset[0];y+=s.inset[1]
  if y<0 or y+h>image.height/scale:continue
  pixel=image.getpixel((round((x+1)*scale),round((y+h/2)*scale)))
  is_ring=max(abs(a-b) for a,b in zip(pixel,accent))<=2
  wanted=bool(c['flags']&VISIBLE) and d['active'] and state!='disabled'
  assert is_ring==wanted,(family,variant,state,c['id'],c['flags'],pixel,wanted)
  if wanted:
   inside=image.getpixel((round((x+3)*scale),round((y+h/2)*scale)))
   assert max(abs(a-b) for a,b in zip(inside,accent))>2,('focus thicker than 2px',family,inside)
  samples.append({'id':c['id'],'edge':pixel,'ring':is_ring,'flags':c['flags']})
  # A Details cell must not paint a second vertical outline inside the row.
  if family=='column' and wanted:
   other=next(item for item in d['cells'] if item['id']==c['id'] and item['column']==1)
   cx=other['bounds'][0]-16+s.inset[0]
   interior=image.getpixel((round((cx+1)*scale),round((y+h/2)*scale)))
   assert max(abs(a-b) for a,b in zip(interior,accent))>2,('duplicate cell ring',interior)
 assert any(p['ring'] for p in samples)==ring,(family,state,samples)
 selected=[c for c in rows(d) if c['selected']]
 if selected and state!='disabled':
  c=selected[0];x,y,w,h=c['bounds'] if family=='grid' else c['owner']
  pixel=image.getpixel((round((x+w-48+s.inset[0])*scale),round((y+h-8+s.inset[1])*scale)))
  want=(238,242,255) if variant=='light' else (43,43,68)
  assert max(abs(a-b) for a,b in zip(pixel,want))<=2,(family,state,pixel,want)
  assert c['size']==14 and c['weight']==500
 evidence.append({'family':family,'variant':variant,'scale':scale,'interaction':state,'selected':d['selected'],'active':d['active'],'samples':samples,'nodes':d['nodes']})
 return d

with Session() as s:
 for variant in ('light','dark'):
  for family in ('grid','list','column'):
   d=s.start('data-'+family+'-multi',variant)
   # Pointer selection has FOCUS_WITHIN, but no FOCUS_VISIBLE.
   s.click(next(c['owner'] for c in rows(d) if c['id']==1));d=settled(s)
   assert d['selected']==[1] and not focus_rows(d)
   capture(s,d,family,variant,'mouse-selected',False)
   s.command('key','Right' if family=='grid' else 'Down');d=settled(s)
   assert focus_rows(d) and any(c['selected'] for c in focus_rows(d))
   capture(s,d,family,variant,'keyboard-focused',True)
   capture(s,d,family,variant,'selected-keyboard-focused',True)
   # Ctrl+arrow moves keyboard focus without moving selection.
   saved=d['selected'];s.command('key','ctrl+Right' if family=='grid' else 'ctrl+Down');d=settled(s)
   assert d['selected']==saved and focus_rows(d) and all(not c['selected'] for c in focus_rows(d)),d['selected']
   capture(s,d,family,variant,'keyboard-unselected',True)
   s.click(d['controls'][3]);d=settled(s);assert d['selected']==saved and not focus_rows(d)
   capture(s,d,family,variant,'selected-unfocused',False)
   # Return through real keyboard traversal, then navigate within the view.
   for attempt in range(12):
    s.command('key','Tab');d=settled(s)
    if focus_rows(d):break
   assert focus_rows(d),family
   capture(s,d,family,variant,'keyboard-return',True)
   # Selection is shared by identity when presentation changes.
   saved=d['selected']
   for index,mode in enumerate(('grid','list','column')):
    s.click(d['controls'][index]);d=settled(s);assert d['selected']==saved and d['mode']==mode
   s.click(d['controls'][('grid','list','column').index(family)]);d=settled(s)
   allrows=rows(d);s.click(allrows[0]['owner']);d=settled(s);allrows=rows(d)
   s.click(allrows[1]['owner'],'ctrl');d=settled(s);assert len(d['selected'])==2,(family,d['selected'])
   capture(s,d,family,variant,'multiple-selection',bool(focus_rows(d)))
   s.click(rows(d)[3]['owner'],'shift');d=settled(s);assert len(d['selected'])>=3
   capture(s,d,family,variant,'range-selection',bool(focus_rows(d)))
   # Activate a different native window, preserving selection.
   s.command('windowactivate','--sync',s.wid)
   target=subprocess.Popen(['xmessage','-name','MajorisFocusAway','-buttons','OK:0','Outside focus'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   try:
    time.sleep(.3);wid=s.command('search','--name','MajorisFocusAway').splitlines()[-1];s.command('windowactivate','--sync',wid);d=s.read(lambda r:not r['active'])
    capture(s,d,family,variant,'inactive-window',False)
   finally:target.terminate();target.wait(timeout=5)
   d=s.start('data-'+family+'-disabled',variant)
   assert all(c['flags']&8 for c in rows(d))
   capture(s,d,family,variant,'disabled',False)
  # A genuine keyboard-focused descendant propagates VISIBLE to its row.
  os.environ['MAJORIS_DATA_CHILD_CONTROL']='1'
  try:
   for family in ('list','column'):
    d=s.start('data-'+family+'-multi',variant);s.click(rows(d)[1]['owner']);s.command('key','Down');d=settled(s)
    s.command('key','Tab');d=settled(s)
    assert any(n['node']=='checkbutton' and n['focused'] for n in d['nodes']),d['nodes']
    assert any(c['flags']&WITHIN and c['flags']&VISIBLE and not c['flags']&FOCUSED for c in rows(d))
    capture(s,d,family,variant,'keyboard-descendant',True)
  finally:os.environ.pop('MAJORIS_DATA_CHILD_CONTROL',None)
(geometry/('focus-state-report'+('-2x' if scale==2 else '')+'.json')).write_text(json.dumps(evidence,indent=2)+'\n')
print('Real pointer/keyboard selection, row/descendant focus pixels, modifiers, view switching, return traversal and inactive selection passed')
