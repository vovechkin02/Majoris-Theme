"""Canonical extraction, scoped selectors and geometry parity."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from design import extract
from css_contract import rules,expect
scale=dict(none=0,compact=4,standard=8,section=16,major=32)
for variant in ('light','dark'):
 t=json.loads((ROOT/('design/tokens.json' if variant=='light' else 'design/tokens-dark.json')).read_text());assert t['spacing']==scale==extract(variant)['spacing']
 css=rules('4',variant)
 expect(css,'preferencesgroup > box > box:not(.header)','border-spacing','8px')
 for cls,target in [('majoris-control-stack',8),('majoris-compact-stack',4),('majoris-section-stack',16),('majoris-major-stack',32),('majoris-connected-group',0)]:expect(css,'box.'+cls,'border-spacing',str(target)+'px')
 assert 'box' not in css or 'border-spacing' not in css['box']
 for node in ('button','entry','label','switch'):
  assert not any(key.startswith('margin') for key in css.get(node,{})),node
 gtk3=(ROOT/'design/templates/gtk3-spacing.css.in').read_text();assert 'preferencesgroup' not in gtk3 and 'border-spacing:' not in gtk3
print('Spacing tokens, scoped container ownership, GTK3 boundary and geometry parity pass')
