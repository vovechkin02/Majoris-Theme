"""Genuine pointer/keyboard input, native sort/resize and recycled factories."""
import json,time
from data_native import Session,ROOT
evidence=[]
def name_rows(data):return [c for c in data['cells'] if c['column']==0]
def compact_multi_ready(data):
 rows=name_rows(data)
 return data['multi'] and len(rows)>=4 and all(c['owner'][3]==32 for c in rows) and all(rows[i+1]['owner'][1]-rows[i]['owner'][1]==32 for i in range(3))
with Session() as s:
 d=s.start('data-column');selected=d['selected'];assert selected==[1]
 # Native sortable headers toggle order and preserve the selected object.
 for i in range(4):
  s.click(d['headers'][i]);time.sleep(.2);a=s.read();assert a['selected']==selected,a
  s.click(a['headers'][i]);time.sleep(.2);b=s.read();assert b['selected']==selected,b
  assert a['header_bounds'][3]==b['header_bounds'][3]==32
  assert a['indicators'][i]['bounds'][2:]==b['indicators'][i]['bounds'][2:],(a['indicators'],b['indicators'])
  iw,ih=a['indicators'][i]['bounds'][2:];assert iw==16 and 16<=ih<=23,(iw,ih)
  assert a['indicators'][i]['classes']!=b['indicators'][i]['classes']
  assert a['order']!=b['order'],(i,a['order'],b['order']);evidence.append({'sort':i,'ascending':a['order'],'descending':b['order'],'selected':selected});d=b
 # Drag the real first-column resize boundary; width must survive later frames.
 x,y,w,h=d['headers'][0];s.command('mousemove','--window',s.wid,round(x+w-2+s.inset[0]),round(y+h/2+s.inset[1]));s.command('mousedown',1);s.command('mousemove','--window',s.wid,round(x+w-70+s.inset[0]),round(y+h/2+s.inset[1]));s.command('mouseup',1)
 resized=s.read(lambda r:r['widths'][0]!=d['widths'][0]);time.sleep(.5);assert s.read()['widths'][0]==resized['widths'][0]
 evidence.append({'resize_before':d['widths'],'resize_after':resized['widths']})
 # Switch native view modes and density without losing model identity.
 for i,mode in enumerate(('grid','list','column')):
  s.click(resized['controls'][i]);d=s.read(lambda r:r['mode']==mode and len(r['cells'])>2);assert d['selected']==selected,d
 s.click(d['controls'][3]);d=s.read(lambda r:r['compact']);assert d['selected']==selected
 s.click(d['controls'][4]);d=s.read(compact_multi_ready);rows=name_rows(d)
 first_id=rows[0]['id'];s.click(rows[0]['owner']);d=s.read(lambda r:r['selected']==[first_id] and compact_multi_ready(r))
 rows=name_rows(d);second_id=rows[1]['id'];s.click(rows[1]['owner'],'ctrl');d=s.read(lambda r:set(r['selected'])=={first_id,second_id})
 rows=name_rows(d);s.click(rows[3]['owner'],'shift');d=s.read(lambda r:len(r['selected'])>=3)
 s.command('key','ctrl+a');d=s.read(lambda r:len(r['selected'])==r['count']);assert len(d['selected'])==64
 s.command('key','Home');s.command('key','Return');s.read(lambda r:r['activated']>0)
 evidence.append({'ctrl_shift_select_all':True,'activated':True})
 # A column without a sorter retains native non-sorting header behavior.
 disabled=s.start('data-column-disabled-sort');s.click(disabled['headers'][3]);time.sleep(.25);assert s.read()['order']==disabled['order']
 evidence.append({'disabled_sort_header_ignores_activation':True})
 # Asynchronous replacement preserves tile and filename allocations.
 d=s.start('data-grid');placeholder=next(c for c in d['cells'] if c['id']==3)
 ready=s.read(lambda r:any(c['id']==3 and c['thumbnail']=='landscape.svg' for c in r['cells']))
 loaded=next(c for c in ready['cells'] if c['id']==3)
 assert placeholder['bounds']==loaded['bounds'] and placeholder['label']==loaded['label'],(placeholder,loaded)
 evidence.append({'asynchronous_thumbnail_no_layout_shift':True})
 # A real 1,200-item model must recycle, not construct 1,200 tile widgets.
 d=s.start('data-grid-stress');assert d['count']>=1000 and d['setups']<d['count']/2,d
 initial=d['setups'];s.click(d['cells'][0]['owner']);s.command('key','ctrl+End');time.sleep(.4)
 d=s.read(lambda r:any(c['id']>1100 for c in r['cells']));assert d['setups']<d['count']/2,d
 assert d['unbinds']>0,d
 assert all(c['text']==c['name'] and c['tooltip']==c['name'] for c in d['cells']),d
 evidence.append({'stress_count':d['count'],'initial_setups':initial,'final_setups':d['setups'],'unbinds':d['unbinds']})
 # Native density/RTL/narrow/enlarged text each still render unclipped text.
 for mode in ('data-grid-narrow','data-grid-compact-rtl','data-list-compact-rtl','data-column-compact-rtl','data-grid-large','data-list-large','data-column-large'):
  d=s.start(mode);time.sleep(1);d=s.read()
  for c in d['cells']:
   assert c['ink'][1]+c['ink'][3]<=c['label'][3],(mode,c)
   if 'rtl' in mode and c['column']==0 and c['family']!='grid':assert c['icon'][0]-(c['label'][0]+c['label'][2])==8,(mode,c)
  if mode=='data-grid-large':
   assert all(c['bounds'][3]==c['owner'][3] and c['artwork'][1]-c['owner'][1]==8 for c in d['cells']),d
  if mode.endswith('-large'):
   assert max(c['bounds'][3] if c['family']=='grid' else c['owner'][3] for c in d['cells'])>(160 if 'grid' in mode else 40),mode
  evidence.append({'mode':mode,'cells':len(d['cells'])})
(ROOT/'artifacts/data-view-finalisation/geometry/interactions.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Native sorting, resizing, selection/modifier keys, mode/density switching, activation, stress recycling and accessibility layouts passed')
