from css_contract import *
for v in ('3','4'):
    css=rules(v)
    pairs=[('.navigation-sidebar row:selected','color','@primary_700'),('.majoris-data-view row:selected','color','@primary_800'),('button.suggested-action','background-color','@primary_600'),('levelbar block.filled','background-color','@success'),('progressbar trough','background-color',html('.progress','background')),('levelbar block.empty','background-color',html('.level span','background')),('scale trough','background-color',html('.track','background')),('tooltip','background-color',html('.tooltip','background')),('scrollbar slider','background-color',html('.scroll-thumb','background'))]
    for selector,prop,value in pairs:expect(css,selector,prop,value)
css=rules('4')
expect(css,'button.majoris-menu-danger','color','@danger')
expect(css,'toast','background-color',html('.toast','background'))
expect(css,'windowcontrols > button.close:hover','background-color','@danger')
expect(css,'windowcontrols > button.close:active','background-color','@danger_pressed')
print('Parsed CSS semantic colors agree with HTML; navigation and data selection remain distinct')

import runpy
runpy.run_path(str(ROOT/'tests/test-surgical-colour-contract.py'))
