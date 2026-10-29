"""Actual factory + Majoris.Ui.Toolbar: native allocations, GSK paints and Pango."""
import json,os,time,tempfile,subprocess,sys,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];scale=int(os.environ.get('GDK_SCALE','1'))
base=ROOT/'artifacts/location-bar-standardisation';geo=base/'geometry';geo.mkdir(parents=True,exist_ok=True)
measurements=[];comparisons=[];texts=[]
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
time.sleep(.3)
def command(*args):return subprocess.check_output(['xdotool',*map(str,args)],text=True).strip()
def shadows(nodes):return [{k:v for k,v in n.items() if k not in ('bounds',)} for n in nodes if 'SHADOW_NODE' in n['type']]
def outer_border(nodes):return next(n for n in nodes if n['type']=='GSK_BORDER_NODE' and n['bounds'][3]>=32)
def labels(d):return [n for n in d['nodes'] if n.get('layout_source')=='GtkLabel layout' and n['text']!='Search files']
class Fixture:
 def __init__(self,variant,mode='location',width=None,theme=None):
  self.variant=variant;self.out=base/(variant+('-2x' if scale==2 else ''));self.out.mkdir(parents=True,exist_ok=True)
  self.temp=tempfile.TemporaryDirectory();self.report=Path(self.temp.name)/'report.json'
  self.log=(self.out/(mode+'.log')).open('w')
  env={**os.environ,'MAJORIS_LOCATION_REPORT':str(self.report),'MAJORIS_THEME_ROOT':str(theme or ROOT/'theme/Majoris'),'GTK_A11Y':'none','GIO_USE_VFS':'local','MAJORIS_CAPTURE':'1','GSK_RENDERER':'cairo','GDK_BACKEND':'x11'}
  if width:env['MAJORIS_CONTENT_WIDTH']=str(width)
  self.process=subprocess.Popen([str(ROOT/'build/factory/majoris-theme-factory'),'--page='+mode,'--'+variant],cwd=ROOT,env=env,stdout=self.log,stderr=self.log)
  self.read();self.wid=command('search','--sync','--name','^Majoris Files Components$').splitlines()[-1];command('windowactivate','--sync',self.wid);time.sleep(.25)
 def read(self,condition=lambda d:True):
  deadline=time.monotonic()+8
  while time.monotonic()<deadline:
   try:
    d=json.loads(self.report.read_text())
    if d['location'][3]>0 and d['render_location'] and condition(d):return d
   except (OSError,ValueError):pass
   assert self.process.poll() is None,'Fixture exited'
   time.sleep(.05)
  raise AssertionError('Native report condition timed out: '+self.report.read_text())
 def settle(self):time.sleep(.25);return self.read()
 def click(self,bounds):
  x,y,w,h=bounds;command('mousemove','--window',self.wid,round((x+w/2)*scale),round((y+h/2)*scale));command('click',1);return self.settle()
 def capture(self,name):
  path=self.out/(name+'.png');xwd=path.with_suffix('.xwd')
  subprocess.run(['xwd','-silent','-id',self.wid,'-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(path)],check=True);return path
 def close(self):
  self.process.terminate();self.process.wait(timeout=5);self.log.close();self.temp.cleanup()
 def __enter__(self):return self
 def __exit__(self,*exc):self.close()
def geometry(d,normal=True):
 if normal:
  assert d['location'][3]==d['search'][3]==32,d
  assert d['toolbar'][3]==40 and d['location'][1]==d['search'][1]==d['toolbar'][1]+4
  assert d['location'][1]+32==d['toolbar'][1]+36
 outer=next(n for n in d['nodes'] if 'majoris-location-bar' in n['classes'])
 assert outer['border']==[1]*4 and outer['padding']==[2]*4,outer
 for key in ('render_location','render_search'):
  border=outer_border(d[key]);assert border['radius']==[4]*4 and border['widths']==[1]*4,border
 assert outer_border(d['render_location'])['color']==outer_border(d['render_search'])['color']
 assert shadows(d['render_location'])==shadows(d['render_search']),(d['render_location'],d['render_search'])
 for n in labels(d):
  assert 'Plus Jakarta Sans' in n['font'] and n['size']==14,n
  assert n['weight'] in (500,600),n
  ox,oy=n['layout_offset'];ix,iy,iw,ih=n['ink'];x,y,w,h=n['bounds']
  assert oy+iy>=0 and oy+iy+ih<=h,n
  # Both separator and breadcrumb label boxes are vertically centered in the 26px interior.
  if normal:assert abs((y+h/2)-(d['location'][1]+16))<=.5,n
  texts.append({'variant':variant,'scale':scale,'node':n,'location':d['location']})
 measurements.append({'variant':variant,'scale':scale,'report':d})
if '--comparison' in sys.argv:
 try:
  old=base/'comparison/before-theme';shutil.copytree(ROOT/'theme/Majoris/gtk-4.0',old/'gtk-4.0',dirs_exist_ok=True)
  for name in ('gtk.css','gtk-dark.css'):
   (old/'gtk-4.0'/name).write_bytes(subprocess.check_output(['git','show','HEAD:theme/Majoris/gtk-4.0/'+name],cwd=ROOT))
  for state,theme in (('before',old),('after',None)):
   os.environ['MAJORIS_LOCATION_SNAPSHOT']=str(base/'comparison'/(state+'.png'))
   with Fixture('light',theme=theme) as f:
    time.sleep(.4);f.capture('comparison-'+state)
 finally:
  wm.terminate();wm.wait(timeout=5)
 sys.exit(0)
try:
 for variant in ('light','dark'):
  with Fixture(variant) as f:
   d=f.settle();geometry(d);f.capture('location-default');f.capture('location-vs-search');f.capture('location-in-toolbar')
   comparisons.append({'variant':variant,'scale':scale,'state':'default','location':d['render_location'],'search':d['render_search']})
   crumb=next(n for n in d['nodes'] if n['node']=='button' and 'majoris-location-crumb' in n['classes'])
   x,y,w,h=crumb['bounds'];command('mousemove','--window',f.wid,round((x+w/2)*scale),round((y+h/2)*scale));d=f.settle();f.capture('breadcrumb-hover')
   assert any(n.get('radius')==[4]*4 and n['bounds'][3]==26 for n in d['render_location']),d['render_location']
   command('mousedown',1);time.sleep(.15);pressed=f.read();f.capture('breadcrumb-pressed');assert pressed['location']==d['location'];command('mouseup',1);d=f.settle()
   # Keyboard focus stays on a crumb and does not request field editing.
   for i in range(18):
    command('key','Tab');d=f.settle()
    if any(n['node']=='button' and 'majoris-location-crumb' in n['classes'] and n['flags']&8192 for n in d['nodes']):break
   assert not d['editing'] and any(n['node']=='button' and n['flags']&8192 for n in d['nodes'])
   f.capture('breadcrumb-keyboard-focus')
   command('key','ctrl+l');d=f.read(lambda r:r['editing']);time.sleep(.25);d=f.read();f.capture('location-editing');f.capture('location-editing-focus')
   assert d['location'][3]==32 and d['entry'][3]==26,d
   assert not shadows(d['render_entry']),d['render_entry']
   focused=shadows(d['render_location']);assert len(focused)>=2,focused
   focus_border=outer_border(d['render_location']);assert focus_border['color']==('rgb(99,102,241)' if variant=='light' else 'rgb(129,140,248)')
   f.click(d['search']);command('type','--clearmodifiers','Search files');d=f.settle()
   assert focused==shadows(d['render_search']),(focused,shadows(d['render_search']))
   comparisons.append({'variant':variant,'scale':scale,'state':'editing-focus','location_shadows':focused,'search':d['render_search']})
   # Real native path editing exercises requested glyphs at both selected/current and normal weights.
   for value in ('Home','Desktop','Documents','Downloads','Favorites','Files','Format','ABCDEFGHIJKLMNOPQRSTUVWXYZ','gjpqy','A Very Long Folder Name With Multiple Words'):
    for target in ('/'+value,'/'+value+'/gjpqy'):
     command('key','ctrl+l');f.read(lambda r:r['editing']);command('type','--clearmodifiers',target);command('key','Return');d=f.read(lambda r:not r['editing'] and r['path']==target);time.sleep(.2);d=f.read()
     sample=next(n for n in labels(d) if n['text']==value)
     assert sample['weight']==(600 if target=='/'+value else 500),sample
     for n in labels(d):
      ox,oy=n['layout_offset'];ink_top=oy+n['ink'][1];ink_bottom=ink_top+n['ink'][3]
      assert ink_top>=0 and ink_bottom<=n['bounds'][3],n
      assert n['bounds'][1]+ink_top>=d['location'][1]+3 and n['bounds'][1]+ink_bottom<=d['location'][1]+29,n
      texts.append({'variant':variant,'scale':scale,'node':n,'location':d['location']})
   command('key','ctrl+l');f.read(lambda r:r['editing']);command('type','--clearmodifiers','/home/demo/Documents/Projects/A Very Long Folder Name With Multiple Words/Archive');command('key','Return');d=f.read(lambda r:not r['editing']);f.capture('location-long-path')
  with Fixture(variant,width=480) as f:
   d=f.settle();geometry(d);assert d['location'][2]>48 and d['search'][2]>=160;f.capture('location-narrow')
  with Fixture(variant,'location-rtl') as f:
   d=f.settle();geometry(d);assert any(n.get('text')=='‹' for n in d['nodes']);f.capture('location-rtl')
  with Fixture(variant,'location-large') as f:
   d=f.read(lambda r:r['location'][3]>32);assert d['toolbar'][3]>40 and d['search'][3]>32,d
   for n in labels(d):
    oy=n['layout_offset'][1];assert oy+n['ink'][1]>=0 and oy+n['ink'][1]+n['ink'][3]<=n['bounds'][3],n
   f.capture('location-accessibility');measurements.append({'variant':variant,'scale':scale,'accessibility':d})
 (geo/('location-bar'+('-2x' if scale==2 else '')+'.json')).write_text(json.dumps(measurements,indent=2)+'\n')
 (geo/('search-comparison'+('-2x' if scale==2 else '')+'.json')).write_text(json.dumps(comparisons,indent=2)+'\n')
 (geo/('text-metrics'+('-2x' if scale==2 else '')+'.json')).write_text(json.dumps(texts,indent=2)+'\n')
finally:wm.terminate();wm.wait(timeout=5)
print('Actual 32px fields in 40px Toolbar, GSK 4px borders/shadows/focus, 14px typography, Pango ink, input, RTL/narrow/accessibility passed')

