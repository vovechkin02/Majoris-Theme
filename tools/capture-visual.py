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
scale=os.environ.get('MAJORIS_CAPTURE_SCALE','1')
assert scale in ('1','2')
out=root/os.environ.get('MAJORIS_CAPTURE_DIRECTORY','artifacts/screenshots')/(variant+('-2x' if scale=='2' else ''));out.mkdir(parents=True,exist_ok=True)
pages=['sidebar','sidebar-basic','sidebar-states','sidebar-focus','sidebar-scroll','sidebar-narrow','sidebar-narrow-content','sidebar-large','sidebar-selected-pressed','sidebar-rtl','sidebar-backdrop','location','location-editing','location-narrow','editor','editor-source','editor-focus','editor-states','editor-overflow','layout','overview','scrolled','buttons','selection','inputs','ranges','preferences','navigation','data','menus','tooltip','feedback','dialog','status','simple','dense','split','states-buttons','states-controls','states-inputs','states-selection','states-navigation']
pages+=['layout-'+str(width) for width in (360,390,650,900,1200)]
pages+=['window-edge','window-edge-maximized','window-edge-fullscreen','window-edge-tiled','window-edge-tiled-left','window-edge-tiled-right','window-edge-tiled-top','window-edge-tiled-bottom']
if os.environ.get('MAJORIS_CAPTURE_PAGES'): pages=os.environ['MAJORIS_CAPTURE_PAGES'].split(',')
with tempfile.TemporaryDirectory(prefix='majoris-capture-') as temporary:
    config=Path(temporary)/'gtk-4.0';config.mkdir()
    data=Path(temporary)/'data'; (data/'icons').mkdir(parents=True)
    (data/'icons/Majoris').symlink_to(root/'icons/Majoris')
    fonts=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'fonts'
    if fonts.is_dir(): (data/'fonts').symlink_to(fonts)
    for file in ('gtk.css','gtk-dark.css','colors.css','colors-dark.css'): (config/file).symlink_to(root/'theme/Majoris/gtk-4.0'/file)
    (config/'assets').symlink_to(root/'theme/Majoris/gtk-4.0/assets')
    gtk3=Path(temporary)/'gtk-3.0';gtk3.mkdir()
    for file in ('gtk.css','gtk-dark.css','colors.css','colors-dark.css'): (gtk3/file).symlink_to(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if file=='gtk.css' and variant=='dark' else file))
    (gtk3/'assets').symlink_to(root/'theme/Majoris/gtk-3.0/assets')
    env={**os.environ,'XDG_CONFIG_HOME':temporary,'XDG_DATA_HOME':str(data),'GDK_BACKEND':'x11','ADW_DISABLE_PORTAL':'1','GTK_A11Y':'none','GSK_RENDERER':'cairo','MAJORIS_CAPTURE':'1','GDK_SCALE':scale,'GDK_DPI_SCALE':'1','MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'LD_PRELOAD':str(root/'build/libmajoris-gtk4-theme.so'),'ADW_DEBUG_COLOR_SCHEME':'prefer-dark' if variant=='dark' else 'prefer-light'}
    for page in pages:
        subprocess.run(['xdotool','mousemove','1410','1050'],check=True)
        with (out/f'{page}.log').open('w') as log:
            capture_env=dict(env)
            capture_page=page
            if page.startswith("sidebar"):capture_env["MAJORIS_SIDEBAR_REPORT"]=str(out/(page+"-geometry.json"))
            if page=='location-narrow':
                capture_env['MAJORIS_CONTENT_WIDTH']='480'
                capture_page='location'
            if page=='editor-overflow': capture_env['MAJORIS_CONTENT_WIDTH']='650'
            if page.startswith('layout-'):
                capture_env['MAJORIS_CONTENT_WIDTH']=page.split('-')[1]
                capture_page='layout'
            process=subprocess.Popen([sys.argv[1],'--page='+capture_page,'--'+variant],env=capture_env,stdout=log,stderr=log)
            try:
                time.sleep(2.0)
                assert process.poll() is None,f'{page} did not stay running; see log'
                if page=='sidebar-backdrop':
                    target=subprocess.check_output(['xdotool','search','--name','^Backdrop focus target$'],text=True).splitlines()[-1]
                    subprocess.run(['xdotool','windowactivate','--sync',target],check=True)
                    time.sleep(.2)
                    active=subprocess.check_output(['xdotool','getactivewindow'],text=True).strip()
                    assert int(active)==int(target), (active,target)
                    (out/'sidebar-backdrop-focus.json').write_text(json.dumps({'focus_target':target,'active_window':active,'method':'real Openbox activation; no held backdrop CSS flags'},indent=2)+'\n')
                if page.startswith('layout-'):
                    wid=subprocess.check_output(['xdotool','search','--name','^Majoris Widget Factory$'],text=True).splitlines()[0]
                    geometry=subprocess.check_output(['xdotool','getwindowgeometry','--shell',wid],text=True)
                    values=dict(line.split('=',1) for line in geometry.splitlines() if '=' in line)
                    assert int(values['WIDTH'])==int(capture_env['MAJORIS_CONTENT_WIDTH']), (page,values)
                    (out/(page+'-geometry.json')).write_text(json.dumps(values,indent=2)+'\n')
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
                if page.startswith('location'):
                    wid=subprocess.check_output(['xdotool','search','--name','^Majoris Files Components$'],text=True).splitlines()[0]
                    geometry=subprocess.check_output(['xdotool','getwindowgeometry','--shell',wid],text=True)
                    values=dict(line.split('=',1) for line in geometry.splitlines() if '=' in line)
                    subprocess.run(['xdotool','mousemove','--window',wid,str(int(values['WIDTH'])-100),str(int(values['HEIGHT'])-40),'click','--repeat','8','5'],check=True)
                    time.sleep(.4)
                    subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/(page+'-states.xwd'))],check=True)
                    subprocess.run(['magick',str(out/(page+'-states.xwd')),str(out/(page+'-states.png'))],check=True)
                if page=='layout':
                    # Preserve extra full-frame views of the scrollable card variants.
                    wid=subprocess.check_output(['xdotool','search','--name','^Majoris Widget Factory$'],text=True).splitlines()[0]
                    for stage in ('middle','bottom'):
                        for y in ('400','760'):
                            subprocess.run(['xdotool','mousemove','--window',wid,'700',y,'click','--repeat','4','--delay','80','5'],check=True)
                        time.sleep(.3)
                        name=page+'-'+stage
                        subprocess.run(['xwd','-silent','-screen','-root','-out',str(out/(name+'.xwd'))],check=True)
                        subprocess.run(['magick',str(out/(name+'.xwd')),str(out/(name+'.png'))],check=True)

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
    (out/'capture-metadata.json').write_text(json.dumps({'display':'Xvfb X11 with Openbox and xcompmgr' ,'viewport':[1440*int(scale),1080*int(scale)],'default_window_logical':[1280,960],'editor_window_logical':[900,650],'scale':int(scale),'renderer':'cairo','font_requested':'Plus Jakarta Sans','font_resolved':font,'theme':'Majoris','variant':variant,'pages':pages,'state_method':'real GTK state flags (not event simulation or app CSS)'},indent=2)+'\n')
