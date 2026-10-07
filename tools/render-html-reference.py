"""Capture the unchanged reference without CSS, DOM edits, or cropping."""
import hashlib,json,subprocess
from PIL import Image,ImageStat
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=root/'design/reference/majoris-widget-factory.html'
out=root/'artifacts/screenshots/html';out.mkdir(parents=True,exist_ok=True)
# Scrolled Chromium frames were blank on this runtime: never use them as evidence.
for name,height in [('overview',1080),('full-reference',4000)]:
    command=['chromium','--headless','--disable-gpu','--disable-dev-shm-usage','--force-device-scale-factor=1',f'--window-size=1440,{height}','--host-resolver-rules=MAP fonts.googleapis.com ~NOTFOUND, MAP fonts.gstatic.com ~NOTFOUND','--virtual-time-budget=8000','--screenshot='+str(out/(name+'.png')),source.as_uri()]
    with (out/(name+'.log')).open('w') as log:subprocess.run(command,stdout=log,stderr=log,check=True,timeout=40)
    assert max(ImageStat.Stat(Image.open(out/(name+'.png')).convert('RGB')).stddev)>5,'Blank HTML render: '+name
    print('Rendered HTML '+name,flush=True)
(out/'render-metadata.json').write_text(json.dumps({'source':str(source.relative_to(root)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'viewports':{'overview':[1440,1080],'full-reference':[1440,4000]},'scale':1,'transformation':'none: unchanged HTML, full uncropped captures','font':'Remote font hosts disabled for deterministic installed-font fallback. Supply Plus Jakarta Sans for exact typography acceptance.','comparison':'Full reference shows every section. Native captures retain the complete display. Compare components structurally, not by pixel equality.'},indent=2)+'\n')
