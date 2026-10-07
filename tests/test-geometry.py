import json,os,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
expected=json.loads((root/'tests/expected/headerbars.json').read_text())
with tempfile.TemporaryDirectory(prefix='majoris-geometry-') as directory:
    config=Path(directory)/'gtk-4.0'; config.mkdir()
    for f in ('colors.css','gtk.css','gtk-dark.css'): (config/f).symlink_to(root/'theme/Majoris/gtk-4.0'/f)
    data=Path(directory)/'data'; (data/'icons').mkdir(parents=True)
    (data/'icons/Majoris').symlink_to(root/'icons/Majoris')
    env={**os.environ,'XDG_CONFIG_HOME':directory,'XDG_DATA_HOME':str(data),'GTK_A11Y':'none','GSK_RENDERER':'cairo'}
    result=subprocess.run([sys.argv[1],'--geometry-report'],env=env,text=True,capture_output=True,check=True,timeout=20)
    report=json.loads(result.stdout)
    assert 'Theme parser error' not in result.stderr,result.stderr
    print(json.dumps(report,indent=2),flush=True)
    for scenario in ('simple','dense'):
        h=report['headerbar_'+scenario]['height']; assert h==expected['headerbar_height'],(scenario,h)
        buttons=[w for w in report['windowcontrols_'+scenario] if w['type']=='GtkButton']
        assert len(buttons)==3,(scenario,buttons)
        for b in buttons: assert (b['width'],b['height'])==(32,32),(scenario,b)
        images=[w for w in report['windowcontrols_'+scenario] if w['type']=='GtkImage']
        assert len(images)==3
        for image in images: assert (image['width'],image['height'])==(16,16),(scenario,image)
    assert report['headerbar_simple']['height']==report['headerbar_dense']['height']
    (root/'artifacts').mkdir(exist_ok=True)
    (root/'artifacts/geometry.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
