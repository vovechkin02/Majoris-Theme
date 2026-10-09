"""Independent primitive and component-state invariants for generated CSS."""
import re
from design import ROOT
PALETTE=dict(zip(['primary_'+str(n) for n in (50,100,200,300,400,500,600,700,800)],['#EEF2FF','#E0E7FF','#C7D2FE','#A5B4FC','#818CF8','#6366F1','#4F46E5','#4338CA','#3730A3']))
DARK_ACTIONS={'action_primary':'#6366F1','action_primary_hover':'#7377F3','action_primary_pressed':'#4F46E5','focus_color':'#818CF8','action_danger':'#DC3C4D','action_danger_hover':'#E34B5B','action_danger_pressed':'#B92F3E'}
def verify_palette(source,variant):
    definitions=re.findall(r'@define-color\s+(\w+)\s+([^;]+);',source)
    for name,value in PALETTE.items():
        actual=[v.upper() for k,v in definitions if k==name]
        assert actual==[value],(variant,name,actual,value,'primitive must be defined once')
    values=dict(definitions)
    if variant=='dark':
        for name,value in DARK_ACTIONS.items():assert values.get(name)==value,(name,values.get(name),value)

def verify_generated():
    for version in ('3','4'):
        for variant in ('light','dark'):
            directory=ROOT/f'theme/Majoris/gtk-{version}.0'
            verify_palette((directory/('colors-dark.css' if variant=='dark' else 'colors.css')).read_text(),variant)
            css=(directory/('gtk-dark.css' if variant=='dark' else 'gtk.css')).read_text()
            mixed=re.findall(r'check:indeterminate\s*\{([^}]+)\}',css)
            assert mixed and all(re.search(r'(?<![-\w])color:\s*@primary_600\s*;',block) for block in mixed),(version,variant,mixed)
