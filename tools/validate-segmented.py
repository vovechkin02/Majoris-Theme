"""Capture the native segmented matrix in an isolated Linux X11 session."""
import os,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for variant in ('light','dark'):
 for scale,dpi in (('1','1'),('2','1'),('1','1.25')):
  env={**os.environ,'MAJORIS_VARIANT':variant,'GDK_SCALE':scale,'GDK_DPI_SCALE':dpi,'GDK_BACKEND':'x11','ADW_DISABLE_PORTAL':'1','GTK_A11Y':'none'}
  subprocess.run(['dbus-run-session','--','xvfb-run','-a','-s','-screen 0 2880x2160x24','python3','tests/test-segmented-native.py'],cwd=root,env=env,check=True)

import json,shutil
out=root/'artifacts/segmented-control-standardisation'
(out/'comparison').mkdir(exist_ok=True);(out/'geometry').mkdir(exist_ok=True)
for name in ('before','after'):shutil.copyfile(out/'light'/(name+'.png'),out/'comparison'/(name+'.png'))
for name in ('segmented-dimensions','focus-states','radius-validation'):
 report={path.parent.name:json.loads(path.read_text()) for path in out.glob('*/'+name+'.json') if path.parent.name!='geometry'}
 (out/'geometry'/(name+'.json')).write_text(json.dumps(report,indent=2))
