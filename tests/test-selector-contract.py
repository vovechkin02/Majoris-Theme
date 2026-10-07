from css_contract import *
css=rules('4')
for state,bg in [('hover','@hover'),('active','@active')]:
    selector='windowcontrols > button:'+state
    for prop,value in [('background-color',bg),('border-color','transparent'),('background-image','none'),('box-shadow','none'),('outline','none'),('border-radius',html('.window-control','border-radius'))]:expect(css,selector,prop,value)
expect(css,'windowcontrols > button:focus-visible','outline','none')
expect(css,'windowcontrols > button:focus-visible','border-color',html('.window-control.is-focus','border-color'))
for v in ('3','4'):
    css=rules(v)
    expect(css,'notebook > header tab:checked','border','none')
    if v=='4':assert '10px' in css['notebook > header tab:checked']['background-image'] and 'calc(100% - 10px)' in css['notebook > header tab:checked']['background-image']
    else:expect(css,'notebook > header tab:checked label','margin','0 -2px')
    assert 'primary_500' in css['.navigation-sidebar row:selected']['background-image']
    expect(css,'.navigation-sidebar row:selected','background-size','2px 100%')
    for selector in ['button','entry']:
        assert '128ms' in css[selector]['transition'] and 'transform' not in css[selector]['transition']
print('Explicit cascade reset, inset tab/sidebar indicator and stationary motion contracts passed; runtime images supplement source checks')
