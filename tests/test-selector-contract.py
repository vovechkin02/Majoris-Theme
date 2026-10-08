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
for version in ('3','4'):
    css=rules(version)
    expect(css,'.title-1','font-size',html('.page-title','font-size'))
    expect(css,'.title-1','letter-spacing',html('.page-title','letter-spacing'))
expect(rules('4'),'.majoris-card-description','line-height',html('.card-head p','line-height'))
expect(rules('4'),'dialog.alert .body','line-height',html('.dialog-body p','line-height'))
expect(rules('4'),'banner','padding','0')
expect(rules('4'),'banner','border','none')
expect(rules('4'),'banner > revealer > widget','background-color','@primary_50')
expect(rules('4'),'banner > revealer > widget','border','1px solid @primary_200')
expect(rules('4'),'banner > revealer > widget','padding',html('.banner','padding'))
expect(rules('4'),'headerbar entry button','min-height','20px')
expect(rules('4'),'headerbar entry button','border','none')
expect(rules('4'),'headerbar entry button','box-shadow','none')
