from css_contract import rules, colors, resolve, expect, ROOT
for variant in ('light','dark'):
    css=rules('4',variant);palette=colors('4',variant)
    expect(css,'.majoris-location-bar','border-radius','9px')
    expect(css,'.majoris-location-bar','box-shadow','none')
    expect(css,'.majoris-location-bar button.majoris-location-crumb','border-radius','7px')
    expect(css,'.majoris-location-bar button.majoris-location-current','font-weight','700')
    expect(css,'button','min-height','30px')
    expect(css,'button','border-radius','4px')
    assert resolve(css['.majoris-location-bar']['background'],palette)==('#28282C' if variant=='dark' else '#F2F2F4')
    focus=css['.majoris-location-bar.majoris-location-editing']['border-color']
    assert resolve(focus,palette)==('#818CF8' if variant=='dark' else '#6366F1')
    for name in ('majoris-location-bar','majoris-location-crumb','majoris-location-current','majoris-location-separator','majoris-location-entry','majoris-location-editing','majoris-high-contrast'):
        assert any(name in selector for selector in css),name
    assert not any('majoris-location' in s for s in rules('3',variant))
source=(ROOT/'factory/src/location-bar.vala').read_text()
assert 'CssProvider' not in source and 'add_css_class("flat")' not in source
assert 'majoris-document-tabs' in source
print('Location semantic palette, geometry, focus, GTK3 isolation and native ownership passed')
