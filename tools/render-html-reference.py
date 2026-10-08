"""Render a temporary reference copy with the same local fonts as GTK."""
import hashlib,json,subprocess,tempfile,os
from PIL import Image,ImageStat
from pathlib import Path
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light')
assert variant in ('light','dark')
source=root/('design/reference/majoris-widget-factory'+('-dark' if variant=='dark' else '')+'.html')
out=root/('artifacts/screenshots/html'+('-dark' if variant=='dark' else ''));out.mkdir(parents=True,exist_ok=True)
fonts=[]
for pattern,style in [('Plus Jakarta Sans','normal'),('Plus Jakarta Sans:slant=italic','italic')]:
    family=subprocess.check_output(['fc-match','-f','%{family}',pattern],text=True)
    assert family.split(',')[0]=='Plus Jakarta Sans',family
    path=Path(subprocess.check_output(['fc-match','-f','%{file}',pattern],text=True))
    fonts.append({'file':str(path),'style':style,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
css=''.join('@font-face{font-family:"Plus Jakarta Sans";font-style:'+f['style']+';font-weight:200 800;font-display:block;src:url("'+Path(f['file']).as_uri()+'") format("truetype");}' for f in fonts)
with tempfile.TemporaryDirectory(prefix='majoris-reference-') as temporary:
    rendered=Path(temporary)/'reference.html'
    readiness='<script>Promise.all([document.fonts.load(\'13px "Plus Jakarta Sans"\'),document.fonts.load(\'italic 13px "Plus Jakarta Sans"\')]).then(f=>{document.documentElement.dataset.majorisFontLoaded=String(f.every(a=>a.length>0));});</script>'
    rendered.write_text(source.read_text().replace('</head>','<style>'+css+'</style></head>').replace('</body>',readiness+'</body>'))
    for name,height in [('overview',1080),('full-reference',4000)]:
        command=['chromium','--headless','--disable-gpu','--disable-dev-shm-usage','--allow-file-access-from-files','--force-device-scale-factor=1',f'--window-size=1440,{height}','--host-resolver-rules=MAP fonts.googleapis.com ~NOTFOUND, MAP fonts.gstatic.com ~NOTFOUND','--virtual-time-budget=8000','--screenshot='+str(out/(name+'.png')),rendered.as_uri()]
        command.insert(1,'--dump-dom')
        with (out/(name+'.log')).open('w') as log:
            result=subprocess.run(command,stdout=subprocess.PIPE,stderr=log,text=True,check=True,timeout=40)
        assert 'data-majoris-font-loaded="true"' in result.stdout,'Browser did not load supplied local fonts'
        assert max(ImageStat.Stat(Image.open(out/(name+'.png')).convert('RGB')).stddev)>5,'Blank HTML render: '+name
        print('Rendered HTML '+name,flush=True)
(out/'render-metadata.json').write_text(json.dumps({'source':str(source.relative_to(root)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'viewports':{'overview':[1440,1080],'full-reference':[1440,4000]},'scale':1,'transformation':'temporary copy: local @font-face only; authoritative HTML untouched; no crops','fonts':fonts,'font':'Exact locally installed Plus Jakarta Sans; remote hosts disabled','comparison':'Compare native structure rather than pixel equality.'},indent=2)+'\n')
