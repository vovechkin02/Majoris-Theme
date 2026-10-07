from css_contract import *
for v in ('3','4'):
    css=rules(v)
    for selector in ['button','entry','check','notebook > header tab','tooltip']:
        expect(css,selector,'border-radius',html('.tooltip' if selector=='tooltip' else '.checkbox','border-radius'))
    for selector in ['.card','.boxed-list','dialog']:expect(css,selector,'border-radius',str(TOKENS['radius']['structure'])+'px')
    expect(css,'radio','border-radius',html('.radio','border-radius'))
    expect(css,'switch','border-radius',html('.switch','border-radius'))
    expect(css,'switch slider','border-radius',html('.switch:after','border-radius'))
    for selector in ['.majoris-segmented','viewswitcher','stackswitcher']:expect(css,selector,'border-radius',html('.toggle-group','border-radius'))
    expect(css,'levelbar block','border-radius',html('.level span','border-radius'))
    expect(css,'button.titlebutton' if v=='3' else 'windowcontrols > button','border-radius',html('.window-control','border-radius'))
print('Parsed CSS component radii and exceptions agree with HTML')
