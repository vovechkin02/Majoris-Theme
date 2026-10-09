"""Baseline and final geometry with an actual X11 WM (not solid-CSD fallback)."""
import os,subprocess,tempfile,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];records={}
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
compositor=None
try:
 time.sleep(.5);compositor=subprocess.Popen(['xcompmgr','-n'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.5)
 for stage in ['baseline','final']:
  theme=ROOT/('artifacts/baseline-final-fixes/theme/Majoris' if stage=='baseline' else 'theme/Majoris')
  for variant in ['light','dark']:
   with tempfile.TemporaryDirectory() as tmp:
    config=Path(tmp)/'gtk-4.0';config.mkdir()
    for name in ['gtk.css','gtk-dark.css','colors.css','colors-dark.css','assets']:(config/name).symlink_to(theme/'gtk-4.0'/name)
    env={**os.environ,'XDG_CONFIG_HOME':tmp,'GDK_BACKEND':'x11','ADW_DISABLE_PORTAL':'1','GTK_A11Y':'none','GSK_RENDERER':'cairo','MAJORIS_THEME_ROOT':str(theme)}
    p=subprocess.run([str(ROOT/'build/factory/majoris-theme-factory'),'--geometry-report','--'+variant],env=env,text=True,capture_output=True,check=True)
    assert 'Theme parser error' not in p.stderr and 'CRITICAL' not in p.stderr,p.stderr
    records[stage+'-'+variant]=json.loads(p.stdout)
    assert 'csd' in records[stage+'-'+variant]['widget_tree'][0]['classes'].split(),records[stage+'-'+variant]['widget_tree'][0]
    for name in ['simple_headerbar','dense_headerbar','split_sidebar_headerbar','split_content_headerbar']:assert records[stage+'-'+variant][name]['allocation_height']==48
    for name in ['simple_window_controls','dense_window_controls']:
     for value in records[stage+'-'+variant][name].values():assert (value['width'],value['height'],value['glyph']['width'],value['glyph']['height'])==(32,32,16,16)
 assert records['final-light']==records['final-dark']
 (ROOT/'artifacts/csd-baseline-final-geometry.json').write_text(json.dumps(records,indent=2)+'\n')
 print('WM-managed normal CSD: all four headers 48, plates32/glyphs16, complete light/dark geometry equal')
 for name in ['simple_headerbar','dense_headerbar','split_sidebar_headerbar','split_content_headerbar']:
  print(name,'baseline-width',records['baseline-light'][name]['width'],'final-width',records['final-light'][name]['width'])
finally:
 if compositor:compositor.terminate();compositor.wait(timeout=5)
 wm.terminate();wm.wait(timeout=5)
