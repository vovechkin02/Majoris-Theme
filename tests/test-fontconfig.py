import sys,subprocess,xml.etree.ElementTree as ET
from css_contract import ROOT
aliases=ET.parse(ROOT/'fonts/fontconfig/65-majoris-fonts.conf').getroot().findall('alias')
for family in ('sans-serif','system-ui'):
    alias=next(a for a in aliases if a.findtext('family')==family)
    assert alias.attrib.get('binding')=='strong'
    assert [f.text for f in alias.findall('prefer/family')][:3]==['Plus Jakarta Sans','Noto Sans','Cantarell']
if '--runtime' in sys.argv:
    resolved=subprocess.check_output(['fc-match','-f','%{family}','Plus Jakarta Sans'],text=True)
    if 'Plus Jakarta Sans' not in resolved:
        print('SKIP: exact Plus Jakarta Sans absent; resolved '+resolved);sys.exit(77)
    for family in ('sans-serif','system-ui'):
        assert 'Plus Jakarta Sans' in subprocess.check_output(['fc-match','-f','%{family}',family],text=True)
print('Strong sans-serif and system-ui aliases passed')
