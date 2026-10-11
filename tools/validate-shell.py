"""Static CSS grammar and selector validation against installed Trixie resources."""
import re,subprocess,os
from pathlib import Path
import tinycss2
from shell_contract import validate
root=Path(__file__).resolve().parents[1]
css=(root/('theme/Majoris/gnome-shell/gnome-shell-dark.css' if os.environ.get('MAJORIS_VARIANT')=='dark' else 'theme/Majoris/gnome-shell/gnome-shell.css')).read_text()
validate(css,os.environ.get('MAJORIS_VARIANT','light'))
rules=tinycss2.parse_stylesheet(css,skip_whitespace=True,skip_comments=True)
for rule in rules:
    assert rule.type=='qualified-rule',str(rule)
    declarations=tinycss2.parse_declaration_list(rule.content,skip_whitespace=True,skip_comments=True)
    assert all(d.type=='declaration' for d in declarations),declarations
    assert all(t.type!='error' for d in declarations for t in d.value)
resource=Path('/usr/share/gnome-shell/gnome-shell-theme.gresource')
if resource.exists():
    stock=subprocess.check_output(['gresource','extract',str(resource),'/org/gnome/shell/theme/gnome-shell-light.css'],text=True)
    for selector in ['.panel-button','.popup-menu-content','.popup-menu-item','.quick-toggle','.quick-slider','.calendar-day','.calendar-today','.message','.modal-dialog','.search-entry','.dash-label','.workspace-thumbnail']:
        assert selector in stock,'Selector absent from installed Shell CSS: '+selector
    print('Shell CSS grammar and Trixie selector reference passed (not Shell runtime validation)')
else:
    raise SystemExit('Install gnome-shell-common to validate selectors against Trixie')
