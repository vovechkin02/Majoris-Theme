"""Validate a single visible native edge and absence of managed edge insets.

Reads untouched full-display XWD-derived PNGs and their X11 window geometry.
Compositor shadow/transparent corner acceptance remains a GNOME VM check.
"""
import json,re
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'artifacts/window-edge-probes'
results=[]
for variant in ['light','dark']:
 for state in ['floating','maximized','fullscreen','tiled','tiled-left','tiled-right','tiled-top','tiled-bottom']:
  text=(out/f'{variant}-{state}-xwindow.txt').read_text()
  def number(label):return int(re.search(re.escape(label)+r':\s*(-?\d+)',text)[1])
  x=number('Absolute upper-left X');y=number('Absolute upper-left Y');w=number('Width');h=number('Height')
  im=Image.open(out/f'{variant}-{state}.png').convert('RGB')
  background=(24,24,27) if variant=='dark' else (247,247,248)
  edge=im.getpixel((x,y+h//2));inside=im.getpixel((x+1,y+h//2))
  assert inside==background,(variant,state,inside,background)
  if state=='floating':
   paint=(255,255,255) if variant=='dark' else (20,20,25);alpha=.07 if variant=='dark' else .12
   expected=tuple(round(paint[i]*alpha+background[i]*(1-alpha)) for i in range(3))
   assert all(abs(edge[i]-expected[i])<=2 for i in range(3)),(variant,edge,expected)
   assert edge!=inside,'Visible single edge is missing'
  else:assert edge==inside,(variant,state,'managed inset/edge remains',edge,inside)
  if state in ['maximized','fullscreen']:
   assert (x,y,w,h)==(0,0,1440,1080),(state,x,y,w,h)
   assert im.getpixel((0,1079))==background and im.getpixel((1439,1079))==background,(state,'bottom rounded seam')
   assert im.getpixel((0,0))==im.getpixel((1,0)),(state,'top rounded seam')
  results.append({'variant':variant,'state':state,'single_edge_width':1 if state=='floating' else 0,'edge_pixel':edge,'adjacent_content_pixel':inside,'actual_window':[x,y,w,h]})
(ROOT/'artifacts/window-edge-pixel-validation.json').write_text(json.dumps(results,indent=2)+'\n')
print('Single 1px light/dark edges match reference alpha paints; seven managed states have no edge inset; actual maximized/fullscreen frames have square seamless corners')
