"""Floating CSD edge and supported managed-state source contracts."""
from css_contract import *
for version in ('3','4'):
    for variant in ('light','dark'):
        css=rules(version,variant)
        normal='decoration' if version=='3' else 'window.csd'
        expect(css,normal,'border-radius','8px') if version=='3' else expect(css,'window.csd','border-radius','8px')
        expect(css,normal,'border',html('.window','border'))
        expect(css,normal,'border-color','rgba(255,255,255,.07)' if variant=='dark' else html('.window','border').split('solid ',1)[1])
        assert css[normal]['box-shadow']!='none'
        if version=='4':expect(css,normal,'outline','none')
        for state in ['maximized','fullscreen','tiled','tiled-left','tiled-right','tiled-top','tiled-bottom']:
            for selector in [f'window.csd.{state}']+([f'window.csd.{state} decoration'] if version=='3' else []):
                expect(css,selector,'border-radius','0');expect(css,selector,'border-width','0');expect(css,selector,'box-shadow','none')
print('GTK3/4 light/dark floating edge and all seven GTK managed-state contracts passed')
