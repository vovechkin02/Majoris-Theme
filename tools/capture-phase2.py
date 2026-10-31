"""Capture the actual compiled Phase 2 gallery through the standard capture runner."""
import concurrent.futures,subprocess,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def capture(pair):
 variant,scale=pair
 env={**os.environ,'MAJORIS_VARIANT':variant,'MAJORIS_CAPTURE_SCALE':scale,'MAJORIS_CAPTURE_DIRECTORY':'artifacts/phase2-controls/factory','MAJORIS_CAPTURE_PAGES':'phase2-calendar,phase2-calendar-popover,phase2-links,phase2-editable-label,phase2-editing,phase2-paned,phase2-flowbox,phase2-expander,phase2-searchbar','GIO_USE_VFS':'local'}
 subprocess.run(['dbus-run-session','--','xvfb-run','-a','-s','-screen 0 2880x2160x24','python3',str(root/'tools/capture-visual.py'),str(root/'build/factory/majoris-theme-factory')],env=env,check=True,cwd=root)
 print('Native Phase2 captured',variant,scale)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(capture,[(v,s) for v in ['light','dark'] for s in ['1','2']]))
