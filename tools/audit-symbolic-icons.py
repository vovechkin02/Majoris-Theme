"""Read-only audit of theme-owned and locally supplied Majoris SVG resources."""
import argparse,re,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('paths',nargs='*',type=Path);args=parser.parse_args()
roots=args.paths or [ROOT/'icons',ROOT/'theme']+[p for p in ROOT.parent.glob('Majoris-*') if p.is_dir() and p!=ROOT]
roots=[p.resolve() for p in roots]
rows=[];seen=set()
for root in roots:
 for p in ([root] if root.is_file() else sorted(root.rglob('*.svg'))):
  if any(part in ('.git','.reference','node_modules','artifacts','stage') or part.startswith('build') for part in p.relative_to(root).parts):continue
  if p.resolve() in seen:continue
  seen.add(p.resolve());text=p.read_text(errors='replace')
  try:ET.fromstring(text)
  except ET.ParseError:continue
  paints=[(a or b).strip() for a,b in re.findall(r'''(?:stroke|fill)\s*(?:=\s*["']([^"']+)["']|:\s*([^;}]+))''',text)]
  fixed=sorted(set(v for v in paints if v.lower() not in ('none','transparent','currentcolor','inherit','unset','context-fill','context-stroke') and not v.startswith(('url(','var('))))
  owner='THEME ICON' if ROOT in p.parents else 'APP ICON'
  symbolic='symbolic' in p.name
  classification='LIKELY SYMBOLIC BUG' if symbolic and fixed else ('INTENTIONALLY COLOURED' if fixed else owner)
  recommendation='Owning app: replace fixed symbolic stroke/fill with currentColor; validate light/dark recolouring.' if classification=='LIKELY SYMBOLIC BUG' else ('Retain intentional multicolour/spinner artwork.' if fixed else 'No fixed-colour issue.')
  rows.append((p,owner,classification,', '.join(fixed) or 'none',recommendation))
out=ROOT/'artifacts/symbolic-icon-audit.md';out.parent.mkdir(exist_ok=True)
lines=['# Symbolic icon audit','', 'Read-only scan. No application assets were rewritten. Name-based symbolic classification is a review finding, not an automatic mutation.','', '| File | Owner | Classification | Fixed paints | Recommendation |','|---|---|---|---|---|']
for row in rows:lines.append('| '+' | '.join(str(x).replace('|','\\|') for x in row)+' |')
lines+=['',f'Scanned {len(rows)} SVGs; {sum(row[2]=="LIKELY SYMBOLIC BUG" for row in rows)} likely symbolic bugs.','', 'Theme window-control glyphs inherit currentColor. Spinner assets deliberately retain two fixed colours. Application findings belong to their owning repositories.']
out.write_text('\n'.join(lines)+'\n');print(lines[-3])
