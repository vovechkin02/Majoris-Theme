"""Summarize and compare the existing native menu matrix after Meson tests."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
base = root / 'artifacts/menu-v2/after'
report = []
for toolkit in ('3', '4'):
    for scale in ('1', '2'):
        samples = {}
        for variant in ('light', 'dark'):
            directory = base / f'gtk{toolkit}-{variant}-{scale}x'
            records = json.loads((directory / 'keycap-measurements.json').read_text())
            samples[variant] = [(item['key'], item['allocation'], item['logical'], item['ink']) for item in records]
        assert samples['light'] == samples['dark'], (toolkit, scale, 'keycap geometry differs between variants')
        report.append({'toolkit': toolkit, 'scale': scale, 'light_dark_geometry_equal': True, 'keycaps_measured': len(samples['light'])})
output = base.parent / 'geometry-comparison.json'
output.write_text(json.dumps(report, indent=2) + '\n')
print('Light/dark native keycap geometry matches in all four toolkit/scale pairs')
