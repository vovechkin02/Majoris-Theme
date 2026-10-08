"""Generate the dark variant from the effective dark HTML cascade."""
import json,re
from design import ROOT,extract,html_value

def generate(output):
    t=extract('dark')
    output(ROOT/'design/tokens-dark.json',json.dumps(t,indent=2)+'\n')
    light=json.loads((ROOT/'design/tokens.json').read_text())
    assert all(t[k]==light[k] for k in ('radius','motion','motion_css','window','font'))
    values={**t['color'],**{k+'_radius':str(v)+'px' for k,v in t['radius'].items()},**{k+'_motion':v for k,v in t['motion_css'].items()},**{k+'_shadow':v for k,v in t['shadow'].items()},**{k:str(v)+'px' for k,v in t['window'].items()}}
    values.update(control_content_size='30px',header_padding=html_value(t,'.headerbar','padding'),header_padding_top='7px',header_padding_bottom='8px',entry_content_width=str(int(html_value(t,'.entry','min-width')[:-2])-22)+'px',dropdown_content_width=str(int(html_value(t,'.select','min-width')[:-2])-26)+'px',preference_content_height='33px',banner_button_content_height=str(int(html_value(t,'.banner .btn','height')[:-2])-2)+'px',control_duration='128ms',surface_duration='256ms')
    def render(s):
        s=re.sub(r'\$\{([^|}]+)\|([^}]+)\}',lambda m:html_value(t,m[1],m[2]),s)
        return re.sub(r'\$\{(\w+)\}',lambda m:values[m[1]],s)
    colors='/* Generated from the effective dark reference cascade. */\n'+''.join('@define-color '+k+' '+v+';\n' for k,v in t['color'].items())
    aliases={'primary_600':'primary_default','primary_700':'primary_hover','primary_800':'primary_pressed','danger':'danger_default','danger_pressed':'danger_pressed','success':'success'}
    colors+=''.join('@define-color '+name+' '+t['semantic_color'][key]+';\n' for name,key in aliases.items())
    for name in ('accent_fg_color','destructive_fg_color','theme_selected_fg_color'): colors+='@define-color '+name+' #FFFFFF;\n'
    for version in ('3','4'):
        directory=ROOT/f'theme/Majoris/gtk-{version}.0'
        output(directory/'colors-dark.css',colors)
        output(directory/'assets/spinner-dark.svg','<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="9" fill="none" stroke="'+html_value(t,'.spinner','border-color')+'" stroke-width="2"/><path d="M3.63604 3.63604 A9 9 0 0 1 16.36396 3.63604" fill="none" stroke="'+html_value(t,'.spinner','border-top-color')+'" stroke-width="2"/></svg>\n')
        shared=(ROOT/'design/templates/gtk-common.css.in').read_text()
        specific=(ROOT/f'design/templates/gtk{version}.css.in').read_text()
        if version=='4': shared=re.sub(r'(button(?:\.[\w-]+)?):focus\b',r'\1:focus-visible',shared)
        else:
            shared=shared.replace('${.tab.active|font-weight}','600').replace('${.nav.active|font-weight}','600').replace('transparent 10px, @primary_500 10px','transparent 10%, @primary_500 10%').replace('calc(100% - 10px)','90%').replace('transparent 9px, @primary_500 9px, @primary_500 calc(100% - 9px), transparent calc(100% - 9px)','transparent 26.470588%, @primary_500 26.470588%, @primary_500 73.529412%, transparent 73.529412%')
        css=render(shared+specific).replace('rgba(99,102,241,.24)','rgba(129,140,248,.34)').replace('alpha(@primary_500,.24)','rgba(129,140,248,.34)').replace('assets/spinner.svg','assets/spinner-dark.svg')
        extra=render((ROOT/'design/templates/gtk-dark.css.in').read_text())
        if version=='3': extra=extra.replace(':focus-visible',':focus').replace('calc(100% - 9px)','73.529412%').replace('transparent 9px, #818CF8 9px','transparent 26.470588%, #818CF8 26.470588%').replace('#818CF8 73.529412%, transparent 73.529412%','#818CF8 73.529412%, transparent 73.529412%')
        if version=='3':
            extra=re.sub(r'notebook > header tab:checked \{ background-image:.*?\}\n', '', extra)
            extra=extra.replace('popover.background { background: transparent; }','')
            extra+=render((ROOT/'design/templates/gtk3-dark.css.in').read_text())
        base='@import url("resource:///org/gtk/libgtk/theme/Adwaita/gtk-contained.css");\n' if version=='3' else ''
        output(directory/'gtk-dark.css','/* Generated: shared geometry, effective dark cascade, native overrides. */\n'+base+'@import url("colors.css");\n@import url("colors-dark.css");\n'+css+extra)
    shell=render((ROOT/'design/templates/shell.css.in').read_text()).replace('color: '+t['color']['surface']+';','color: #FFFFFF;').replace('rgba(99,102,241,.24)','rgba(129,140,248,.34)')
    shell+='\n.dash-label, .tooltip { color: #18181B; background-color: #F4F4F5; box-shadow: '+html_value(t,'.tooltip','box-shadow')+'; }\n.search-entry:focus { border-color: #818CF8; }\n'
    output(ROOT/'theme/Majoris/gnome-shell/gnome-shell-dark.css','/* Generated dark Shell variant. */\n'+shell)
    alias=ROOT/'theme/Majoris-Dark/gnome-shell/gnome-shell.css'
    alias.parent.mkdir(parents=True,exist_ok=True)
    output(alias,'/* Generated dark Shell variant. */\n'+shell)
