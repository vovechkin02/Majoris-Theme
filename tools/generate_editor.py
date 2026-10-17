"""Supplemental GTK4 editor geometry and opt-in SourceView assets."""
import json, re
from design import ROOT

def editor_values(variant):
    tokens=json.loads((ROOT/'design/editor-tokens.json').read_text())
    return {**tokens['geometry'], **tokens[variant]}

def generate_schemes(output):
    for variant in ('light','dark'):
        tokens=json.loads((ROOT/('design/tokens-dark.json' if variant=='dark' else 'design/tokens.json')).read_text())
        values=tokens['color']
        source=(ROOT/f'design/sourceview/majoris-{variant}.xml.in').read_text()
        result=re.sub(r'\$\{(\w+)\}',lambda m:values[m[1]],source)
        directory=ROOT/'theme/Majoris/gtksourceview-5/styles'
        directory.mkdir(parents=True,exist_ok=True)
        output(directory/f'majoris-{variant}.xml',result)
