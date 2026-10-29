"""Native public component: geometry, dynamic groups, real focus and disabled pixels."""
import os,time,json,tempfile,subprocess
from pathlib import Path
from PIL import Image
import gi
gi.require_version('Gtk','4.0')
from gi.repository import Gtk
root=Path(__file__).resolve().parents[1];scale=int(os.environ.get('GDK_SCALE','1'));out=root/'artifacts/toolbar-polish';records=[]
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def cmd(*args):return subprocess.check_output(['xdotool',*map(str,args)],text=True).strip()
def gap(a,b):return b[0]-a[0]-a[2]
try:
 time.sleep(.3)
 for variant in ('light','dark'):
  with tempfile.TemporaryDirectory(prefix='toolbar-polish-') as temporary:
   report=Path(temporary)/'report.json';folder=out/(variant+('-2x' if scale==2 else ''));folder.mkdir(parents=True,exist_ok=True)
   with (folder/'public-component.log').open('w') as stream:
    app=subprocess.Popen([str(root/'build/toolbar-polish-probe'),str(report)],env={**os.environ,'MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'MAJORIS_VARIANT':variant,'GIO_USE_VFS':'local'},stdout=stream,stderr=stream)
    def read(predicate=lambda d:True):
     end=time.monotonic()+6
     while time.monotonic()<end:
      try:
       d=json.loads(report.read_text())
       if d['standard'][3]>=40 and d['raised'][3]>0 and predicate(d):return d
      except (OSError,ValueError):pass
      assert app.poll() is None,(folder/'public-component.log').read_text();time.sleep(.05)
     raise AssertionError(report.read_text())
    try:
     d=read();initial=d;mutations=[];focus_states={};wid=cmd('search','--name','^Majoris Toolbar Polish$').splitlines()[-1];cmd('windowactivate','--sync',wid)
     def point(rect):x,y,w,h=rect;return round((x+min(w/2,50)-d['window'][0])*scale),round((y+h/2-d['window'][1])*scale)
     def click(rect):x,y=point(rect);cmd('mousemove','--window',wid,x,y);cmd('click',1);time.sleep(.2)
     def capture(name):
      path=folder/('public-'+name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);return Image.open(path.with_suffix('.png')).convert('RGB')
     assert gap(*d['legacy_controls'])==4,d
     assert d['standard'][3]==d['compact'][3]==40,d
     assert d['compact'][1]-d['standard'][1]==40,d
     assert d['raised'][0]-d['standard'][0]==8,d
     assert d['standard'][0]+d['standard'][2]-d['edge'][0]-d['edge'][2]==8,d
     assert d['raised'][1]-d['standard'][1]==4 and d['raised'][3]==32,d
     assert d['entry'][1]-d['compact'][1]==6 and d['entry'][3]==28,d
     assert gap(d['raised'],d['flat'])==gap(d['first'],d['second'])==4,d
     assert gap(d['disabled'],d['group'])==gap(d['group'],d['next_group'])==8,d
     assert [f['weight'] for f in d['fonts']]==[600,500,600,600,500],d['fonts']
     for f in d['fonts']+d['text_metrics']:
      assert f['size']==14 and f['ink'][1]+f['layout_offset'][1]>=0 and f['ink'][1]+f['ink'][3]+f['layout_offset'][1]<=f['label'][3] and 'Plus Jakarta Sans' in f['resolved'],f
     baseline=d['segments'];flat_baseline=d['compact_first'];capture('stacked-toolbars');capture('standard-toolbar')
     # Single disabled opacity, measured from actual glyph pixels rather than CSS strings.
     image=capture('disabled-controls');x,y,w,h=d['fonts'][2]['label'];ox,oy=-d['window'][0],-d['window'][1]
     crop=image.crop((round((x+ox)*scale),round((y+oy)*scale),round((x+w+ox)*scale),round((y+h+oy)*scale)))
     extreme=min(p[0] for p in crop.getdata()) if variant=='light' else max(p[0] for p in crop.getdata())
     base,fore=(255,28) if variant=='light' else (32,244);alpha=(extreme-base)/(fore-base);assert .54<=alpha<=.62,(variant,alpha,extreme,d['fonts'][2])
     # One logical divider pixel belongs to the first 40px row, with no extra band.
     divider=(229,229,233) if variant=='light' else (49,49,54);surface=(255,255,255) if variant=='light' else (32,32,35)
     px=round((d['standard'][0]+d['standard'][2]/2+ox)*scale)
     for row,color in ((38,surface),(39,divider),(40,surface)):
      assert image.getpixel((px,round((d['standard'][1]+row+oy)*scale)))==color,(variant,row)
     disabled_alphas=[alpha]
     for sample in d['disabled_samples']:
      rect=sample['font']['label'] if sample['font'] else sample['bounds']
      x,y,w,h=rect
      pixels=image.crop((round((x+ox)*scale),round((y+oy)*scale),round((x+w+ox)*scale),round((y+h+oy)*scale)))
      extreme=min(p[0] for p in pixels.getdata()) if variant=='light' else max(p[0] for p in pixels.getdata())
      sample_base=max(p[0] for p in pixels.getdata()) if variant=='light' else min(p[0] for p in pixels.getdata())
      value=(extreme-sample_base)/(fore-sample_base);assert .54<=value<=.62,(variant,value,sample);disabled_alphas.append(value)
     def focus_pixels(image,rect,expected):
      x,y,w,h=rect;px=round((x+w/2+ox)*scale);py=round((y+oy)*scale)
      target=(99,102,241) if variant=='light' else (129,140,248)
      rows=sum(max(abs(a-b) for a,b in zip(image.getpixel((px,py+dy)),target))<=3 for dy in range(4*scale))
      assert rows==(2*scale if expected else 0),(variant,scale,rect,rows)
     # Pointer focus and keyboard focus must differ for raised, flat and segments.
     focus=Gtk.StateFlags.FOCUS_VISIBLE
     for name,index in (('raised',0),('flat',1)):
      click(d[name]);pointer=read(lambda r:(r['flags'][index]&int(Gtk.StateFlags.FOCUSED))!=0)
      assert not pointer['flags'][index]&int(focus),pointer
      focus_pixels(capture('focus-mouse-'+name),d[name],False);focus_states[name+'-pointer']=pointer['flags']
      cmd('key','Tab' if name=='raised' else 'shift+Tab');keyboard=read(lambda r:any(flag&int(focus) for flag in r['flags']))
      focus_pixels(capture('focus-keyboard-'+name),keyboard['flat' if name=='raised' else 'raised'],True);focus_states[name+'-keyboard']=keyboard['flags']
     click(d['segments'][0]);d=read();assert not any(f&int(focus) for f in d['flags'][2:]),d
     cmd('key','Right');cmd('key','space');time.sleep(.2)
     keyboard=read(lambda r:any(f&int(focus) for f in r['flags'][2:]));selected=next(i for i,f in enumerate(keyboard['flags'][2:]) if f&int(focus))
     focus_pixels(capture('segmented-control'),keyboard['segments'][selected],True);focus_states['segment-keyboard']=keyboard['flags']
     # Explicit dynamic insert/remove/reorder, empty groups and redundant separators.
     for stage in range(1,24):
      cmd('key','F6');d=read(lambda r:r['stage']==stage);time.sleep(.15);d=read();mutations.append(d)
      if stage==1:assert d['group_visible']
      if stage==2:assert gap(d['first'],d['second'])==4,d
      if stage==3:assert d['next_group'][0]-d['standard'][0]==8,d
      if stage==4:assert not d['group_visible'],d
      if stage==5:assert d['group_visible'] and gap(d['first'],d['second'])==4,d
      if stage==6:assert d['separators']==[True,False],d
      if stage==7:assert gap(d['next_group'],d['raised'])==16,d
      if stage==8:
       assert d['standard'][3]==40 and d['raised'][3]==28 and d['raised'][1]-d['standard'][1]==6,d;capture('compact-toolbar')
      if stage==9:assert d['segments']==baseline,d
      if stage==10:assert not d['group_visible'],d
      if stage==11:assert d['group_visible'],d
      if stage==12:assert d['next_group']==[0,0,0,0],d
      if stage==13:assert gap(d['disabled'],d['next_group'])==gap(d['next_group'],d['group'])==8,d
      if stage==14:assert d['compact_first']==flat_baseline and d['text_metrics'][5]['weight']==600,d
      if stage==15:assert d['standard'][3]==40 and d['compact'][1]-d['standard'][1]==40,d
      if stage==16:
       assert d['standard'][0]+d['standard'][2]-d['raised'][0]-d['raised'][2]==8 and gap(d['second'],d['first'])==4,d
       capture('rtl-toolbar')
      if stage==17:
       enlarged_segments=d['segments'];assert d['standard'][3]>40,d
       for f in d['fonts'][3:]:assert f['size']==24 and f['ink'][1]+f['ink'][3]+f['layout_offset'][1]<=f['label'][3],f
       capture('enlarged-segments')
      if stage==18:assert d['segments']==enlarged_segments,d
      if stage==19:assert d['standard'][3]==40 and [r[2:] for r in d['segments']]==[r[2:] for r in baseline],d
      if stage==20:renamed_segments=d['segments']
      if stage==21:assert d['segments']==renamed_segments,d
      if stage==22:dynamic_bounds=d['dynamic_segment'];with_dynamic=d['segments'];assert dynamic_bounds[2]>0,d
      if stage==23:assert d['dynamic_segment']==dynamic_bounds and d['segments']==with_dynamic,d
     records.append({'variant':variant,'scale':scale,'disabled_alphas':disabled_alphas,'initial':initial,'focus':focus_states,'mutations':mutations,'final':d})
    finally:app.terminate();app.wait(timeout=5)
   log=(folder/'public-component.log').read_text();assert 'CRITICAL' not in log and 'Theme parser error' not in log,log
finally:wm.terminate();wm.wait(timeout=5)
geo=out/'geometry';geo.mkdir(exist_ok=True,parents=True);(geo/f'public-{scale}x.json').write_text(json.dumps(records,indent=2)+'\n')
print('Public toolbar insets, stack80, gaps4/8/16, dynamic groups, stable weights, pointer/keyboard focus and disabled pixel opacity passed')
