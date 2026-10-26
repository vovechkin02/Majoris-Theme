"""Genuine X11 pointer/keyboard events against the native Vala adaptive fixture."""
import os,sys,json,time,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'artifacts/sidebar-finalisation/geometry';out.mkdir(parents=True,exist_ok=True)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def command(*args):return subprocess.check_output(['xdotool',*map(str,args)],text=True).strip()
try:
 time.sleep(.3)
 with tempfile.TemporaryDirectory(prefix='majoris-sidebar-input-') as temp:
  data=Path(temp)/'data';(data/'icons').mkdir(parents=True);(data/'icons/Majoris').symlink_to(root/'icons/Majoris')
  fonts=Path(os.environ.get('XDG_DATA_HOME',str(Path.home()/'.local/share')))/'fonts'
  if fonts.is_dir():(data/'fonts').symlink_to(fonts)
  report=Path(temp)/'geometry.json'
  env={**os.environ,'MAJORIS_SIDEBAR_REPORT':str(report),'MAJORIS_THEME_ROOT':str(root/'theme/Majoris'),'GTK_A11Y':'none','GIO_USE_VFS':'local','GSK_RENDERER':'cairo','MAJORIS_CAPTURE':'1','XDG_DATA_HOME':str(data)}
  evidence=[]
  def read(predicate=lambda item:True):
   deadline=time.monotonic()+6
   while time.monotonic()<deadline:
    try:
     item=json.loads(report.read_text())
     if predicate(item):return item
    except (OSError,json.JSONDecodeError):pass
    time.sleep(.05)
   raise AssertionError(('Native report did not reach expected state',report.read_text() if report.exists() else 'missing'))
  def click(bounds):
   x,y,w,h=bounds
   command('mousemove','--window',wid,round(x+min(w/2,60)),round(y+h/2));command('click','1')
  with (out/'interaction.log').open('w') as log:
   app=subprocess.Popen([str(root/'build/factory/majoris-theme-factory'),'--page=sidebar','--light'],env=env,stdout=log,stderr=log)
   try:
    initial=read(lambda r:r['sidebar_width']>=224 and not r['collapsed'] and len(r['headings'])==3 and all(h['bounds'][3]>0 for h in r['headings']));assert initial['sidebar_width']==224,initial
    assert [(h['first'],h['top_margin'],h['bottom_margin']) for h in initial['headings']]==[(True,0,8),(False,16,8),(False,16,8)]
    wid=command('search','--name','^Majoris Sidebar Design$').splitlines()[0];command('windowactivate','--sync',wid)
    click(initial['rows'][1]['bounds']);selected=read(lambda r:r['selected']=='Documents')
    assert selected['rows'][1]['weight']==600
    assert selected['rows'][1]['baseline']==initial['rows'][1]['baseline']
    evidence.append({'event':'pointer Documents','selected':selected['selected']})
    click(selected['rows'][5]['bounds']);time.sleep(.3);assert read()['selected']=='Documents'
    # Re-focus the selected row before sending actual native list navigation keys.
    click(read()['rows'][1]['bounds']);command('key','Down');keyboard=read(lambda r:r['selected']=='Downloads');command('key','Return')
    evidence.append({'event':'Down / Return','selected':keyboard['selected']})
    click(keyboard['group_title']);read(lambda r:not r['expanded']);assert read()['selected']=='Downloads'
    for _ in range(10):
     command('key','Tab');time.sleep(.24)
     if read()['group_focus']:break
    focused=read();assert focused['group_focus'],focused
    persistent=focused['selected']
    command('key','Return');read(lambda r:r['expanded']);assert read()['selected']==persistent
    evidence.append({'event':'pointer collapse / Tab traversal / Return expand','selection_preserved':True})
    command('windowsize','--sync',wid,390,650);narrow=read(lambda r:r['collapsed'])
    assert narrow['selected']==persistent
    click(narrow['reveal']);navigation=read(lambda r:not r['show_content'])
    click(navigation['rows'][1]['bounds']);content=read(lambda r:r['show_content'] and r['selected']=='Documents')
    assert content['collapsed']
    evidence.append({'event':'390px reveal / navigate','selected':content['selected']})
    command('windowsize','--sync',wid,900,650);desktop=read(lambda r:not r['collapsed']);assert desktop['selected']=='Documents',desktop
    evidence.append({'event':'resize desktop','selection_preserved':True,'sidebar_width':desktop['sidebar_width']})
   finally:app.terminate();app.wait(timeout=5)
   report.unlink(missing_ok=True)
   app=subprocess.Popen([str(root/'build/factory/majoris-theme-factory'),'--page=sidebar-scroll','--dark'],env=env,stdout=log,stderr=log)
   try:
    scrolled=read(lambda r:r['scroll']>0);wid=command('search','--name','^Majoris Sidebar Design$').splitlines()[-1]
    before=scrolled['scroll'];command('mousemove','--window',wid,110,180);command('click','--repeat',6,'--delay',60,'4')
    after=read(lambda r:r['scroll']<before)
    evidence.append({'event':'native wheel scrolling','before':before,'after':after['scroll']})
    command('mousemove','--window',wid,110,180);command('click','1');time.sleep(.24);command('key','Home')
    top=read(lambda r:r['selected']=='Home' and r['scroll']<=initial['rows'][0]['bounds'][1])
    assert top['rows'][0]['bounds'][1]>=48 and top['rows'][0]['bounds'][1]+32<=650
    evidence.append({'event':'native Home keyboard scrolling','selected':'Home','scroll':top['scroll'],'focused_row_visible':True})
   finally:app.terminate();app.wait(timeout=5)
   for mode in ('sidebar-first-hidden','sidebar-first-removed'):
    report.unlink(missing_ok=True)
    app=subprocess.Popen([str(root/'build/factory/majoris-theme-factory'),'--page='+mode,'--light'],env=env,stdout=log,stderr=log)
    try:
     changed=read(lambda r:len(r['headings'])==2 and r['headings'][0]['title']=='Locations' and all(h['bounds'][3]>0 for h in r['headings']))
     assert [(h['first'],h['top_margin'],h['bottom_margin']) for h in changed['headings']]==[(True,0,8),(False,16,8)],changed
     assert changed['headings'][0]['bounds'][1]-changed['surface'][1]==16,changed
     evidence.append({'event':mode,'headings':changed['headings']})
    finally:app.terminate();app.wait(timeout=5)
  assert 'CRITICAL' not in (out/'interaction.log').read_text()
  (out/'interaction.json').write_text(json.dumps(evidence,indent=2)+'\n')
finally:wm.terminate();wm.wait(timeout=5)
print('Actual pointer/keyboard selection, disabled row, disclosure, scrolling and adaptive reveal/selection persistence passed')
