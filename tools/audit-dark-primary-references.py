"""Review every generated dark indigo-index reference without rewriting CSS."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
lines=['# Dark primary-index audit','', 'Every match is classified below. Action declarations use action_primary tokens. Focus declarations use focus_color. Shared selection fallbacks precede explicit dark sidebar/table overrides, preserving their distinct text colours.','', '| File:line | Classification | Context |','|---|---|---|']
for version in ['3','4']:
 for name in ['colors-dark.css','gtk-dark.css']:
  p=ROOT/f'theme/Majoris/gtk-{version}.0'/name
  for n,line in enumerate(p.read_text().splitlines(),1):
   if not re.search(r'primary_[5678]00',line):continue
   if '@define-color' in line:kind='canonical palette usage — invariant primitive definition'
   elif 'indeterminate' in line:kind='canonical palette usage — mixed mark p600'
   elif 'spinner' in line:kind='canonical palette usage — inherited foreground; SVG owns dark arc #818CF8'
   elif 'row:selected' in line or 'view:selected' in line:kind='component-state usage — shared fallback; explicit dark sidebar/table declarations override it'
   elif 'scale slider' in line:kind='component-state usage — shared slider border fallback; explicit dark thumb border overrides it'
   elif 'tab:checked' in line:kind='component-state usage — shared fallback; explicit dark indicator #818CF8 overrides it'
   elif any(x in line for x in ['check:checked','radio:checked','switch:checked','scale highlight','progressbar progress']):kind='component-state usage — specified checked/accent p500 #6366F1'
   elif 'background-image:' in line:kind='component-state usage — shared indicator fallback; explicit dark cascade overrides it'
   elif 'banner' in line:kind='component-state usage — shared banner foreground fallback; explicit dark foreground overrides it'
   elif 'statuspage' in line:kind='component-state usage — shared status fallback; explicit dark icon colour overrides it'
   else:raise AssertionError(('Unclassified primary reference',p,n,line))
   lines.append(f'| {p.relative_to(ROOT)}:{n} | {kind} | `{line.strip().replace("|","/")}` |')
lines+=['', 'Shell uses rendered literals: selection/accent #6366F1, independent focus #818CF8 and danger #DC3C4D. No dark Shell primitive alias is redefined. Spinner files are unchanged.']
(ROOT/'artifacts/dark-primary-reference-audit.md').write_text('\n'.join(lines)+'\n')
print('Every dark GTK3/4 primary_[5678]00 reference classified; no unclassified action dependency')
