from css_contract import rules, expect, html, ROOT

selectors = {
    '.majoris-card-body': {'padding': html('.card-body', 'padding')},
    '.majoris-card-footer': {'padding': '12px 16px', 'border-top': '1px solid @border_soft'},
    '.majoris-page-content': {'padding': html('.content', 'padding')},
    '.majoris-page-content.majoris-compact': {'padding': '16px'},
}
for version in ('3', '4'):
    light, dark = rules(version), rules(version, 'dark')
    for selector, declarations in selectors.items():
        for prop, value in declarations.items():
            expect(light, selector, prop, value)
            expect(dark, selector, prop, value)
        assert light[selector] == dark[selector]
        assert not ({'background', 'background-color', 'box-shadow', 'border-radius'} & light[selector].keys())
    for selector in ('box', '.card', '.card > *', '.card *', 'row', 'scrolledwindow', 'navigationpage', 'toolbarview'):
        assert not any(p.startswith('padding') for p in light.get(selector, {})), selector
code = (ROOT/'factory/src/factory-page.vala').read_text()
assert 'inner.add_css_class("majoris-card-body")' in code
assert 'inner.margin_' not in code
assert 'Adw.PreferencesGroup' in code and 'majoris-compact' in code
print('Shared layout boundaries, token insets and light/dark parity verified')
