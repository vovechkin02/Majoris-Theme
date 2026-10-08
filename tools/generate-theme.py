"""Generate native CSS from token placeholders. Run after editing design/templates."""
import json,re,sys
from design import ROOT,html_value
t=json.loads((ROOT/'design/tokens.json').read_text())
def output(path,content):
    if '--check' in sys.argv:
        assert path.read_text()==content,'Generated theme drift: '+str(path.relative_to(ROOT))
    else: path.write_text(content)
values={**t['color'], **{k+'_radius':str(v)+'px' for k,v in t['radius'].items()}, **{k+'_motion':v for k,v in t['motion_css'].items()}, **{k+'_shadow':v for k,v in t['shadow'].items()}, **{k:str(v)+'px' for k,v in t['window'].items()}}
values['control_content_size']=str(t['window']['window_control_size']-2)+'px'
values['header_padding']=html_value(t,'.headerbar','padding')
# HTML border-box height includes its divider; GTK min-height excludes padding/border.
remaining=t['window']['headerbar_height']-t['window']['window_control_size']-1
values['header_padding_top']=str(remaining//2)+'px'
values['header_padding_bottom']=str(remaining-remaining//2)+'px'
values['entry_content_width']=str(int(html_value(t,'.entry','min-width')[:-2])-22)+'px'
values['dropdown_content_width']=str(int(html_value(t,'.select','min-width')[:-2])-26)+'px'
values['preference_content_height']=str(int(html_value(t,'.pref-row','min-height')[:-2])-17)+'px'
values['banner_button_content_height']=str(int(html_value(t,'.banner .btn','height')[:-2])-2)+'px'
values['control_duration']=str(t['motion']['control_ms'])+'ms'
values['surface_duration']=str(t['motion']['surface_ms'])+'ms'
def render(s):
    s=re.sub(r'\$\{([^|}]+)\|([^}]+)\}',lambda m:html_value(t,m[1],m[2]),s)
    return re.sub(r'\$\{(\w+)\}',lambda m:values[m[1]],s)
colors='/* Generated from design/tokens.json. */\n'+''.join('@define-color '+k+' '+v+';\n' for k,v in t['color'].items())
colors+=''.join('@define-color '+k+' @'+v+';\n' for k,v in {'accent_color':'primary_500','accent_bg_color':'primary_500','accent_fg_color':'surface','window_bg_color':'background','window_fg_color':'text','view_bg_color':'surface','view_fg_color':'text','headerbar_bg_color':'surface','headerbar_fg_color':'text','card_bg_color':'surface','card_fg_color':'text','popover_bg_color':'surface','popover_fg_color':'text','dialog_bg_color':'surface','dialog_fg_color':'text','destructive_bg_color':'danger','destructive_fg_color':'surface','success_bg_color':'success','warning_bg_color':'warning','theme_bg_color':'background','theme_fg_color':'text','theme_base_color':'surface','theme_text_color':'text','theme_selected_bg_color':'primary_500','theme_selected_fg_color':'surface'}.items())
for version in ('3','4'):
    directory=ROOT/f'theme/Majoris/gtk-{version}.0'
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'assets').mkdir(exist_ok=True)
    # Border-top spinner: 20px border-box, 2px stroke, exact HTML palette.
    output(directory/'assets/spinner.svg','<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="9" fill="none" stroke="'+t['color']['primary_200']+'" stroke-width="2"/><path d="M3.63604 3.63604 A9 9 0 0 1 16.36396 3.63604" fill="none" stroke="'+t['color']['primary_600']+'" stroke-width="2"/></svg>\n')
    output(directory/'colors.css',colors)
    shared=(ROOT/'design/templates/gtk-common.css.in').read_text()
    specific=(ROOT/f'design/templates/gtk{version}.css.in').read_text()
    if version=='4':
        # GTK4 distinguishes keyboard-visible button focus; entries keep focus
        # styling because the reference intentionally uses entry:focus.
        shared=re.sub(r'(button(?:\.[\w-]+)?):focus\b',r'\1:focus-visible',shared)
    if version=='3':
        shared=shared.replace('${.tab.active|font-weight}', '600').replace('${.nav.active|font-weight}', '600')
        # GTK3 gradients do not support calc(); tabs use a label-owned underline
        # below, and sidebar rows have a fixed 34px target so percentage stops
        # faithfully reproduce the HTML's 9px vertical insets.
        shared=shared.replace('transparent 10px, @primary_500 10px','transparent 10%, @primary_500 10%').replace('calc(100% - 10px)','90%')
        shared=shared.replace('transparent 9px, @primary_500 9px, @primary_500 calc(100% - 9px), transparent calc(100% - 9px)', 'transparent 26.470588%, @primary_500 26.470588%, @primary_500 73.529412%, transparent 73.529412%')
    base='@import url("resource:///org/gtk/libgtk/theme/Adwaita/gtk-contained.css");\n' if version=='3' else ''
    output(directory/'gtk.css','/* Generated; edit design/templates and regenerate. */\n'+base+'@import url("colors.css");\n'+render(shared+specific))
p=ROOT/'theme/Majoris/gnome-shell/gnome-shell.css'
p.parent.mkdir(parents=True,exist_ok=True)
output(p,'/* Generated from Majoris HTML tokens. */\n'+render((ROOT/'design/templates/shell.css.in').read_text()))

from generate_dark import generate
generate(output)
