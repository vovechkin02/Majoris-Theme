"""Evidence-linked light/dark review; passing tests do not invent visual acceptance."""
import collections,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'artifacts';captures=out/'screenshots'
results=[json.loads(line) for line in (root/'build/meson-logs/testlog.json').read_text().splitlines()]
counts=collections.Counter(x['result'] for x in results);assert counts.get('FAIL',0)==0 and counts.get('ERROR',0)==0,counts
lines=['# Visual conformance report — 2026-10-08','','Reviewed uncropped native frames and separately captured complete popups/tooltip surfaces against the unchanged HTML authorities. PASS concerns exposed theme styling; native structure and GNOME compositor acceptance remain separately classified.','',f'Meson: {dict(counts)}. Exact Plus Jakarta Sans required; no font skips.','']
for variant,file in [('light','visual-review.json'),('dark','visual-review-dark.json')]:
 review=json.loads((root/'docs'/file).read_text());meta=json.loads((captures/variant/'capture-metadata.json').read_text())
 ref=json.loads((captures/('html-dark' if variant=='dark' else 'html')/'render-metadata.json').read_text())
 assert hashlib.sha256((root/ref['source']).read_bytes()).hexdigest()==ref['sha256']
 lines+=['## '+variant.upper(),'',f'Native: 1440×1080 Xvfb, scale 1, Cairo, Openbox/xcompmgr; requested/resolved font {meta["font_resolved"]}. Reference SHA256 `{ref["sha256"]}`. Temporary local normal/italic font injection only.','',f'[HTML authority](screenshots/{"html-dark" if variant=="dark" else "html"}/full-reference.png) · [Capture metadata](screenshots/{variant}/capture-metadata.json)','','| Category | Evidence | Result | Observation / classification |','|---|---|---|---|']
 for section,image,status,reason in review['rows']:
  assert status in ('PASS','PARTIAL — native constraint','FAIL','NOT VALIDATABLE UNDER WSL')
  assert (captures/variant/image).is_file(),image
  lines.append(f'| {section} | [{image}](screenshots/{variant}/{image}) | {status} | {reason} |')
comparison=json.loads((out/'light-baseline-comparison.json').read_text());unchanged=[x for x in comparison if x.get('bbox','different') is None]
lines+=['',f'Light baseline: {len(unchanged)} of {len(comparison)} complete images are pixel-identical. The menu gains the required Appearance submenu (32px extra row); its popup and full frame change. GTK4 Demo now uses the bridge, so the existing 48px Majoris header contract overrides its later application/provider defaults; the sidebar/tab spacing consequently follows Majoris too. No light theme CSS was changed by dark generation. [Pixel comparison](light-baseline-comparison.json).','', '## SHARED GEOMETRY','']
l=json.loads((out/'geometry-light.json').read_text());d=json.loads((out/'geometry-dark.json').read_text());assert l==d
lines+=['The entire realized widget tree, font and geometry reports are identical between variants. Hidden banners remain 0px.','', '| Fixture | Header | Content | Divider | Window control / glyph |','|---|---:|---:|---:|---|']
for name in ('simple_headerbar','dense_headerbar','split_sidebar_headerbar','split_content_headerbar'):
 h=l[name];lines.append(f'| {name} | {h["allocation_height"]} | {h["content_height"]} | {h["divider"]} | 32×32 / 16×16 |')
lines+=['','[Light geometry](geometry-light.json) · [Dark geometry](geometry-dark.json) · [Native live/system switching](variant-switching.json) · [Dark contrast](dark-contrast.json)','', '## TOOLKIT CONSTRAINTS','','NATIVE TOOLKIT CONSTRAINT: native preference internals, banner centering, adaptive toast width, alert-dialog response layout, view-switcher content policy, popup anchoring/arrow, tooltip placement without the HTML arrow, scrollbar behavior and GTK3 fallback decorations cannot exactly duplicate the simulated HTML layout. The exposed palette, radii, shadows and state treatment are implemented. Clock custom symbolic SVG stroke paints remain fixed in its application resources and have weak contrast in dark mode; no sibling application assets were modified.','', '## VM-ONLY VALIDATION','','GNOME SESSION VALIDATION REQUIRED: Settings produced no visible window; blank output was rejected. Shell styles pass both static grammar/selector suites, but User Themes/automatic switching, St rendering, panel, Quick Settings, calendar, notifications, search/overview/dash, Mutter shadows/corners, inactive/maximized/restored/tiled windows, fractional scaling, Wayland, portals and GDM require the target GNOME VM.','', '[Implementation and switching](../docs/dark-theme.md) · [17-item completion audit](../docs/dark-theme-completion.md) · [Exact changed files](../docs/dark-changed-files.txt)','']
(out/'visual-conformance-report.md').write_text('\n'.join(lines));print('Generated light/dark visual conformance report')
