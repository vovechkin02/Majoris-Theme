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

# Both variants and both toolkits retain controls/structures and scoped segments.
for version in ('3','4'):
    for variant in ('light','dark'):
        css=rules(version,variant)
        for group in ('.majoris-segmented','viewswitcher','stackswitcher'):
            expect(css,group,'border-radius','4px')
            expect(css,group,'padding','2px')
            expect(css,group+' button','border-radius','2px')
            expect(css,group+' button','min-height','28px')
            expect(css,group+' button','font-weight','500')
            expect(css,group+' button:checked','font-weight','600')
        for group in ('.majoris-toolbar-segmented','.majoris-toolbar-view-switcher'):
            expect(css,group,'border-radius','4px')
            expect(css,group,'padding','3px')
            expect(css,group,'min-height','24px')
            expect(css,group+' > button','border-radius','2px')
        expect(css,'button','border-radius','4px')
        expect(css,'.card','border-radius','8px')
assert html('.toggle','border-radius')=='4px'
assert html('.toggle-group .toggle','border-radius')=='2px'

for version in ("3","4"):
    for variant in ("light","dark"):
        css=rules(version,variant)
        expect(css,"switch","border-radius","4px")
        expect(css,"switch slider","border-radius","4px")
        expect(css,"switch","min-width","34px")
        expect(css,"switch","min-height","16px")
        expect(css,"switch","padding","2px")
