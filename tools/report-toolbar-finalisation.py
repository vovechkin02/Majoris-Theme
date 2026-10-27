"""Compare the realized toolbar matrix and collect its geometry reports."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1];base=root/'artifacts/toolbar-finalisation'
reports=[];focus=[];text=[]
for version in ('3','4'):
 for suffix in ('','-2x'):
  a=json.loads((base/('light'+suffix)/('gtk'+version+'-measurements.json')).read_text())
  b=json.loads((base/('dark'+suffix)/('gtk'+version+'-measurements.json')).read_text())
  assert a==b,(version,suffix,'palette geometry mismatch')
  for variant in ('light','dark'):
   path=base/(variant+suffix)
   reports.append(dict(toolkit=version,variant=variant,scale=2 if suffix else 1,**a))
   focus.append(dict(toolkit=version,variant=variant,scale=2 if suffix else 1,states=json.loads((path/('gtk'+version+'-focus-states.json')).read_text())))
   text.append(dict(toolkit=version,variant=variant,scale=2 if suffix else 1,labels=json.loads((path/('gtk'+version+'-text-metrics.json')).read_text())))
geometry=base/'geometry';geometry.mkdir(exist_ok=True)
for name,records in [('toolbar-measurements',reports),('toolbar-focus-states',focus),('toolbar-text-metrics',text)]:
 (geometry/(name+'.json')).write_text(json.dumps(records,indent=2)+'\n')
print('Toolbar geometry matches between palettes in all toolkit/scale pairs')
