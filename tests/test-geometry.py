import json,os,subprocess,sys,tempfile
from pathlib import Path
from css_contract import html
def px(selector,property):return int(html(selector,property).removesuffix("px"))
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light')
tokens=json.loads((root/'design/tokens.json').read_text())
with tempfile.TemporaryDirectory(prefix='majoris-geometry-') as directory:
    config=Path(directory)/'gtk-4.0'; config.mkdir()
    for f in ('colors.css','colors-dark.css','gtk.css','gtk-dark.css'): (config/f).symlink_to(root/'theme/Majoris/gtk-4.0'/f)
    (config/'assets').symlink_to(root/'theme/Majoris/gtk-4.0/assets')
    data=Path(directory)/'data'; (data/'icons').mkdir(parents=True)
    (data/'icons/Majoris').symlink_to(root/'icons/Majoris')
    # Keep supplied user fonts visible when isolating the icon installation.
    fonts=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'fonts'
    if fonts.is_dir(): (data/'fonts').symlink_to(fonts)
    env={**os.environ,'XDG_CONFIG_HOME':directory,'XDG_DATA_HOME':str(data),'GTK_A11Y':'none','GSK_RENDERER':'cairo','GDK_BACKEND':'x11','MAJORIS_THEME_ROOT':str(root/'theme/Majoris')}
    result=subprocess.run([sys.argv[1],'--geometry-report','--'+variant],env=env,text=True,capture_output=True,check=True,timeout=20)
    report=json.loads(result.stdout)
    assert report['hidden_banner']['height']==0,report['hidden_banner']
    if os.environ.get('MAJORIS_REQUIRE_EXACT_FONT')=='1':
        assert report['resolved_pango_font'].startswith('Plus Jakarta Sans'),report['resolved_pango_font']
    for row_type in ('AdwActionRow','AdwSwitchRow','AdwComboRow','AdwEntryRow','AdwPasswordEntryRow','AdwSpinRow','AdwExpanderRow'):
        rows=[w for w in report['widget_tree'] if w['type']==row_type]
        assert rows,row_type
        assert all(w['height']>=50 for w in rows),(row_type,rows)
    assert 'Theme parser error' not in result.stderr and 'CRITICAL' not in result.stderr,result.stderr
    for scenario in ('simple_headerbar','dense_headerbar','split_sidebar_headerbar','split_content_headerbar'):
        h=report[scenario]
        assert h['painted_height']==tokens['window']['headerbar_height'],(scenario,h)
        assert h['content_height']==tokens['window']['window_control_size']
        assert h['divider']==1
        assert h['allocation_height']==h['content_height']+15+h['divider']
    for scenario in ('simple_window_controls','dense_window_controls'):
        controls=report[scenario]; assert set(controls)=={'minimize','maximize','close'}
        for name,b in controls.items():
            assert (b['width'],b['height'])==(tokens['window']['window_control_size'],)*2,(scenario,name,b)
            assert (b['glyph']['width'],b['glyph']['height'])==(tokens['window']['window_control_glyph'],)*2
    for name in ('normal_icon_button','flat_icon_button'):
        assert (report[name]['width'],report[name]['height'])==(px('.icon-btn','width'),px('.icon-btn','height')),(name,report[name])
    assert report['entry']['height']==px('.entry','height')
    assert report['dropdown']['height']==px('.select','height') and report['dropdown']['width']>=px('.select','min-width')
    for name in ('switch','switch_off'):assert (report[name]['width'],report[name]['height'])==(px('.switch','width'),px('.switch','height')),(name,report[name])
    assert report['view_switcher_button']['height']==px('.view-switch button','height'),report['view_switcher_button']
    assert report['tab']['label']['height']==px('.tab','height'),report['tab']
    assert any(w['type']=='GtkListBoxRow' and w['height']==px('.nav','height')+px('.nav','margin-bottom') for w in report['widget_tree']),'Sidebar 34px target plus 2px gap disappeared'
    (root/'artifacts').mkdir(exist_ok=True)
    (root/('artifacts/geometry-'+variant+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    if variant=='light': (root/'artifacts/geometry.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='widget_tree'},indent=2))
