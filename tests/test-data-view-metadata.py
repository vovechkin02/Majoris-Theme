"""Realized native metadata: Pango ink/layout offsets through cell ancestry."""
import os,json,time,subprocess
from data_native import Session,ROOT
scale=int(os.environ.get('GDK_SCALE','1'));reports=[]
base=ROOT/'artifacts/data-view-focus';geometry=base/'geometry';geometry.mkdir(parents=True,exist_ok=True)
samples={'18 bytes','24 bytes','Folder','Plain text document','Modified','Favorites','Files','Format','ABCDEFGHIJKLMNOPQRSTUVWXYZ','gjpqy','10/27/2026 02:41:48 AM'}
fc=subprocess.check_output(['fc-match','-f','%{family} | %{style} | %{file}\n','Plus Jakarta Sans:style=Regular'],text=True).strip()
assert 'Plus Jakarta Sans' in fc,fc
with Session() as s:
 for variant in ('light','dark'):
  for compact in (False,True,'unhinted'):
   d=s.start('data-column-metadata'+('-unhinted' if compact=='unhinted' else '-compact' if compact else ''),variant);time.sleep(.3);d=s.read()
   metrics=[m for m in d['text_metrics'] if m['column']>0]
   assert samples<={m['text'] for m in metrics},samples-{m['text'] for m in metrics}
   for m in metrics:
    cell=next(c for c in d['cells'] if c['id']==m['id'] and c['column']==m['column'])
    assert not cell['ellipsized'],cell
    assert cell['size']==12 and cell['weight']==400,cell
    assert 'Plus Jakarta Sans' in m['resolved_font'] and m['scale']==scale,m
    assert cell['owner'][3]==(32 if compact is True else 40),cell
    ix,iy,iw,ih=m['ink'];ox,oy=m['layout_offset'];lx,ly,lw,lh=m['label']
    assert oy+iy>=0 and oy+iy+ih<=lh,m
    # Parent cells must contain all vertically positioned ink, not merely the layout origin.
    for ancestor in m['ancestors']:
     if ancestor['node'] in ('cell','row','box'):
      ax,ay,aw,ah=ancestor['bounds']
      assert ly+oy+iy>=ay and ly+oy+iy+ih<=ay+ah,m
    assert m['logical'][3]<=lh,m
   out=base/(variant+('-2x' if scale==2 else ''));out.mkdir(parents=True,exist_ok=True)
   png=out/('details-metadata'+('-unhinted' if compact=='unhinted' else '-compact' if compact else '')+'.png');xwd=png.with_suffix('.xwd')
   s.command('mousemove',0,0);subprocess.run(['xwd','-silent','-id',s.wid,'-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
   settings=subprocess.check_output(['xrdb','-query'],text=True)
   reports.append({'variant':variant,'scale':scale,'compact':compact,'fontconfig':fc,'xresources':settings,'font_rendering':d['font_rendering'],'metrics':metrics,'header':d['header_fonts'],'nodes':d['nodes']})
(geometry/('metadata-text-metrics'+('-2x' if scale==2 else '')+'.json')).write_text(json.dumps(reports,indent=2)+'\n')
print('All requested 12px/400 strings: native Pango ink fits labels/cells in both densities and themes; no vertical clipping reproduced')
