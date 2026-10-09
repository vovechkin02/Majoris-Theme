"""Halo-only titlebar controls, primitive identities and checkbox state mapping."""
from css_contract import *
from token_contract import verify_generated,verify_palette
verify_generated()
# Negative regression: semantic hover may remain correct while p700 is corrupt.
source=(ROOT/'theme/Majoris/gtk-4.0/colors-dark.css').read_text()
try:verify_palette(source.replace('@define-color primary_700 #4338CA;','@define-color primary_700 #7377F3;'),'dark')
except AssertionError:pass
else:raise AssertionError('Palette corruption was accepted')
for version in ('3','4'):
 for variant in ('light','dark'):
    css=rules(version,variant);palette=colors(version,variant)
    prefix='button.titlebutton' if version=='3' else 'windowcontrols > button'
    focus=':focus' if version=='3' else ':focus-visible'
    expect(css,prefix,'border','1px solid transparent')
    assert css[prefix].get('background',css[prefix].get('background-color'))=='transparent'
    expect(css,prefix,'box-shadow','none');expect(css,prefix,'border-radius','4px')
    for state,token in [(':hover','hover'),(':active','active')]:
        assert resolve(css[prefix+state]['background-color'],palette)==palette[token]
        expect(css,prefix+state,'box-shadow','none')
    expect(css,prefix+focus,'border-color','transparent')
    expect(css,prefix+focus,'box-shadow','0 0 0 2px '+('rgba(129,140,248,.36)' if variant=='dark' else 'rgba(99,102,241,.24)'))
    for state,value in [(':hover','#DC3C4D' if variant=='dark' else palette['danger']),(':active','#B92F3E' if variant=='dark' else palette['danger_pressed'])]:
        assert resolve(css[prefix+'.close'+state]['background-color'],palette)==value
    assert resolve(css['check:indeterminate']['color'],palette)=='#4F46E5'
    if variant=='dark':
        assert resolve(css['check']['background-color'],palette)=='#26262A'
        assert resolve(css['check']['border-color'],palette)=='#4A4A50'
        assert resolve(css['check:checked']['background-color'],palette)=='#6366F1'
        assert 'focus_color' in css['check:focus']['outline']
        for selector in ['button.suggested-action','banner button'] if version=='4' else ['button.suggested-action']:
            for state,token in [('', 'action_primary'),(':hover','action_primary_hover'),(':active','action_primary_pressed')]:
                expect(css,selector+state,'background-color','@'+token)
print('Independent palette/action states, checkbox contracts and halo-only window controls passed in all four configurations')
