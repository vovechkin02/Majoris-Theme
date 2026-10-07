from pathlib import Path
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
for v in ('3','4'):
    for f in ('colors.css','gtk.css','gtk-dark.css'): assert (root/f'theme/Majoris/gtk-{v}.0'/f).is_file()
for p in (root/'icons/Majoris/scalable/ui').glob('*.svg'):
    svg=ET.parse(p).getroot(); assert svg.attrib['viewBox']=='0 0 16 16'
assert 'Inherits=Adwaita,hicolor' in (root/'icons/Majoris/index.theme').read_text()
print('Theme installation tree and SVGs passed')
