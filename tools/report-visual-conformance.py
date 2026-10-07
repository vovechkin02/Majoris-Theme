"""Generate an evidence-linked report from explicit human/agent visual reviews.

This never converts passing source tests into visual PASS automatically.
"""
import hashlib,json,collections
from pathlib import Path
root=Path(__file__).resolve().parents[1]
review=json.loads((root/'docs/visual-review.json').read_text())
out=root/'artifacts';captures=out/'screenshots'
metadata=json.loads((captures/'capture-metadata.json').read_text())
reference=json.loads((captures/'html/render-metadata.json').read_text())
source=root/reference['source']
assert hashlib.sha256(source.read_bytes()).hexdigest()==reference['sha256'],'Reference changed since render'
geometry=json.loads((out/'geometry.json').read_text())
results=[json.loads(line) for line in (root/'build/meson-logs/testlog.json').read_text().splitlines()]
counts=collections.Counter(result['result'] for result in results)
assert counts.get('FAIL',0)==0 and counts.get('ERROR',0)==0,counts
lines=['# Visual conformance report — '+review['review_date'],'',review['scope'],'',
       'Review basis: complete native captures, separate complete popup/tooltip surfaces, unchanged full HTML reference, native geometry/colors and parsed source contracts. Images are neither cropped nor altered. Root xwd omitted override-redirect popup surfaces on this setup; the complete popup captures are separate evidence, not composited into another image.','',
       '## Reproduction and evidence','',
       '`scripts/render-html-reference.sh`; `scripts/capture-visual-regressions.sh`; `python3 tools/report-visual-conformance.py`. Update the reviewed observations after inspecting changed captures.','',
       'Native conditions: '+json.dumps(metadata,ensure_ascii=False)+'.','',
       'HTML conditions: '+json.dumps(reference,ensure_ascii=False)+'.','',
       'Meson results: '+json.dumps(dict(counts))+'. Exact font verification is skipped when the font is absent.','',
       '[Full unchanged reference](screenshots/html/full-reference.png) · [Reference overview](screenshots/html/overview.png) · [Geometry JSON](geometry.json) · [Meson log](testlog.txt)','',
       '## Native header geometry','',
       '| Fixture | Content | Padding total | Divider | Border-box allocation |','|---|---:|---:|---:|---:|']
for name in ('simple_headerbar','dense_headerbar','split_sidebar_headerbar','split_content_headerbar'):
    h=geometry[name];lines.append(f"| {name} | {h['content_height']} | {h['allocation_height']-h['content_height']-h['divider']} | {h['divider']} | {h['allocation_height']} |")
lines+=['','## Component review','','| Section | HTML reference | Native evidence | Result | Reason |','|---|---|---|---|---|']
for section,file,status,reason in review['rows']:
    assert status in ('PASS','PARTIAL','FAIL')
    assert (captures/file).is_file(),file
    lines.append(f'| {section} | [Full reference](screenshots/html/full-reference.png) | [{file}](screenshots/{file}) | {status} | {reason} |')
lines+=['','## Final acceptance boundaries','','Every PARTIAL row states why equivalence is not certified. Exact typography and real Majoris VM validation remain open. Native diagnostics demonstrate CSS states; pointer/keyboard behavior and compositor integration still require the target desktop. No pixel-perfect equality is claimed.','',
        'The [fresh audit](../docs/visual-conformance-audit.md), [implementation report](../docs/implementation-report.md) and [exact changed-file manifest](../docs/changed-files.txt) document the fixes, newly discovered differences, tests and remaining work.','']
(out/'visual-conformance-report.md').write_text('\n'.join(lines))
print('Generated artifacts/visual-conformance-report.md from reviewed observations')
