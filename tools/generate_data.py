"""Translate complete canonical allocations into GTK content minima."""
from design import html_value
def data_values(t):
 def n(selector,prop):return int(html_value(t,selector,prop).removesuffix('px'))
 def vertical(selector):return int(html_value(t,selector,'padding').split()[0].removesuffix('px'))*2
 normal='.data-list .data-item';compact='.data-list.compact .data-item';tile='.data-tile';small='.data-grid.compact .data-tile';header='.data-column .table-head div'
 def paint(role):
  value=html_value(t,'.data-views','--dv-'+role)
  if value.startswith('rgba('):
   parts=value[5:-1].split(',')
   return 'mix(@majoris_data_surface, rgb('+','.join(parts[:3])+'), '+parts[3]+')'
  return '@majoris_data_'+role.replace('-','_')
 return dict(data_selected_paint=paint('selected'),data_selected_hover_paint=paint('selected-hover'),data_selected_pressed_paint=paint('selected-pressed'),data_list_min=str(n(normal,'min-height')-vertical(normal))+'px',data_compact_min=str(n(compact,'min-height')-vertical(compact))+'px',data_column_min=str(n(normal,'min-height')-vertical(normal)-1)+'px',data_column_compact_min=str(n(compact,'min-height')-vertical(compact)-1)+'px',data_header_min=str(n(header,'min-height')-vertical(header)-1)+'px',data_tile_width=str(n(tile,'width')-vertical(tile))+'px',data_tile_height=str(n(tile,'min-height')-vertical(tile))+'px',data_tile_compact_width=str(n(small,'width')-vertical(small))+'px',data_tile_compact_height=str(n(small,'min-height')-vertical(small))+'px')
