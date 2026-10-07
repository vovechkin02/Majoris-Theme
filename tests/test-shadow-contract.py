from css_contract import *
for v in ('3','4'):
    css=rules(v)
    expect(css,'.card','box-shadow',TOKENS['shadow']['card'])
    expect(css,'.boxed-list','box-shadow','none')
    for selector in ['button.flat','button.flat:hover','button.flat:active']:
        expect(css,selector,'box-shadow','none')
    prefix='button.titlebutton' if v=='3' else 'windowcontrols > button'
    for state in ['','hover','active','backdrop']:
        expect(css,prefix+(':'+state if state else ''),'box-shadow','none')
    for state in ['hover','active']:expect(css,prefix+'.close:'+state,'box-shadow','none')
    if v=='4':
        for state in ['',':hover',':active',':backdrop']:
            expect(css,'windowcontrols > button'+state+' > image','background','transparent')
            expect(css,'windowcontrols > button'+state+' > image','box-shadow','none')
    expect(css,prefix+(':focus' if v=='3' else ':focus-visible'),'box-shadow',html('.window-control:focus-visible','box-shadow'))


    expect(css,prefix+(":focus" if v=="3" else ":focus-visible"),"border-color",html(".window-control.is-focus","border-color"))

print('Parsed CSS semantic-shadow and titlebar-state contracts passed (source inspection)')
