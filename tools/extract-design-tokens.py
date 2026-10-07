import json
from design import ROOT, extract, icons
(ROOT/'design/tokens.json').write_text(json.dumps(extract(), indent=2)+'\n')
for name, svg in icons().items():
    p=ROOT/'icons/Majoris/scalable/ui'/('window-'+name+'-symbolic.svg')
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(svg+'\n')
