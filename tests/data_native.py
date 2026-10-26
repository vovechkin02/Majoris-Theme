"""Shared native X11 harness; no application appearance CSS."""
import os,json,time,tempfile,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Session:
 def __enter__(self):
  self.wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);self.temp=tempfile.TemporaryDirectory(prefix='majoris-data-');self.report=Path(self.temp.name)/'report.json';self.app=None;time.sleep(.25);return self
 def start(self,mode,variant='light'):
  self.stop();self.report.unlink(missing_ok=True)
  self.log=(ROOT/'artifacts/data-view-finalisation/geometry'/f'{mode}-{variant}-{os.environ.get("GDK_SCALE","1")}-{os.getpid()}.log');self.log.parent.mkdir(parents=True,exist_ok=True);self.stream=self.log.open('w')
  self.app=subprocess.Popen([str(ROOT/'build/factory/majoris-theme-factory'),'--page='+mode,'--'+variant],cwd=ROOT,env={**os.environ,'MAJORIS_DATA_REPORT':str(self.report),'MAJORIS_THEME_ROOT':str(ROOT/'theme/Majoris'),'GTK_A11Y':'none','GIO_USE_VFS':'local','MAJORIS_CAPTURE':'1','GSK_RENDERER':'cairo','ADW_DISABLE_PORTAL':'1'},stdout=self.stream,stderr=self.stream)
  data=self.read(lambda d:len(d['cells'])>=3 and all(c['owner'][3]>0 and c['label'][3]>0 for c in d['cells']))
  self.inset=[-data['window_bounds'][0],-data['window_bounds'][1]]
  self.wid=self.command('search','--name','^Majoris Data Views$').splitlines()[-1];self.command('windowactivate','--sync',self.wid);return data
 def read(self,predicate=lambda d:True):
  end=time.monotonic()+8
  while time.monotonic()<end:
   try:
    d=json.loads(self.report.read_text())
    if predicate(d):return d
   except (OSError,ValueError):pass
   if self.app.poll() is not None:raise AssertionError(self.log.read_text())
   time.sleep(.05)
  raise AssertionError(('native condition not reached',self.report.read_text() if self.report.exists() else self.log.read_text()))
 def command(self,*args):return subprocess.check_output(['xdotool',*map(str,args)],text=True).strip()
 def click(self,bounds,key=None):
  scale=int(os.environ.get('GDK_SCALE','1'));x,y,w,h=bounds
  if key:self.command('keydown',key)
  self.command('mousemove','--window',self.wid,round((x+min(w/2,60)+self.inset[0])*scale),round((y+h/2+self.inset[1])*scale));self.command('click','1')
  if key:self.command('keyup',key)
 def stop(self):
  if self.app is not None:
   self.app.terminate();self.app.wait(timeout=5);self.stream.close();assert 'Theme parser error' not in self.log.read_text();assert 'CRITICAL' not in self.log.read_text(),self.log.read_text();self.app=None
 def __exit__(self,*exc):self.stop();self.temp.cleanup();self.wm.terminate();self.wm.wait(timeout=5)
