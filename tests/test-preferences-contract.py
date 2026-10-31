from css_contract import *
for variant in ('light','dark'):
 for version in ('3','4'):
  css=rules(version,variant)
  assert 'row:hover' not in css
  expect(css,'row.activatable:hover','background-color','@hover')
  expect(css,'.boxed-list > row','padding','8px 16px')
  expect(css,'.boxed-list > row','border-radius','0')
  expect(css,'.boxed-list','border-radius','8px')
  expect(css,'.boxed-list > row:first-child','border-top-left-radius','7px')
  expect(css,'.boxed-list > row:last-child','border-bottom-right-radius','7px')
  expect(css,'.boxed-list > row:not(.activatable):hover','background-color','transparent')
  assert '.boxed-list > row label' not in css
  if version=='4':
   title='.boxed-list row > box.header > box.title > label.title'
   sub='.boxed-list row > box.header > box.title > label.subtitle'
   expect(css,title,'font-size','10.5pt');expect(css,title,'font-weight','500')
   expect(css,sub,'font-size','9pt');expect(css,sub,'font-weight','400')
   assert 'min-height' not in css[title] and 'min-height' not in css[sub]
   heading='preferencesgroup > box > box.header > box.labels > label.heading'
   expect(css,heading,'font-size','10.5pt');expect(css,heading,'font-weight','600')
   expect(css,'preferencesgroup > box','border-spacing','8px')
   expect(css,'preferencesgroup > box > box.header > box.labels','border-spacing','4px')
   expect(css,'.boxed-list row > box.header > box.title','border-spacing','4px')
   expect(css,'switch','border-radius','4px');expect(css,'switch slider','border-radius','4px')
print('Scoped preferences typography, semantic hover, spacing and switch invariants pass')
