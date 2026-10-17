"""Render unchanged supplemental showcase using temporary local-font copies."""
import hashlib, json, subprocess, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
source=root/'design/reference/editor-v1/Majoris-Theme-Complete-Widget-Showcase-v1.html'
out=root/'artifacts/screenshots/editor-html';out.mkdir(parents=True,exist_ok=True)
font=Path(subprocess.check_output(['fc-match','-f','%{file}','Plus Jakarta Sans'],text=True))
assert 'Plus Jakarta Sans' in subprocess.check_output(['fc-match','-f','%{family}','Plus Jakarta Sans'],text=True)
css='@font-face{font-family:"Plus Jakarta Sans";font-weight:200 800;src:url("'+font.as_uri()+'");}'
with tempfile.TemporaryDirectory(prefix='majoris-editor-html-') as temp:
 for variant in ('light','dark'):
  for section in ('document-tabs','editor','source'):
   section_css='.section:not(#'+section+'){display:none}.intro{display:none}'
   html=source.read_text().replace('</head>','<style>'+css+section_css+'</style></head>')
   script="<script>themeSet('"+variant+"');document.fonts.ready.then(()=>{document.documentElement.dataset.majorisSection='"+section+"';});</script>"
   file=Path(temp)/'reference.html';file.write_text(html.replace('</body>',script+'</body>'))
   command=['chromium','--headless','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files','--force-device-scale-factor=1','--window-size=1440,1080','--host-resolver-rules=MAP fonts.googleapis.com ~NOTFOUND, MAP fonts.gstatic.com ~NOTFOUND','--virtual-time-budget=3000','--dump-dom','--screenshot='+str(out/f'{variant}-{section}.png'),file.as_uri()]
   with (out/f'{variant}-{section}.log').open('w') as log:result=subprocess.run(command,stdout=subprocess.PIPE,stderr=log,text=True,check=True,timeout=30)
   assert 'data-majoris-section="'+section+'"' in result.stdout, 'Reference fonts did not finish loading'
   assert 'data-theme="'+variant+'"' in result.stdout, 'Reference appearance did not switch'
(out/'metadata.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'font_file':str(font),'font_sha256':hashlib.sha256(font.read_bytes()).hexdigest(),'viewport':[1440,1080],'method':'temporary local-font copy; unrelated sections and introduction hidden for section review; target CSS/markup unchanged; no screenshot manipulation'},indent=2)+'\n')
print('Supplemental document-tab, editor and source HTML references rendered in both modes')
