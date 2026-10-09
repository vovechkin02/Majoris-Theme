"""Assert that the surgical pass leaves all unrelated light declarations intact."""
import json,sys
from pathlib import Path
import tinycss2
ROOT=Path(__file__).resolve().parents[1]
def rules(path):
 result={}
 for rule in tinycss2.parse_stylesheet(path.read_text(),skip_comments=True,skip_whitespace=True):
  if rule.type!='qualified-rule':continue
  ds={d.name:tinycss2.serialize(d.value).strip() for d in tinycss2.parse_declaration_list(rule.content,skip_comments=True,skip_whitespace=True) if d.type=='declaration'}
  for sel in tinycss2.serialize(rule.prelude).strip().split(','):result.setdefault(sel.strip(),{}).update(ds)
 return result
changes=[]
for version in ['3','4']:
 relative=Path(f'theme/Majoris/gtk-{version}.0/gtk.css')
 before=rules(ROOT/'artifacts/baseline-final-fixes'/relative);after=rules(ROOT/relative)
 for selector in before.keys()|after.keys():
  for prop in before.get(selector,{}).keys()|after.get(selector,{}).keys():
   a=before.get(selector,{}).get(prop);b=after.get(selector,{}).get(prop)
   if a==b:continue
   assert selector=='decoration' or selector.startswith('window.csd'),(version,selector,prop,a,b,'Unrelated light styling changed')
   changes.append({'version':version,'selector':selector,'property':prop,'before':a,'after':b})
(ROOT/'artifacts/surgical-light-scope.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Every changed light declaration is restricted to CSD/decoration edges and managed states')
