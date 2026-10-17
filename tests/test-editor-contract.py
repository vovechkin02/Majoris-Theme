import json, xml.etree.ElementTree as ET
from css_contract import ROOT, rules, expect
for version in ('3','4'):
 for variant in ('light','dark'):
    css=rules(version,variant)
    assert 'selection' not in css, 'SourceView selection must remain scheme-owned'
    assert ':not(.sourceview) > text > selection' in css, 'Standalone GTK text retains UI selection colours'
    if version=='3':
        assert not any('majoris-document-tabs' in s or 'majoris-editor-toolbar' in s or 'majoris-statusbar' in s for s in css)
        continue
    expect(css,'tabbar.majoris-document-tabs','min-height','37px')
    expect(css,'.majoris-editor-toolbar','min-height','39px')
    expect(css,'.majoris-statusbar','min-height','33px')
    expect(css,'tabbar.majoris-document-tabs tab:selected','background-size','100% 2px')
    expect(css,'.majoris-editor-toolbar > button','min-height','26px')
    expect(css,'.majoris-statusbar > menubutton > button','min-height','26px')
    for s in css:
        if any(name in s for name in ('majoris-document-tabs','majoris-editor-toolbar','majoris-statusbar')):
            assert 'transform' not in css[s] or css[s]['transform']=='none'
    expect(css,'button','min-height','30px')
    expect(css,'windowcontrols > button','min-height','30px')
for variant in ('light','dark'):
 p=ROOT/f'theme/Majoris/gtksourceview-5/styles/majoris-{variant}.xml'
 xml=ET.parse(p).getroot()
 assert xml.attrib['id']=='majoris-'+variant
 styles={s.attrib['name']:s.attrib for s in xml.findall('style')}
 palette={c.attrib['name']:c.attrib['value'] for c in xml.findall('color')}
 def resolve(value): return palette.get(value,value)
 def luminance(color):
    components=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    return sum((c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4)*w for c,w in zip(components,(.2126,.7152,.0722)))
 def contrast(a,b):
    a,b=sorted((luminance(resolve(a)),luminance(resolve(b))))
    return (b+.05)/(a+.05)
 required=['text','selection','selection-unfocused','cursor','current-line','line-numbers','current-line-number','right-margin','bracket-match','search-match','draw-spaces','def:keyword','def:string','def:number','def:comment','def:type','def:function','def:identifier','def:constant','def:preprocessor','def:operator','def:property','def:attribute','def:special-char','def:doc-comment','def:heading','def:link-text','def:list-marker','def:preformatted-section','diff:added-line','diff:removed-line','def:error','def:warning']
 assert set(required)<=styles.keys()
 for name in required:
    style=styles[name]
    if 'foreground' not in style or name in ('draw-spaces','right-margin'):continue
    background=style.get('background', styles['text']['background'])
    assert contrast(style['foreground'], background)>=4.5,(variant,name,contrast(style['foreground'],background))
 assert resolve(styles['current-line']['background'])!=resolve(styles['text']['background'])
 assert resolve(styles['selection']['background'])!=resolve(styles['text']['background'])
print('Opt-in editor CSS, GTK3 isolation, stable primitives and source contrast contracts passed')
