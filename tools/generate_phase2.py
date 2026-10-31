"""Phase 2 typography derives physical points from canonical 96-DPI pixel roles."""
from design import html_value

def phase2_values(tokens):
    def points(selector):return f"{float(html_value(tokens,selector,'font-size').removesuffix('px'))*.75:g}pt"
    return dict(phase2_control_font=points('.phase2-day'),phase2_heading_font=points('.phase2-calendar-heading'),phase2_metadata_font=points('.phase2-weekday'))
