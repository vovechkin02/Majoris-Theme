"""Actual Openbox maximization/fullscreen, restore glyph allocation and edge frames."""
import json,os,re,subprocess,tempfile,time,sys
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1];out=root/'artifacts/window-edge-probes';out.mkdir(parents=True,exist_ok=True)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
compositor=None
try:
 time.sleep(.4);compositor=subprocess.Popen(['xcompmgr','-n'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.3)
 with tempfile.TemporaryDirectory() as tmp:
  config=Path(tmp)/'gtk-4.0';config.mkdir()
  for name in ['gtk.css','gtk-dark.css','colors.css','colors-dark.css','assets']:(config/name).symlink_to(root/'theme/Majoris/gtk-4.0'/name)
  data=Path(tmp)/'data/icons';data.mkdir(parents=True);(data/'Majoris').symlink_to(root/'icons/Majoris')
  fonts=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'fonts'
  if fonts.is_dir():(data.parent/'fonts').symlink_to(fonts)
  results=[]
  env={**os.environ,'XDG_CONFIG_HOME':tmp,'XDG_DATA_HOME':str(data.parent),'GSK_RENDERER':'cairo','GTK_A11Y':'none','MAJORIS_CAPTURE':'1','MAJORIS_THEME_ROOT':str(root/'theme/Majoris')}
  for variant in ['light','dark']:
   for state in ['floating','maximized','fullscreen','tiled','tiled-left','tiled-right','tiled-top','tiled-bottom']:
    page='window-edge'+('' if state=='floating' else '-'+state)
    logfile=out/f'{variant}-{state}.log'
    with logfile.open('w') as log:
     process=subprocess.Popen([sys.argv[1],'--page='+page,'--'+variant],env=env,stdout=log,stderr=log)
     try:
      time.sleep(1.6);assert process.poll() is None
      text=logfile.read_text();assert 'Theme parser error' not in text and 'CRITICAL' not in text,text
      assert 'header=48' in text,text
      classes=re.search(r'classes=(.*)',text)[1].split()
      assert 'csd' in classes and 'solid-csd' not in classes,classes
      if state!='floating':assert state in classes,classes
      if state=='maximized':assert 'maximized=true' in text,text
      if state=='fullscreen':assert 'fullscreen=true' in text,text
      glyphs=re.findall(r'control=(\S+) plate=(\d+)x(\d+) glyph=(\d+)x(\d+)',text)
      assert len(glyphs)==3,(state,text)
      assert all(g[1:]==('32','32','16','16') for g in glyphs),glyphs
      assert any(g[0]==('window-restore-symbolic' if state=='maximized' else 'window-maximize-symbolic') for g in glyphs),glyphs
      wid=subprocess.check_output(['xdotool','search','--name','^Majoris window edge /'],text=True).splitlines()[-1]
      xwd=out/f'{variant}-{state}.xwd';png=xwd.with_suffix('.png')
      subprocess.run(['xwd','-silent','-screen','-root','-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
      (out/f'{variant}-{state}-xwindow.txt').write_text(subprocess.check_output(['xwininfo','-id',wid],text=True))
      props=subprocess.check_output(['xprop','-id',wid,'_NET_WM_STATE'],text=True)
      if state=='maximized':assert '_NET_WM_STATE_MAXIMIZED_HORZ' in props and '_NET_WM_STATE_MAXIMIZED_VERT' in props,props
      if state=='fullscreen':assert '_NET_WM_STATE_FULLSCREEN' in props,props
      results.append({'variant':variant,'state':state,'actual_managed_state':state in ['maximized','fullscreen'],'tiled_diagnostic':state.startswith('tiled'),'header':48,'controls':[{'glyph':g[0],'plate':[32,32],'glyph_size':[16,16]} for g in glyphs],'wm_state':props.strip(),'screenshot':str(png)})
     finally:process.terminate();process.wait(timeout=5)
  (out/'geometry.json').write_text(json.dumps(results,indent=2)+'\n')
  subprocess.run([sys.executable,str(root/'tools/verify-rendered-window-edges.py')],check=True)
finally:
 if compositor:compositor.terminate();compositor.wait(timeout=5)
 wm.terminate();wm.wait(timeout=5)
print('Actual maximized/fullscreen states, diagnostic tiled classes, 48px header and minimize/maximize/restore/close 32px plates / 16px glyphs passed in both schemes')
