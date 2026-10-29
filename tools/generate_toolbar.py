"""Toolbar dimensions derive from the canonical border-box HTML geometry."""
from design import ROOT, html_value

def toolbar_values(tokens):
    number=lambda selector,prop:int(html_value(tokens,selector,prop).removesuffix('px'))
    control=number('.majoris-toolbar-control','min-height')
    strip=number('.majoris-toolbar','min-height')
    inset=int(html_value(tokens,'.majoris-toolbar','padding').split()[0].removesuffix('px'))
    switch=number('.majoris-toolbar-segmented','height')
    segment_padding=int(html_value(tokens,'.majoris-toolbar-segmented button','padding').split()[0].removesuffix('px'))
    icon=number('.majoris-toolbar-icon svg','width')
    segment=number('.majoris-toolbar-segmented button','min-height')
    compact=number('.majoris-toolbar-compact .majoris-toolbar-control','min-height')
    return dict(toolbar_compact_content=str(compact-2)+'px',toolbar_compact_icon_padding=str((compact-icon-2)//2)+'px',toolbar_button_surface=html_value(tokens,'.btn','background'),toolbar_content=str(strip-2*inset)+'px',toolbar_control_content=str(control-2)+'px',toolbar_icon_padding=str((control-icon-2)//2)+'px',toolbar_segment_content=str(segment-2*segment_padding)+'px',toolbar_switch_content=str(segment)+'px',toolbar_switch_padding=str((switch-segment-2)//2)+'px')

def toolbar_template(version):
    text=(ROOT/'design/templates/gtk-toolbar.css.in').read_text()
    if version=='3':
        # GTK3 cannot distinguish pointer/keyboard focus: retain native :focus,
        # and omit GTK4-only pointer resets rather than restyling unfocused controls.
        text='\n'.join(line for line in text.split('\n') if ':focus:not(:focus-visible)' not in line)
        text=text.replace(':focus-visible',':focus').replace('-gtk-icon-size: 16px;','')
        import re
        text=re.sub(r'border-spacing: [^;]+;', '', text)
        text=text.replace(' filter: none;', '').replace('-gtk-icon-filter: none;', '-gtk-icon-effect: none;')
    return text
