"""Canonical toolbar tokens, selector isolation and unchanged primitive contracts."""
import sys,json
from css_contract import ROOT,rules,expect
sys.path.insert(0,str(ROOT/'tools'))
from design import html_value
from generate_toolbar import toolbar_values,toolbar_template
for version in ('3','4'):
 for variant in ('light','dark'):
  tokens=json.loads((ROOT/'design'/('tokens-dark.json' if variant=='dark' else 'tokens.json')).read_text())
  values=toolbar_values(tokens);css=rules(version,variant)
  assert values['toolbar_content']=='32px' and values['toolbar_icon_padding']=='7px'
  expect(css,'.majoris-toolbar','min-height','32px');expect(css,'.majoris-toolbar','padding','4px 8px')
  expect(css,'.majoris-toolbar','box-shadow','none');
  if version=='4':expect(css,'.majoris-toolbar','border-spacing','0')
  expect(css,'.majoris-toolbar-group-gap','margin-left','4px')
  expect(css,'.majoris-toolbar-major-groups > .majoris-toolbar-group-gap','margin-left','12px')
  expect(css,'button.majoris-toolbar-control:disabled','opacity','.58')
  expect(css,'button.majoris-toolbar-control.majoris-toolbar-item-flat','font-weight','500')
  expect(css,'button.majoris-toolbar-control.majoris-toolbar-item-flat:checked','font-weight','600')
  expect(css,'button.majoris-toolbar-control','min-height','30px')
  expect(css,'button.majoris-toolbar-icon','padding','7px');expect(css,'.majoris-toolbar-view-switcher','min-height','24px')
  expect(css,'.majoris-toolbar-view-switcher','padding','3px');expect(css,'.majoris-toolbar-view-switcher','border-radius','4px')
  expect(css,'.majoris-toolbar-view-switcher > button','min-height','20px')
  expect(css,'button','min-height','30px');expect(css,'button','border-radius','4px')
  if version=='4':expect(css,'.majoris-editor-toolbar > button','min-height','26px')
  text=toolbar_template(version)
  import tinycss2
  for rule in tinycss2.parse_stylesheet(text,skip_comments=True,skip_whitespace=True):
   if rule.type!='qualified-rule':continue
   selectors=tinycss2.serialize(rule.prelude).split(',')
   assert all('majoris-toolbar' in selector for selector in selectors),selectors
  assert '.majoris-toolbar button' not in text,'Broad descendant rule could leak into crumbs or popovers'
  assert 'majoris-editor-toolbar' not in text
  assert values['toolbar_compact_content']=='26px' and values['toolbar_compact_icon_padding']=='5px'
  expect(css,'.majoris-toolbar-segmented','min-height','24px')
  assert '.majoris-toolbar-navigation|background' not in text and '.majoris-toolbar-commands|background' not in text
print('Toolbar border-box derivation, canonical palettes, opt-in scope and editor isolation passed')
