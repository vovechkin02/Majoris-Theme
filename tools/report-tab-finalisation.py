"""Compare measured native tab geometry between palettes after the tab matrix."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
base=root/'artifacts/tab-finalisation'
summary=[]
for suffix in ('','-2x','-text-125'):
 light=json.loads((base/('light'+suffix)/'gtk4-measurements.json').read_text())
 dark=json.loads((base/('dark'+suffix)/'gtk4-measurements.json').read_text())
 def signature(rows):return {(row['text'],row['selected'],row['font'],tuple(row['allocation']),tuple(row['logical']),tuple(row['ink']),round(row['baseline'],4),row['tab_height']) for row in rows}
 assert signature(light)==signature(dark),(suffix,'document geometry differs by palette')
 summary.append({'case':suffix or '1x','document_geometry_equal':True,'labels_measured_light':len(light),'labels_measured_dark':len(dark)})
for toolkit in ('3','4'):
 for suffix in ('','-2x'):
  a=json.loads((base/('light'+suffix)/('gtk'+toolkit+'-navigation.json')).read_text())
  b=json.loads((base/('dark'+suffix)/('gtk'+toolkit+'-navigation.json')).read_text())
  assert a==b,(toolkit,suffix,'notebook geometry differs by palette')
(base/'geometry-comparison.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Native document and notebook geometry matches between palettes at all tested scales')
