"""Generate the dark variant from the effective dark HTML cascade."""
from generate_toolbar import toolbar_values, toolbar_template
from generate_data import data_values
import json,re
from generate_sidebar import sidebar_values
from generate_editor import editor_values
from design import ROOT,extract,html_value

def generate(output):
    t=extract('dark')
    output(ROOT/'design/tokens-dark.json',json.dumps(t,indent=2)+'\n')
    light=json.loads((ROOT/'design/tokens.json').read_text())
    assert all(t[k]==light[k] for k in ('radius','motion','motion_css','window','font'))
    values={**t['color'],**{k+'_radius':str(v)+'px' for k,v in t['radius'].items()},**{k+'_motion':v for k,v in t['motion_css'].items()},**{k+'_shadow':v for k,v in t['shadow'].items()},**{k:str(v)+'px' for k,v in t['window'].items()}}
    values.update(control_content_size='30px',header_padding=html_value(t,'.headerbar','padding'),header_padding_top='7px',header_padding_bottom='8px',entry_content_width=str(int(html_value(t,'.entry','min-width')[:-2])-22)+'px',dropdown_content_width=str(int(html_value(t,'.select','min-width')[:-2])-26)+'px',preference_content_height=str(int(html_value(t,'.pref-row','--single-target')[:-2])-17)+'px',banner_button_content_height=str(int(html_value(t,'.banner .btn','height')[:-2])-2)+'px',control_duration='128ms',surface_duration='256ms')
    def render(s):
        s=re.sub(r'\$\{([^|}]+)\|([^}]+)\}',lambda m:html_value(t,m[1],m[2]),s)
        return re.sub(r'\$\{(\w+)\}',lambda m:values[m[1]],s)
    values.update(editor_values('dark'))
    # Points preserve 14px/12px at 96 DPI and follow native accessibility text DPI.
    values.update(preference_title_font=f"{float(html_value(t,'.pref-title','font-size')[:-2])*.75:g}pt",preference_subtitle_font=f"{float(html_value(t,'.pref-desc','font-size')[:-2])*.75:g}pt")
    values['preference_inner_radius']=str(t['radius']['structure']-1)+'px'
    values['menu_border']='#3B3B40'
    values['window_edge_color']=html_value(t,'.window','border-color')
    colors='/* Generated from the effective dark reference cascade. */\n'+''.join('@define-color '+k+' '+v+';\n' for k,v in t['color'].items())
    # Primitive indigo identities remain invariant; component states are separate.
    aliases={'action_primary':'primary_default','action_primary_hover':'primary_hover','action_primary_pressed':'primary_pressed','focus_color':'focus','action_danger':'danger_default','action_danger_hover':'danger_hover','action_danger_pressed':'danger_pressed','danger':'danger_default','danger_pressed':'danger_pressed','success':'success'}
    colors+=''.join('@define-color '+name+' '+t['semantic_color'][key]+';\n' for name,key in aliases.items())
    for name in ('accent_fg_color','destructive_fg_color','theme_selected_fg_color'): colors+='@define-color '+name+' #FFFFFF;\n'
    for version in ('3','4'):
        values.update(sidebar_values(t,'dark',version));values.update(data_values(t));values.update(toolbar_values(t))
        directory=ROOT/f'theme/Majoris/gtk-{version}.0'
        output(directory/'colors-dark.css',colors)
        output(directory/'assets/spinner-dark.svg','<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><circle cx="10" cy="10" r="9" fill="none" stroke="'+html_value(t,'.spinner','border-color')+'" stroke-width="2"/><path d="M3.63604 3.63604 A9 9 0 0 1 16.36396 3.63604" fill="none" stroke="'+html_value(t,'.spinner','border-top-color')+'" stroke-width="2"/></svg>\n')
        shared=(ROOT/'design/templates/gtk-common.css.in').read_text()
        shared,desktop=shared.split('/* Desktop Icons NG:',1)
        desktop='/* Desktop Icons NG:'+desktop
        specific=(ROOT/f'design/templates/gtk{version}.css.in').read_text()
        if version=='4': shared=re.sub(r'(button(?:\.[\w-]+)?):focus\b',r'\1:focus-visible',shared)
        else:
            shared=shared.replace('${.tab.active|font-weight}','600').replace('${.nav.active|font-weight}','600').replace('transparent 10px, @primary_500 10px','transparent 10%, @primary_500 10%').replace('calc(100% - 10px)','90%')
        # Target only semantic action/focus declarations, never all palette uses.
        lines=[]
        for line in (shared+specific).splitlines(keepends=True):
            selector=line.split('{',1)[0]
            if 'button.suggested-action' in selector or selector.strip().startswith('banner button'):
                for step,state in [('600',''),('700','_hover'),('800','_pressed')]:
                    line=line.replace('@primary_'+step,'@action_primary'+state)
            if ':focus' in selector and 'border-color:' in line:
                line=line.replace('@primary_500','@focus_color')
            lines.append(line)
        css=render(''.join(lines)).replace('rgba(99,102,241,.24)','rgba(129,140,248,.34)').replace('alpha(@primary_500,.24)','alpha(@focus_color,.34)').replace('assets/spinner.svg','assets/spinner-dark.svg')
        extra=render((ROOT/'design/templates/gtk-dark.css.in').read_text())
        if version=='3': extra=extra.replace(':focus-visible',':focus')
        if version=='3':
            extra=re.sub(r'notebook > header tab:checked \{ background-image:.*?\}\n', '', extra)
            extra=extra.replace('popover.background { background: transparent; }','')
            extra+=render((ROOT/'design/templates/gtk3-dark.css.in').read_text())
        if version=='4': extra+=render((ROOT/'design/templates/gtk4-editor.css.in').read_text()+(ROOT/'design/templates/gtk4-location.css.in').read_text())
        sidebar=(ROOT/'design/templates/gtk-sidebar.css.in').read_text()
        if version=='3': sidebar=sidebar.replace(':focus-visible',':focus').replace('-gtk-icon-size: 16px;','')
        extra+=render(sidebar)+render((ROOT/f'design/templates/gtk{version}-data.css.in').read_text())+render(toolbar_template(version))
        base='@import url("resource:///org/gtk/libgtk/theme/Adwaita/gtk-contained.css");\n' if version=='3' else ''
        output(directory/'gtk-dark.css','/* Generated: shared geometry, effective dark cascade, native overrides. */\n'+base+'@import url("colors.css");\n@import url("colors-dark.css");\n'+css+extra+render(desktop))
    # Explicit Shell roles avoid substring replacements matching background-color.
    values.update(shell_panel_surface=t['color']['surface'],shell_popup_surface='rgba(40,40,44,.98)',shell_control_surface=t['color']['surface_secondary'],shell_search_surface=t['color']['surface_secondary'],shell_disabled_foreground=t['color']['text_tertiary'],shell_selected_foreground='#FFFFFF',shell_focus_color=t['semantic_color']['focus'],shell_tooltip_background=html_value(t,'.tooltip','background'),shell_tooltip_foreground=html_value(t,'.tooltip','color'),shell_tooltip_shadow=html_value(t,'.tooltip','box-shadow'))
    values['danger']=t['semantic_color']['danger_default']
    shell=render((ROOT/'design/templates/shell.css.in').read_text()).replace('rgba(99,102,241,.24)','rgba(129,140,248,.34)')
    output(ROOT/'theme/Majoris/gnome-shell/gnome-shell-dark.css','/* Generated dark Shell variant. */\n'+shell)
    alias=ROOT/'theme/Majoris-Dark/gnome-shell/gnome-shell.css'
    alias.parent.mkdir(parents=True,exist_ok=True)
    output(alias,'/* Generated dark Shell variant. */\n'+shell)
