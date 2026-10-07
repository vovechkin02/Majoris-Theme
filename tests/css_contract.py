"""Parsed CSS source contracts. This is NOT GTK computed-style introspection."""
import json,re,sys
from pathlib import Path
import tinycss2
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from design import html_value
TOKENS=json.loads((ROOT/'design/tokens.json').read_text())
def html(selector,property):return html_value(TOKENS,selector,property)
def rules(version):
    result={}
    css=(ROOT/f'theme/Majoris/gtk-{version}.0/gtk.css').read_text()
    for rule in tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True):
        if rule.type!='qualified-rule':continue
        declarations={d.name:tinycss2.serialize(d.value).strip() for d in tinycss2.parse_declaration_list(rule.content,skip_comments=True,skip_whitespace=True) if d.type=='declaration'}
        for selector in tinycss2.serialize(rule.prelude).strip().split(','): result.setdefault(selector.strip(),{}).update(declarations)
    return result
def expect(css,selector,property,value):
    actual=css.get(selector,{}).get(property)
    assert actual==value,(selector,property,actual,value)
