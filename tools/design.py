"""Extract the user-supplied design; shared by generation and verification."""
import re
import tinycss2
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'design/reference/majoris-widget-factory.html'
def style_rules(html):
    """Preserve every declaration, including non-root values and pseudo-elements."""
    result={}
    def visit(rules,scope=''):
        for rule in rules:
            if rule.type=='qualified-rule':
                head=tinycss2.serialize(rule.prelude).strip()
                declarations={d.name:tinycss2.serialize(d.value).strip() for d in tinycss2.parse_declaration_list(rule.content,skip_comments=True,skip_whitespace=True) if d.type=='declaration'}
                for selector in head.split(','):
                    result.setdefault(scope+selector.strip(),{}).update(declarations)
            elif rule.type=='at-rule' and rule.content is not None:
                visit(tinycss2.parse_rule_list(rule.content,skip_comments=True,skip_whitespace=True),scope+'@'+rule.at_keyword+' '+tinycss2.serialize(rule.prelude).strip()+' / ')
    for style in re.findall(r'<style>(.*?)</style>',html,re.S):
        visit(tinycss2.parse_stylesheet(style,skip_comments=True,skip_whitespace=True))
    return result
def extract():
    html = HTML.read_text(encoding='utf-8')
    variables = dict(re.findall(r'--([\w-]+)\s*:\s*([^;]+);', re.search(r':root\{(.*?)\}', html, re.S).group(1)))
    names = {'bg':'background','surface2':'surface_secondary','danger-press':'danger_pressed','border-soft':'border_soft','text2':'text_secondary','text3':'text_tertiary'}
    colors = {names.get(k, 'primary_'+k[1:] if re.fullmatch(r'p\d+', k) else k):v.upper() for k,v in variables.items() if v.startswith('#')}
    def dimension(selector, prop):
        block = re.search(r'(?m)^'+re.escape(selector)+r'\{(.*?)\}', html, re.S).group(1)
        return int(re.search(r'(?:^|;)\s*'+prop+r':(\d+)px', block).group(1))
    return {'color': colors, 'radius':{'control':int(variables['r-control'][:-2]),'structure':int(variables['r-struct'][:-2])},
            'motion':{k+'_ms':int(variables['motion-'+k].split('ms')[0]) for k in ('control','surface')},
            'motion_css':{k:variables['motion-'+k] for k in ('control','surface')},
            'shadow':{k[7:].replace('-','_'):v for k,v in variables.items() if k.startswith('shadow-')},
            'font': ['Plus Jakarta Sans','Noto Sans','Cantarell','sans-serif'],
            'window':{'headerbar_height':dimension('.headerbar','height'),'window_radius':dimension('.window','border-radius'), 'window_control_size':dimension('.window-control','width'),'window_control_glyph':dimension('.window-control svg','width')},
            'css_variables':variables,
            'css_rules':style_rules(html),
            'inline_styles':re.findall(r'\bstyle="([^"]*)"',html)}
def html_value(tokens,selector,property):
    value=tokens['css_rules'][selector][property]
    return re.sub(r'var\(--([\w-]+)\)',lambda m:tokens['css_variables'][m[1]],value)
def icons():
    html = HTML.read_text(encoding='utf-8')
    result = {}
    for label, svg in re.findall(r'<button[^>]*aria-label="([^"]+)"[^>]*>\s*(<svg.*?</svg>)', html, re.S):
        for kind, match in [('minimize','Minimise'),('maximize','Maximise'),('restore','Restore'),('close','Close')]:
            if label.startswith(match):
                result.setdefault(kind, svg.replace('viewbox=', 'viewBox='))
    assert len(result) == 4
    return result
