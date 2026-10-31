"""Actual rules, native hierarchy, canonical generation and isolation contracts."""
import sys,json
from pathlib import Path
from css_contract import ROOT,rules,expect
sys.path.insert(0,str(ROOT/'tools'))
from design import extract,html_value
for variant in ['light','dark']:
 tokens=extract(variant)
 assert tokens==json.loads((ROOT/'design'/('tokens-dark.json' if variant=='dark' else 'tokens.json')).read_text())
 css=rules('4',variant)
 for selector in ['calendar.view > grid > label.day-number','button.link','editablelabel.editing > stack > text','paned.horizontal > separator','flowbox.majoris-flow-tiles > flowboxchild:selected','expander-widget:not(.majoris-sidebar-group) > box > title','searchbar > revealer > box']:
  assert selector in css,selector
 expect(css,'button.link','min-height','0');expect(css,'button.link','padding','0');expect(css,'button.link','box-shadow','none')
 expect(css,'button','min-height','30px');expect(css,'button','border-radius','4px')
 expect(css,'calendar.view > grid > label.day-number','min-height','32px');expect(css,'calendar.view > grid > label.day-number','border-radius','4px')
 expect(css,'paned.horizontal > separator','min-width','8px');expect(css,'paned.horizontal > separator','background-size','1px 100%')
 expect(css,'editablelabel.editing > stack > text','border-radius','4px');expect(css,'editablelabel > stack > text','padding','0')
 expect(css,'flowbox.majoris-flow-tiles > flowboxchild','border-radius','8px')
 expect(css,'expander-widget:not(.majoris-sidebar-group) > box > title','min-height','32px')
 for version in ['3','4']:
  text=(ROOT/f'design/templates/gtk{version}-phase2.css.in').read_text()
  assert '!important' not in text and 'windowcontrols' not in text and '.boxed-list' not in text
  import re
  assert not re.search(r'(?m)^(?:searchentry|row)\s*\{',text)
  if version=='3':assert 'editablelabel' not in text and 'expander:not(.majoris-sidebar-group) > title > arrow' in text and 'border-spacing:' not in text
 native=(ROOT/'factory/src/phase2-controls.vala').read_text()
 for cls in ['Calendar','LinkButton','EditableLabel','Paned','FlowBox','Expander','SearchBar']:assert 'new Gtk.'+cls in native
 assert 'phase2-controls.vala' in (ROOT/'factory/meson.build').read_text()
print('Phase2 native selectors, canonical geometry, toolkit hierarchy and isolation passed')
