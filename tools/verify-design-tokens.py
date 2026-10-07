import json
from design import ROOT, extract, icons
def differences(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [d for k in a.keys()|b.keys() for d in differences(a.get(k),b.get(k),path+'.'+k)]
    return [] if a==b else [f'{path}: HTML={a!r}, stored={b!r}']
errors=differences(extract(),json.loads((ROOT/'design/tokens.json').read_text()))
for name, svg in icons().items():
    if (ROOT/'icons/Majoris/scalable/ui'/('window-'+name+'-symbolic.svg')).read_text().strip()!=svg:
        errors.append('SVG differs: '+name)
assert not errors, '\n'.join(errors)
print('All HTML tokens and four exact glyphs match')
