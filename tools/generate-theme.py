"""Generate native CSS from token placeholders. Run after editing design/templates."""
import json,re,sys
from design import ROOT
t=json.loads((ROOT/'design/tokens.json').read_text())
def output(path,content):
    if '--check' in sys.argv:
        assert path.read_text()==content,'Generated theme drift: '+str(path.relative_to(ROOT))
    else: path.write_text(content)
values={**t['color'], **{k+'_radius':str(v)+'px' for k,v in t['radius'].items()}, **{k+'_motion':v for k,v in t['motion_css'].items()}, **{k+'_shadow':v for k,v in t['shadow'].items()}, **{k:str(v)+'px' for k,v in t['window'].items()}}
values['control_content_size']=str(t['window']['window_control_size']-2)+'px'
values['header_padding']=str((t['window']['headerbar_height']-t['window']['window_control_size'])//2)+'px'
values['control_duration']=str(t['motion']['control_ms'])+'ms'
values['surface_duration']=str(t['motion']['surface_ms'])+'ms'
def render(s):
    return re.sub(r'\$\{(\w+)\}',lambda m:values[m[1]],s)
colors='/* Generated from design/tokens.json. */\n'+''.join('@define-color '+k+' '+v+';\n' for k,v in t['color'].items())
colors+=''.join('@define-color '+k+' @'+v+';\n' for k,v in {'accent_color':'primary_500','accent_bg_color':'primary_500','accent_fg_color':'surface','window_bg_color':'background','window_fg_color':'text','view_bg_color':'surface','view_fg_color':'text','headerbar_bg_color':'surface','headerbar_fg_color':'text','card_bg_color':'surface','card_fg_color':'text','popover_bg_color':'surface','popover_fg_color':'text','dialog_bg_color':'surface','dialog_fg_color':'text','destructive_bg_color':'danger','destructive_fg_color':'surface','success_bg_color':'success','warning_bg_color':'warning','theme_bg_color':'background','theme_fg_color':'text','theme_base_color':'surface','theme_text_color':'text','theme_selected_bg_color':'primary_500','theme_selected_fg_color':'surface'}.items())
for version in ('3','4'):
    directory=ROOT/f'theme/Majoris/gtk-{version}.0'
    directory.mkdir(parents=True,exist_ok=True)
    output(directory/'colors.css',colors)
    shared=(ROOT/'design/templates/gtk-common.css.in').read_text()
    specific=(ROOT/f'design/templates/gtk{version}.css.in').read_text()
    base='@import url("resource:///org/gtk/libgtk/theme/Adwaita/gtk-contained.css");\n' if version=='3' else ''
    output(directory/'gtk.css','/* Generated; edit design/templates and regenerate. */\n'+base+'@import url("colors.css");\n'+render(shared+specific))
    output(directory/'gtk-dark.css','/* Dark design pending: deliberately uses the specified light palette. */\n@import url("gtk.css");\n')
p=ROOT/'theme/Majoris/gnome-shell/gnome-shell.css'
p.parent.mkdir(parents=True,exist_ok=True)
output(p,'/* Generated from Majoris HTML tokens. */\n'+render((ROOT/'design/templates/shell.css.in').read_text()))
