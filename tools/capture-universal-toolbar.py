"""Capture native public-component instances using the existing Xvfb workflow."""
import os,subprocess,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parents[1]
pages='toolbars,toolbars-navigation,toolbars-commands,toolbars-editor,toolbars-mixed,toolbars-compact,toolbars-states,toolbars-narrow,toolbars-dynamic,toolbars-editing,toolbars-popover'
def capture(pair):
 variant,scale=pair
 env={**os.environ,'MAJORIS_VARIANT':variant,'MAJORIS_CAPTURE_SCALE':scale,'MAJORIS_CAPTURE_PAGES':pages,'MAJORIS_CAPTURE_DIRECTORY':'artifacts/universal-toolbar/factory'}
 subprocess.run(['dbus-run-session','--','xvfb-run','-a','-s','-screen 0 2880x2160x24','python3',str(root/'tools/capture-visual.py'),str(root/'build/factory/majoris-theme-factory') ],env=env,cwd=root,check=True)
 return variant,scale
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for pair in pool.map(capture,[(variant,scale) for variant in ('light','dark') for scale in ('1','2')]):print('Native universal toolbar captures:',*pair)
