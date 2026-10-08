from pathlib import Path
import xml.etree.ElementTree as ET
root=Path(__file__).resolve().parents[1]
for v in ('3','4'):
    for f in ('colors.css','gtk.css','gtk-dark.css'): assert (root/f'theme/Majoris/gtk-{v}.0'/f).is_file()
    spinner=ET.parse(root/f'theme/Majoris/gtk-{v}.0/assets/spinner.svg').getroot()
    assert spinner.attrib['viewBox']=='0 0 20 20'
    assert all(element.attrib['stroke-width']=='2' for element in spinner)
    css=(root/f'theme/Majoris/gtk-{v}.0/gtk.css').read_text()
    assert '-gtk-icon-source: url("assets/spinner.svg")' in css
    assert 'animation: majoris-spin 800ms linear infinite' in css
assert "install_subdir('theme/Majoris'" in (root/'meson.build').read_text()
for p in (root/'icons/Majoris/scalable/ui').glob('*.svg'):
    svg=ET.parse(p).getroot(); assert svg.attrib['viewBox']=='0 0 16 16'
assert 'Inherits=Adwaita,hicolor' in (root/'icons/Majoris/index.theme').read_text()
print('Theme installation tree and SVGs passed')
