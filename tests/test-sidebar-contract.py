from css_contract import rules, expect, html, ROOT
import json
for version in ('3','4'):
 for variant in ('light','dark'):
  css=rules(version,variant)
  for root in ('.sidebar','.navigation-sidebar','.majoris-sidebar'):
   expect(css,root,'padding','16px 8px')
   assert 'min-width' not in css[root] and 'width' not in css[root]
   expect(css,root+' row','min-height','32px')
   expect(css,root+' row','margin','0 0 4px')
   expect(css,root+' row','padding','0 8px')
   expect(css,root+' row','font-size','14px')
   expect(css,root+' row','font-weight','500')
   expect(css,root+' row:selected','font-weight','600')
   expect(css,root+' row','border-radius','4px')
   for state in ('selected','selected:hover','selected:active'):
    image=css[root+' row:'+state]['background-image']
    assert '8px' in image
   for state in ('hover','active','disabled','backdrop','selected:backdrop'):
    assert root+' row:'+state in css
   expect(css,root+' row:selected:dir(rtl)','background-position','right')
   expect(css,root+' row:disabled:hover','background-image','none')
   expect(css,root+'.majoris-sidebar-native-divider','border-right','none')
   expect(css,root+' row:selected','background-size','2px 100%')
   assert 'inset 0 0 0 2px' in css[root+' row:'+('focus-visible' if version=='4' else 'focus')]['box-shadow']
  expect(css,'.majoris-sidebar-heading','font-size','12px')
  expect(css,'.majoris-sidebar-heading','font-weight','600')
  expect(css,'.majoris-sidebar .majoris-sidebar-badge','font-size','12px')
  assert not css.get('row',{}).get('padding')
assert html('.nav','min-height')=='32px' and html('.nav','margin-bottom')=='4px'
assert html('.nav.active:before','top')==html('.nav.active:before','bottom')=='8px'
for variant in ('light','dark'):
 t=json.loads((ROOT/('design/tokens-dark.json' if variant=='dark' else 'design/tokens.json')).read_text())
 assert '224px' in t['css_rules']['.shell']['grid-template-columns']
assert 'SidebarRow("Documents","folder-symbolic")' in (ROOT/'factory/src/headerbar-tests.vala').read_text()
print('Sidebar geometry, roles, explicit states, RTL, native divider ownership and references passed')
