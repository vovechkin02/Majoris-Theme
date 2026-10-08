"""Optional application smoke captures; absence never gates theme unit tests."""
import os,subprocess,tempfile,time,shutil,json
from pathlib import Path
variant=os.environ.get('MAJORIS_VARIANT','light')
root=Path(__file__).resolve().parents[1];out=root/'artifacts/integration'/variant;out.mkdir(parents=True,exist_ok=True)
apps={'Files':shutil.which('nautilus'),'Settings':shutil.which('gnome-control-center')}
clock=root.parent/'Majoris-Clock/build/src/majoris-clock'
apps['Clock']=str(clock) if clock.is_file() else None
if os.environ.get('MAJORIS_INTEGRATION_APPS'):
 apps={k:v for k,v in apps.items() if k in os.environ['MAJORIS_INTEGRATION_APPS'].split(',')}
wm=subprocess.Popen(['openbox']);time.sleep(.5)
compositor=subprocess.Popen(['xcompmgr','-n']);time.sleep(.5)
results={}
try:
 with tempfile.TemporaryDirectory(prefix='majoris-apps-') as temporary:
  for version in ('3','4'):
   config=Path(temporary)/('gtk-'+version+'.0');config.mkdir()
   for file in ('gtk.css','gtk-dark.css','colors.css','colors-dark.css','assets'): (config/file).symlink_to(root/('theme/Majoris/gtk-'+version+'.0')/file)
   (config/'settings.ini').write_text('[Settings]\ngtk-icon-theme-name=Majoris\ngtk-font-name=Plus Jakarta Sans 10\n')
  env={**os.environ,'XDG_CONFIG_HOME':temporary,'GSETTINGS_BACKEND':'memory','GTK_THEME':'Majoris'+(':dark' if variant=='dark' else ''),'GTK_A11Y':'none','GSK_RENDERER':'cairo','GDK_BACKEND':'x11','XDG_SESSION_TYPE':'x11','XDG_CURRENT_DESKTOP':'GNOME','GDK_SCALE':'1','GDK_DPI_SCALE':'1','MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'ADW_DISABLE_PORTAL':'1','LD_PRELOAD':str(root/'build/libmajoris-gtk4-theme.so'),'ADW_DEBUG_COLOR_SCHEME':'prefer-dark' if variant=='dark' else 'prefer-light'}
  for name,binary in apps.items():
   if not binary:results[name]={'status':'unavailable','reason':'executable not installed in Debian'};continue
   appenv=env.copy()
   probe=root/'artifacts/probe-application.so'
   if probe.is_file():
    appenv['LD_PRELOAD']+=':'+str(probe)
    appenv['MAJORIS_APP_REPORT']=str(out/(name+'-geometry.txt'))
   if name=='Clock':appenv['GSETTINGS_SCHEMA_DIR']=str(clock.parents[1]/'data')
   with (out/(name+'.log')).open('w') as log:
    process=subprocess.Popen([binary,*([str(root)] if name=='Files' else [])],env=appenv,stdout=log,stderr=log)
    try:
     for attempt in range(40):
      if process.poll() is not None:break
      visible=subprocess.run(['xdotool','search','--onlyvisible','--pid',str(process.pid)],capture_output=True,text=True)
      if visible.returncode==0:break
      time.sleep(.5)
     time.sleep(4)
     if process.poll() is not None:results[name]={'status':'failed','exit':process.returncode};continue
     subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/(name+'.xwd'))],check=True)
     subprocess.run(['magick',str(out/(name+'.xwd')),str(out/(name+'.png'))],check=True)
     from PIL import Image,ImageStat
     if max(ImageStat.Stat(Image.open(out/(name+'.png')).convert('RGB')).stddev)<5:
      results[name]={'status':'failed','reason':'no visible application surface; blank capture rejected'};continue
     results[name]={'status':'captured','binary':binary}
     wid=visible.stdout.splitlines()[0]
     subprocess.run(['xdotool','windowactivate','--sync',wid],check=True)
     def capture_variant(suffix):
      time.sleep(1.5)
      stem=out/(name+'-'+suffix)
      subprocess.run(['xwd','-silent','-screen','-root','-out',str(stem)+'.xwd'],check=True)
      subprocess.run(['magick',str(stem)+'.xwd',str(stem)+'.png'],check=True)
     geometry=subprocess.check_output(['xdotool','getwindowgeometry','--shell',wid],text=True)
     dims=dict(line.split('=',1) for line in geometry.splitlines() if '=' in line)
     subprocess.run(['xdotool','mousemove','--window',wid,str(int(dims['WIDTH'])-24),'24'],check=True)
     capture_variant('close-hover')
     if name=='Files':
      # Native view button position verified in the complete initial capture.
      subprocess.run(['xdotool','mousemove','--window',wid,str(int(dims['WIDTH'])-172),'24','click','1'],check=True)
      time.sleep(.5)
      subprocess.run(['xdotool','mousemove','--window',wid,'400','100','click','1'],check=True)
      subprocess.run(['xdotool','key','ctrl+a'],check=True)
      subprocess.run(['xdotool','mousemove','--window',wid,'400','400'],check=True)
      capture_variant('list-selection')
      subprocess.run(['xdotool','mousemove','--window',wid,'600','400','click','--repeat','8','--delay','60','5'],check=True)
      capture_variant('scrolled')
     if name=='Clock':
      subprocess.run(['xdotool','mousemove','--window',wid,'100',str(int(dims['HEIGHT'])-24),'click','1'],check=True)
      capture_variant('preferences')
    finally:process.terminate();process.wait(timeout=5)
finally:
 compositor.terminate();wm.terminate()
(out/'availability.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
