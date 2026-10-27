"""Scoped source and canonical contracts, supported by native tests."""
from css_contract import *
for variant in ('light','dark'):
 for version in ('3','4'):
  css=rules(version,variant);palette=colors(version,variant)
  assert resolve('@majoris_data_selected_text',palette)==('#3730A3' if variant=='light' else '#E0E7FF')
  assert resolve('@majoris_data_surface',palette)==('#FFFFFF' if variant=='light' else '#202023')
  if version=='4':
   for root,item in [('listview.majoris-data-list',' > row'),('gridview.majoris-data-grid',' > child > .majoris-data-tile'),('columnview.majoris-data-column',' > listview > row'),('columnview.majoris-data-view',' > listview > row')]:
    assert root+item in css
    for state in ('hover','active','selected','selected:hover','selected:active','focus-visible','backdrop','selected:backdrop','disabled'):
     selector=root+(' > child:'+state+' > .majoris-data-tile' if 'grid' in root else item+':'+state)
     assert selector in css,selector
    assert 'background-image' not in css.get(root+item+':selected',{}),'No sidebar stripe'
   assert not any('row:focus-within' in selector and 'majoris-data-' in selector for selector in css)
   expect(css,'columnview.majoris-data-column cell:focus-visible','box-shadow','none')
   expect(css,'listview.majoris-data-list > row','min-height','24px')
   expect(css,'listview.majoris-data-list.majoris-density-compact > row','padding','4px 8px')
   expect(css,'columnview.majoris-data-column cell','min-height','23px')
   expect(css,'gridview.majoris-data-grid .majoris-data-tile','border-radius','8px')
   expect(css,'columnview.majoris-data-column > listview > row','border-radius','0')
   for selector in css:
    if 'majoris-data-' in selector:assert not any(x in selector for x in ('preferences','actionrow','switchrow','combobox','sidebar','notebook','popover','.boxed-list'))
  else:
   assert 'treeview.majoris-data-view:selected' in css and 'iconview.majoris-data-grid:selected' in css
   expect(css,'treeview.majoris-data-view.view:selected:focus','border-radius','0')
   expect(css,'treeview.majoris-data-list.view:selected:focus','border-radius','4px')
   expect(css,'iconview.majoris-data-grid.view:selected:focus','border-radius','8px')
print('Canonical data semantics, scoped families, compatibility, density minima and no selector leakage passed')
