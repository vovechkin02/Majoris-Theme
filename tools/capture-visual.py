"""Full-display native captures: no crops, image changes or application CSS."""
import json,os,subprocess,sys,tempfile,time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
import atexit
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
atexit.register(wm.terminate);time.sleep(.5)
compositor=subprocess.Popen(['xcompmgr','-n'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
atexit.register(compositor.terminate);time.sleep(.5)
variant=os.environ.get('MAJORIS_VARIANT','light')
assert variant in ('light','dark')
out=root/'artifacts/screenshots'/variant;out.mkdir(parents=True,exist_ok=True)
pages=['overview','scrolled','buttons','selection','inputs','ranges','preferences','navigation','data','menus','tooltip','feedback','dialog','status','simple','dense','split','states-buttons','states-controls','states-inputs','states-selection','states-navigation']
if os.environ.get('MAJORIS_CAPTURE_PAGES'): pages=os.environ['MAJORIS_CAPTURE_PAGES'].split(',')
with tempfile.TemporaryDirectory(prefix='majoris-capture-') as temporary:
    config=Path(temporary)/'gtk-4.0';config.mkdir()
    for file in ('gtk.css','gtk-dark.css','colors.css','colors-dark.css'): (config/file).symlink_to(root/'theme/Majoris/gtk-4.0'/file)
    (config/'assets').symlink_to(root/'theme/Majoris/gtk-4.0/assets')
    gtk3=Path(temporary)/'gtk-3.0';gtk3.mkdir()
    for file in ('gtk.css','gtk-dark.css','colors.css','colors-dark.css'): (gtk3/file).symlink_to(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if file=='gtk.css' and variant=='dark' else file))
    (gtk3/'assets').symlink_to(root/'theme/Majoris/gtk-3.0/assets')
    env={**os.environ,'XDG_CONFIG_HOME':temporary,'GDK_BACKEND':'x11','ADW_DISABLE_PORTAL':'1','GTK_A11Y':'none','GSK_RENDERER':'cairo','MAJORIS_CAPTURE':'1','GDK_SCALE':'1','GDK_DPI_SCALE':'1','MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'LD_PRELOAD':str(root/'build/libmajoris-gtk4-theme.so'),'ADW_DEBUG_COLOR_SCHEME':'prefer-dark' if variant=='dark' else 'prefer-light'}
    for page in pages:
        subprocess.run(['xdotool','mousemove','1410','1050'],check=True)
        with (out/f'{page}.log').open('w') as log:
            process=subprocess.Popen([sys.argv[1],'--page='+page,'--'+variant],env=env,stdout=log,stderr=log)
            try:
                time.sleep(2.0)
                assert process.poll() is None,f'{page} did not stay running; see log'
                if page=='tooltip':
                    window_id=subprocess.check_output(['xdotool','search','--name','^Majoris Widget Factory$'],text=True).splitlines()[0]
                    subprocess.run(['xdotool','mousemove','--window',window_id,'23','23'],check=True);time.sleep(1.2)
                if page in ('menus','tooltip'):
                    import re
                    tree=subprocess.check_output(['xwininfo','-root','-tree'],text=True)
                    details='\n'.join(subprocess.check_output(['xwininfo','-id',wid],text=True) for wid in re.findall(r'^\s+(0x[0-9a-f]+) "majoris-theme-factory"',tree,re.M))
                    (out/(page+'-xwindows.txt')).write_text(tree+details)
                    wid=re.findall(r'^\s+(0x[0-9a-f]+) '+chr(34)+'majoris-theme-factory'+chr(34),tree,re.M)[0]
                    subprocess.run(['xwd','-silent','-id',wid,'-out',str(out/(page+'-popup.xwd'))],check=True)
                    subprocess.run(['magick',str(out/(page+'-popup.xwd')),str(out/(page+'-popup.png'))],check=True)
                subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/(page+'.xwd'))],check=True)
                subprocess.run(['magick',str(out/(page+'.xwd')),str(out/(page+'.png'))],check=True)
            finally:
                process.terminate()
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait()
        diagnostics=(out/f'{page}.log').read_text()
        assert 'Theme parser error' not in diagnostics,diagnostics
        print('Captured '+page,flush=True)
    for name,args in [('gtk3-native',[]),('gtk3-scrolled',['--scrolled'])]:
        with (out/(name+'.log')).open('w') as log:
            process=subprocess.Popen(['python3',str(root/'tools/gtk3-visual-fixture.py'),*args],env={**{k:v for k,v in env.items() if k!='LD_PRELOAD'},'GTK_THEME':'Majoris'+(':dark' if variant=='dark' else '')},stdout=log,stderr=log)
            try:
                time.sleep(2)
                assert process.poll() is None,'GTK3 fixture failed'
                subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/(name+'.xwd'))],check=True)
                subprocess.run(['magick',str(out/(name+'.xwd')),str(out/(name+'.png'))],check=True)
            finally:process.terminate();process.wait(timeout=5)
        assert 'Theme parsing error' not in (out/(name+'.log')).read_text()
    with (out/'gtk4-demo.log').open('w') as log:
        process=subprocess.Popen(['gtk4-demo'],env=env,stdout=log,stderr=log)
        try:
            time.sleep(2)
            assert process.poll() is None,'Stock gtk4-demo failed to launch'
            subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/'gtk4-demo.xwd')],check=True)
            subprocess.run(['magick',str(out/'gtk4-demo.xwd'),str(out/'gtk4-demo.png')],check=True)
        finally:process.terminate();process.wait(timeout=5)
    assert 'Theme parser error' not in (out/'gtk4-demo.log').read_text()
    font=subprocess.check_output(['fc-match','-f','%{family}','Plus Jakarta Sans'],text=True)
    if os.environ.get('MAJORIS_REQUIRE_EXACT_FONT')=='1':
        assert font.split(',')[0]=='Plus Jakarta Sans',font
        for generic in ('sans-serif','system-ui'):
            assert subprocess.check_output(['fc-match','-f','%{family}',generic],text=True).split(',')[0]=='Plus Jakarta Sans'
    (out/'capture-metadata.json').write_text(json.dumps({'display':'Xvfb X11 with Openbox and xcompmgr' ,'viewport':[1440,1080],'window':[1280,960],'scale':1,'renderer':'cairo','font_requested':'Plus Jakarta Sans','font_resolved':font,'theme':'Majoris','variant':variant,'pages':pages,'state_method':'real GTK state flags (not event simulation or app CSS)'},indent=2)+'\n')
