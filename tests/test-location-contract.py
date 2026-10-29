import json,re
from css_contract import rules, colors, resolve, expect, ROOT
for variant in ('light','dark'):
    css=rules('4',variant);palette=colors('4',variant)
    tokens=json.loads((ROOT/('design/tokens-dark.json' if variant=='dark' else 'design/tokens.json')).read_text())
    outer='.majoris-location-bar';crumb=outer+' button.majoris-location-crumb';entry=outer+' entry.majoris-location-entry'
    for selector in (outer,crumb,entry):expect(css,selector,'border-radius','4px')
    expect(css,outer,'padding','2px');expect(css,outer,'border','1px solid @border')
    expect(css,outer,'box-shadow',tokens['shadow']['control'])
    expect(css,crumb,'box-shadow','none');expect(css,entry+':focus-within','box-shadow','none')
    expect(css,crumb,'font-size','14px');expect(css,crumb,'font-weight','500')
    expect(css,outer+' button.majoris-location-current','font-weight','600')
    expect(css,entry,'font-size','14px');expect(css,entry,'font-weight','500')
    expect(css,crumb,'min-height','24px');expect(css,entry,'min-height','24px')
    expect(css,'button','min-height','30px');expect(css,'button','border-radius','4px')
    assert resolve(css[outer]['background'],palette)==('#28282C' if variant=='dark' else '#FFFFFF')
    focus=outer+'.majoris-location-editing:focus-within'
    assert resolve(css[focus]['border-color'],palette)==('#818CF8' if variant=='dark' else '#6366F1')
    normalize=lambda value:re.sub(r'\s+','',value)
    assert normalize(css[focus]['box-shadow'])==normalize(css['entry:focus-within']['box-shadow'])
    assert '128ms' in css[outer]['transition']
    for name in ('majoris-location-bar','majoris-location-crumb','majoris-location-current','majoris-location-separator','majoris-location-entry','majoris-location-editing','majoris-high-contrast'):
        assert any(name in selector for selector in css),name
    assert not any('majoris-location' in s for s in rules('3',variant))
source=(ROOT/'factory/src/location-bar.vala').read_text()
assert 'CssProvider' not in source and 'add_css_class("flat")' not in source
assert 'majoris-document-tabs' in source and 'new Majoris.Ui.Toolbar()' in source
assert 'append_widget(location)' in source and 'append_control(search)' in source
print('Location standard field palette, shadows, focus, 4px geometry, 14px typography, Toolbar ownership and GTK3 isolation passed')
