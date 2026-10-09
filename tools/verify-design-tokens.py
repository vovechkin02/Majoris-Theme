import json
from design import ROOT, extract, icons
from token_contract import verify_generated

def differences(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [d for k in a.keys()|b.keys() for d in differences(a.get(k),b.get(k),path+'.'+k)]
    return [] if a==b else [f'{path}: HTML={a!r}, stored={b!r}']
errors=[]
for variant in ('light','dark'):
    errors+=differences(extract(variant),json.loads((ROOT/('design/tokens-dark.json' if variant=='dark' else 'design/tokens.json')).read_text()),variant)
for name, svg in icons().items():
    if (ROOT/'icons/Majoris/scalable/ui'/('window-'+name+'-symbolic.svg')).read_text().strip()!=svg:
        errors.append('SVG differs: '+name)
assert not errors, '\n'.join(errors)
verify_generated()
assert extract('dark')['semantic_color']['mixed_checkbox']=='#4F46E5'
assert extract('dark')['semantic_color']['focus']=='#818CF8'
print('Both HTML cascades, invariant primitive palette, independent action/focus/mixed states and exact glyphs match')
