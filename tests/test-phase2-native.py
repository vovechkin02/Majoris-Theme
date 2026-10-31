"""Real Phase 2 native allocations, interactions, text pixels and renderer diagnostics."""
import os,sys,json,ctypes,subprocess,time,re
from pathlib import Path
os.environ.setdefault('GDK_BACKEND','x11')
import gi
version=sys.argv[1] if len(sys.argv)>1 else '4';gi.require_version('Gtk',version+'.0');gi.require_version('GdkX11',version+'.0')
from gi.repository import Gtk,Gdk,GdkX11,GLib,Pango
root=Path(__file__).resolve().parents[1];variant=os.environ.get('MAJORIS_VARIANT','light');scale=os.environ.get('GDK_SCALE','1');renderer=os.environ.get('GSK_RENDERER','default');large=bool(os.environ.get('MAJORIS_LARGE_FONT'));baseline=bool(os.environ.get('MAJORIS_PHASE2_BASELINE'))
out=root/'artifacts/phase2-controls'/('gtk'+version)/variant/(renderer+'-'+scale+'x'+('-large' if large else ''));out.mkdir(parents=True,exist_ok=True)
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris');ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach();Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
else:
 Gtk.init([]);provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')));Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
settings=Gtk.Settings.get_default();settings.set_property('gtk-enable-animations',False)
if large:settings.set_property('gtk-xft-dpi',144*1024)
w=Gtk.Window(title='Majoris Phase2 validation');w.set_default_size(720,450)
body=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8);body.set_margin_start(16);body.set_margin_end(16);body.set_margin_top(16);body.set_margin_bottom(16)
w.set_child(body) if version=='4' else w.add(body)
def children(x):
 if version=='3':return x.get_children() if isinstance(x,Gtk.Container) else []
 items=[];c=x.get_first_child()
 while c:items.append(c);c=c.get_next_sibling()
 return items
def nodes(x):
 yield x
 for c in children(x):yield from nodes(c)
def append(x,c):x.append(c) if version=='4' else x.pack_start(c,False,False,0)
def style(x,name):x.add_css_class(name) if version=='4' else x.get_style_context().add_class(name)
def settle(ms=180):
 loop=GLib.MainLoop();GLib.timeout_add(ms,lambda:(loop.quit(),False)[1]);loop.run()
def key(*keys):subprocess.run(['xdotool','key','--clearmodifiers',*keys],check=True);settle()
def show(widget):
 for c in children(body):body.remove(c)
 append(body,widget);w.present() if version=='4' else w.show_all();settle()
 wid=str(w.get_surface().get_xid() if version=='4' else w.get_window().get_xid());subprocess.run(['xdotool','windowfocus',wid],check=True);return wid
def capture(name):
 settle()
 p=out/(name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(p)],check=True);subprocess.run(['magick',str(p),str(p.with_suffix('.png'))],check=True);p.unlink()
def alloc(x):return [x.get_allocated_width(),x.get_allocated_height()]
def padding(x):
 p=x.get_style_context().get_padding() if version=='4' else x.get_style_context().get_padding(Gtk.StateFlags.NORMAL);return [p.top,p.right,p.bottom,p.left]
def borders(x):
 b=x.get_style_context().get_border() if version=='4' else x.get_style_context().get_border(Gtk.StateFlags.NORMAL);return [b.top,b.right,b.bottom,b.left]
def measure(x):
 a=x.measure(Gtk.Orientation.HORIZONTAL,-1) if version=='4' else x.get_preferred_width();b=x.measure(Gtk.Orientation.VERTICAL,-1) if version=='4' else x.get_preferred_height()
 return dict(allocation=alloc(x),padding=padding(x),border=borders(x),horizontal=list(a),vertical=list(b))
lib=ctypes.CDLL('libgtk-4.so.1') if version=='4' else None
if lib:
 lib.gtk_snapshot_to_node.argtypes=[ctypes.c_void_p];lib.gtk_snapshot_to_node.restype=ctypes.c_void_p
 lib.gsk_renderer_render_texture.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p];lib.gsk_renderer_render_texture.restype=ctypes.c_void_p
 lib.gdk_texture_save_to_png.argtypes=[ctypes.c_void_p,ctypes.c_char_p];lib.gdk_texture_save_to_png.restype=ctypes.c_int
 lib.gsk_render_node_write_to_file.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p];lib.gsk_render_node_write_to_file.restype=ctypes.c_int
 lib.gsk_render_node_unref.argtypes=[ctypes.c_void_p]
 gobject=ctypes.CDLL('libgobject-2.0.so.0');gobject.g_object_unref.argtypes=[ctypes.c_void_p]
def paint(x,name):
 snap=Gtk.Snapshot();Gtk.WidgetPaintable.new(x).snapshot(snap,*alloc(x));node=lib.gtk_snapshot_to_node(hash(snap));assert node
 lib.gsk_render_node_write_to_file(node,str(out/(name+'.node')).encode(),None)
 viewport=(ctypes.c_float*4)(0,0,*alloc(x));texture=lib.gsk_renderer_render_texture(hash(w.get_renderer()),node,ctypes.byref(viewport));assert texture
 path=out/(name+'.png');assert lib.gdk_texture_save_to_png(texture,str(path).encode());gobject.g_object_unref(texture);lib.gsk_render_node_unref(node);return path
metrics=[];geometry={};interactions={};pixel_records=[];focus_geometry={}
def text_metrics(widget,family):
 for label in nodes(widget):
  if not isinstance(label,Gtk.Label) or not label.get_mapped() or not label.get_text():continue
  layout=label.get_layout();ink,logical=layout.get_pixel_extents();x,y=label.get_layout_offsets()
  if version=='3':a=label.get_allocation();x-=a.x;y-=a.y
  desc=layout.get_context().get_font_description();resolved=layout.get_context().load_font(desc).describe().to_string()
  record=dict(family=family,text=label.get_text(),allocation=alloc(label),ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.x,logical.y,logical.width,logical.height],origin=[x,y],baseline=layout.get_baseline()/Pango.SCALE,font=desc.to_string(),resolved=resolved)
  assert y+ink.y>=-1 and y+ink.y+ink.height<=alloc(label)[1]+1,record
  metrics.append(record)
  if version=='4':
   from PIL import Image
   path=paint(label,'glyph-'+str(len(metrics)));record['rendered_fonts']=re.findall(r'font: "([^"]+)"',path.with_suffix('.node').read_text());im=Image.open(path).convert('RGBA');color=label.get_style_context().get_color();target=[round(c*255) for c in (color.red,color.green,color.blue)]
   pixels=im.load();points=[(i,j) for j in range(im.height) for i in range(im.width) if pixels[i,j][3]>80 and sum(abs(pixels[i,j][k]-target[k]) for k in range(3))<90]
   assert points,('Missing rendered glyphs',record)
   bbox=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points)+1,max(p[1] for p in points)+1]
   # Background-filled calendar labels also contain text-coloured decorations;
   # plain labels provide the independent upper/lower glyph-pixel check.
   if label.get_parent().get_css_name()!='grid' and not label.get_style_context().has_class('year'):
    assert bbox[1]<=y+ink.y+2 and bbox[3]>=y+ink.y+ink.height-2,('Rendered glyph bounds',bbox,record)
   pixel_records.append(dict(family=family,text=record['text'],bbox=bbox,png=path.name))
def states(widget,name):
 before=alloc(widget);records=[]
 for flag,state in [(Gtk.StateFlags.PRELIGHT,'hover'),(Gtk.StateFlags.ACTIVE,'pressed'),(Gtk.StateFlags.FOCUSED|(Gtk.StateFlags.FOCUS_VISIBLE if version=='4' else Gtk.StateFlags.NORMAL),'focus'),(Gtk.StateFlags.BACKDROP,'backdrop')]:
  widget.set_state_flags(flag,False);settle();assert alloc(widget)==before,(name,state,before,alloc(widget));capture(name+'-'+state);
  if version=='4' and state=='focus':
   native=paint(widget,name+'-focus-native').with_suffix('.node').read_text();focus_geometry[name]={'border_widths':re.findall(r'widths: ([^;]+);',native),'inset_shadow_spreads':re.findall(r'spread: ([^;]+);',native),'allocation':alloc(widget)}
  records.append(state);widget.unset_state_flags(flag)
 widget.set_sensitive(False);settle();assert alloc(widget)==before;capture(name+'-disabled');widget.set_sensitive(True);return records
# Calendar uses real GTK selected/marked/today states; fixed reference month.
calendar=Gtk.Calendar();calendar.set_halign(Gtk.Align.START);calendar.set_show_week_numbers(True) if version=='4' else calendar.set_display_options(Gtk.CalendarDisplayOptions.SHOW_HEADING|Gtk.CalendarDisplayOptions.SHOW_DAY_NAMES|Gtk.CalendarDisplayOptions.SHOW_WEEK_NUMBERS)
if version=='4':calendar.select_day(GLib.DateTime.new_local(2026,10,15,12,0,0))
else:calendar.select_month(9,2026);calendar.select_day(15)
calendar.mark_day(12);wid=show(calendar);geometry['calendar']=measure(calendar);capture('calendar');text_metrics(calendar,'calendar')
if version=='4':
 days=[x for x in nodes(calendar) if isinstance(x,Gtk.Label) and x.has_css_class('day-number')];assert all(alloc(x)[0]>=32 and alloc(x)[1]>=32 for x in days)
 selected=next(x for x in days if x.get_state_flags()&Gtk.StateFlags.SELECTED);assert selected.get_text()=='15'
 marked=next(x for x in days if x.get_text()=='12' and not x.has_css_class('other-month'));assert marked.get_state_flags()&Gtk.StateFlags.CHECKED
 buttons=[x for x in nodes(calendar) if isinstance(x,Gtk.Button)];assert all(alloc(x)==[32,32] for x in buttons),[alloc(x) for x in buttons]
 states(buttons[0],'calendar-navigation');states(selected,'calendar-day');buttons[1].emit('clicked');settle();assert calendar.get_date().get_month()!=10
 year=calendar.get_date().get_year();buttons[3].emit('clicked');settle();assert calendar.get_date().get_year()!=year
 calendar.select_day(GLib.DateTime.new_now_local());settle();today=[x for x in nodes(calendar) if isinstance(x,Gtk.Label) and x.has_css_class('today')];assert len(today)==1 and today[0].get_state_flags()&Gtk.StateFlags.SELECTED;capture('calendar-today-selected')
 now=calendar.get_date();other=1 if now.get_day_of_month()!=1 else 2;calendar.select_day(GLib.DateTime.new_local(now.get_year(),now.get_month(),other,12,0,0));settle();assert not today[0].get_state_flags()&Gtk.StateFlags.SELECTED;capture('calendar-today-unselected')
 calendar.grab_focus();key('Right','space');assert calendar.get_date().get_day_of_month()!=other
 calendar.set_direction(Gtk.TextDirection.RTL);capture('calendar-rtl');calendar.set_direction(Gtk.TextDirection.LTR)
 geometry['calendar']['cells']=[measure(x) for x in days[:7]];geometry['calendar']['header']=measure(calendar.get_first_child())
interactions['calendar']=True;states(calendar,'calendar')
# Link activation is intercepted, so no URI is launched.
links=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8);normal=Gtk.Button(label='Ordinary button');normal.set_halign(Gtk.Align.START);append(links,normal)
link=Gtk.LinkButton(uri='https://example.invalid/phase2',label='Favorites Files Format gjpqy');link.set_halign(Gtk.Align.START);append(links,link);activated=[]
link.connect('activate-link',lambda *_:(activated.append(True),True)[1]);wid=show(links);geometry['linkbutton']=measure(link);assert borders(link)==[0]*4 and padding(link)==[0]*4;assert alloc(link)[1]<alloc(normal)[1];link.set_visited(True);assert link.get_visited();capture('links-visited');link.set_visited(False);link.grab_focus();key('Return');assert activated;interactions['link']=True;capture('links');text_metrics(links,'linkbutton');states(link,'link')
# Native EditableLabel: no entry replacement or custom keyboard handler.
if version=='4':
 editable=Gtk.EditableLabel(text='Favorites Format gjpqy.txt');style(editable,'majoris-editable-discoverable');editable.set_halign(Gtk.Align.START);wid=show(editable)
 stack=next(x for x in children(editable) if x.get_css_name()=='stack');label=next(x for x in children(stack) if isinstance(x,Gtk.Label));text=next(x for x in children(stack) if isinstance(x,Gtk.Text));
 if large:
  attributes=Pango.AttrList();attributes.insert(Pango.attr_scale_new(1.5));label.set_attributes(attributes);text.set_attributes(attributes);settle()
 before=measure(editable);base_before=label.get_layout().get_baseline()/Pango.SCALE+label.get_layout_offsets()[1]
 geometry['editablelabel']={'display':before,'label':measure(label),'display_baseline':base_before};capture('editable-label');text_metrics(editable,'editablelabel');paint(editable,'editable-display-node');states(editable,'editable-label')
 editable.grab_focus();key('Return');assert editable.get_editing();settle();geometry['editablelabel']['editing']=measure(editable);geometry['editablelabel']['text']=measure(text);paint(editable,'editable-editing-node');
 import re
 display_offsets=re.findall(r'offset: ([^;]+);',(out/'editable-display-node.node').read_text());editing_offsets=re.findall(r'offset: ([^;]+);',(out/'editable-editing-node.node').read_text());assert display_offsets[0] in editing_offsets,(display_offsets,editing_offsets)
 geometry['editablelabel']['render_baselines']={'display':display_offsets,'editing':editing_offsets};geometry['editablelabel']['cursor']=[str(r) for r in text.compute_cursor_extents(0)];assert alloc(editable)==before['allocation'],geometry['editablelabel'];assert padding(text)==[0]*4 and borders(text)==[0]*4
 key('ctrl+a');key('x');key('Escape');assert not editable.get_editing() and editable.get_text()=='Favorites Format gjpqy.txt'
 editable.start_editing();editable.set_text('Committed 日本語 مرحبا.txt');key('Return');assert not editable.get_editing() and editable.get_text().startswith('Committed');editable.start_editing();text.select_region(0,-1);selection=text.get_selection_bounds();assert selection[-1]>selection[-2],selection;capture('editable-label-editing');editable.stop_editing(True)
 for sample in ['A very long filename with spaces and punctuation — é 日本語.txt','RTL مرحبا שלום','First line\nSecond line gjpqy']:
  editable.set_text(sample);editable.start_editing();settle();editable.stop_editing(True)
 editable.set_direction(Gtk.TextDirection.RTL);settle();capture('editable-label-rtl')
 editable.set_direction(Gtk.TextDirection.LTR);editable.set_text('Compact filename gjpqy.txt');body.remove(editable)
 tile=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=4);append(tile,Gtk.Image.new_from_icon_name('text-x-generic-symbolic'));append(tile,editable);wid=show(tile);tile_before=alloc(tile);editable.start_editing();settle();assert alloc(tile)==tile_before;editable.stop_editing(True)
 tile.remove(editable);row=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=8);append(row,Gtk.Label(label='List row:'));append(row,editable);wid=show(row);row_before=alloc(row);editable.start_editing();settle();assert alloc(row)==row_before;editable.stop_editing(True)
 geometry['editablelabel']['tile']=tile_before;geometry['editablelabel']['row']=row_before;interactions['editablelabel']=True
# Native splitter gutter and keyboard/real pointer resizing.
paned=Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL);paned.set_size_request(500,150)
start=Gtk.Entry(text='Start pane');end=Gtk.Label(label='End pane')
if version=='4':paned.set_start_child(start);paned.set_end_child(end)
else:paned.pack1(start,True,True);paned.pack2(end,True,True)
paned.set_position(220);wid=show(paned);start.grab_focus();settle();geometry['paned']=measure(paned);capture('paned')
if version=='4':
 sep=next(x for x in children(paned) if x.get_css_name()=='separator');assert alloc(sep)[0]==8,alloc(sep);geometry['paned']['gutter']=measure(sep);divider_png=paint(sep,'paned-divider')
 from PIL import Image
 divider=Image.open(divider_png).convert('RGBA');coverage=sum(divider.getpixel((i,divider.height//2))[3]/255 for i in range(divider.width));assert .9<=coverage<=1.1,coverage
 geometry['paned']['visible_line_pixel_coverage']=coverage;states(sep,'paned-separator')
 ok,point=sep.translate_coordinates(w,4,40) if False else (False,None)
 ok,r=sep.compute_bounds(w);assert ok;x=int((r.get_x()+4)*int(scale));y=int((r.get_y()+40)*int(scale));position=paned.get_position();subprocess.run(['xdotool','mousemove','--window',wid,str(x),str(y),'mousedown','1','mousemove','--window',wid,str(x+50*int(scale)),str(y),'mouseup','1'],check=True);settle();assert paned.get_position()!=position,('Pointer resize',position,paned.get_position())
 start.grab_focus();key('F8');focus_node=paint(sep,'paned-keyboard-focus-native').with_suffix('.node').read_text();focus_geometry['paned-keyboard']={'border_widths':re.findall(r'widths: ([^;]+);',focus_node),'gutter':alloc(sep)};assert 'widths: 2;' in focus_node;position=paned.get_position();key('Right');assert paned.get_position()!=position,('Keyboard resize',position,paned.get_position())
 paned.set_orientation(Gtk.Orientation.VERTICAL);settle();assert alloc(sep)[1]==8;paned.set_wide_handle(True);settle();assert alloc(sep)[1]==16;paned.set_direction(Gtk.TextDirection.RTL);capture('paned-vertical-wide-rtl')
interactions['paned']=True
# Neutral container remains neutral; opt-in tiles use native selection modes.
flow=Gtk.FlowBox();flow.set_selection_mode(Gtk.SelectionMode.NONE);flow.set_min_children_per_line(1);flow.set_max_children_per_line(5)
for caption in ['Favorites','Files','Format gjpqy','日本語','مرحبا']:
 label=Gtk.Label(label=caption)
 if large:
  attributes=Pango.AttrList();attributes.insert(Pango.attr_scale_new(1.5));label.set_attributes(attributes)
 flow.insert(label,-1)
wid=show(flow);geometry['flowbox']={'neutral':measure(flow)};capture('flowbox-neutral');assert not flow.get_selected_children();style(flow,'majoris-flow-tiles');flow.set_selection_mode(Gtk.SelectionMode.MULTIPLE);flow.select_child(flow.get_child_at_index(0));flow.select_child(flow.get_child_at_index(2));assert len(flow.get_selected_children())==2
settle()
geometry['flowbox']['tiles']=measure(flow);capture('flowbox');text_metrics(flow,'flowbox');states(flow.get_child_at_index(0),'flowbox')
for mode in [Gtk.SelectionMode.SINGLE,Gtk.SelectionMode.BROWSE,Gtk.SelectionMode.MULTIPLE]:flow.set_selection_mode(mode);flow.select_child(flow.get_child_at_index(1));assert flow.get_selected_children()
flow.unselect_all();flow.get_child_at_index(0).grab_focus()
if version=='4':
 key('space');key('shift+Right');assert len(flow.get_selected_children())>=2,('Native range selection',len(flow.get_selected_children()))
else:
 flow.select_child(flow.get_child_at_index(0));flow.select_child(flow.get_child_at_index(2));assert len(flow.get_selected_children())==2
 key('Right');key('space');assert flow.get_selected_children()
if version=='4':
 flow.set_max_children_per_line(3);flow.set_row_spacing(8);flow.set_column_spacing(8);settle()
 first=flow.get_child_at_index(0);last=flow.get_child_at_index(2);ok,a=first.compute_bounds(w);ok,b=last.compute_bounds(w)
 x0=int((a.get_x()+a.get_width()/2)*int(scale));y0=int((a.get_y()+a.get_height()/2)*int(scale));x1=int((b.get_x()+b.get_width()/2)*int(scale));y1=int((b.get_y()+b.get_height()/2)*int(scale))
 subprocess.run(['xdotool','mousemove','--window',wid,str(x0),str(y0)],check=True);settle(60);subprocess.run(['xdotool','mousedown','1'],check=True);settle(60);subprocess.run(['xdotool','mousemove','--window',wid,str(x1),str(y1)],check=True);settle();capture('flowbox-rubberband');paint(flow,'flowbox-rubberband-native');rubberband_nodes=[x.get_css_name() for x in nodes(flow) if x.get_css_name()=='rubberband'];subprocess.run(['xdotool','mouseup','1'],check=True);settle();assert len(flow.get_selected_children())>=2,('Native rubberband',len(flow.get_selected_children()))
 geometry['flowbox']['rubberband']={'selected':len(flow.get_selected_children()),'exposed_nodes':rubberband_nodes}
flow.set_max_children_per_line(2);w.set_default_size(360,450) if version=='4' else w.resize(360,450);settle();capture('flowbox-wrapped');interactions['flowbox']=True
# Header allocation stays independent of natural expanded content.
expander=Gtk.Expander(label='Favorites Files Format gjpqy');expander.set_child(Gtk.Entry()) if version=='4' else expander.add(Gtk.Entry());wid=show(expander);geometry['expander']={'collapsed':measure(expander)};text_metrics(expander,'expander');expander.grab_focus();key('space');assert expander.get_expanded();geometry['expander']['expanded']=measure(expander);assert alloc(expander)[1]>geometry['expander']['collapsed']['allocation'][1];capture('expander');states(expander,'expander');interactions['expander']=True
if version=='4':
 title=next(x for x in nodes(expander) if x.get_css_name()=='title');geometry['expander']['header']=measure(title);assert alloc(title)[1]>=32;states(title,'expander-header')
# Native SearchBar focus capture and Escape dismissal.
bar=Gtk.SearchBar();entry=Gtk.SearchEntry();bar.set_child(entry) if version=='4' else bar.add(entry);bar.connect_entry(entry);bar.set_show_close_button(True)
if version=='4':bar.set_key_capture_widget(w)
wid=show(bar);geometry['searchbar']={'hidden':measure(bar)};assert alloc(bar)[1]<=(0 if version=='4' else 1),alloc(bar);bar.set_search_mode(True);settle();geometry['searchbar']['revealed']=measure(bar);assert alloc(entry)[1]==32 if not large else alloc(entry)[1]>=32
entry.set_text('Favorites Files Format gjpqy');settle();
if version=='4':
 paint(entry,'search-entry-native');search_text=next(x for x in nodes(entry) if isinstance(x,Gtk.Text));geometry['searchbar']['text']=measure(search_text)
capture('searchbar');text_metrics(bar,'searchbar');entry.grab_focus();key('Escape');assert not bar.get_search_mode();settle();assert alloc(bar)[1]<=(0 if version=='4' else 1)
if version=='4':key('f');assert bar.get_search_mode();close=next(x for x in nodes(bar) if isinstance(x,Gtk.Button) and x.has_css_class('close'));assert alloc(close)==[32,32];states(close,'searchbar-close');bar.set_search_mode(True);close.emit('clicked');assert not bar.get_search_mode()
interactions['searchbar']=True
for name,record in geometry.items():(out/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
(out/'focus-indicators.json').write_text(json.dumps(focus_geometry,indent=2)+'\n')
(out/'text-metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(out/'glyph-pixels.json').write_text(json.dumps(pixel_records,indent=2)+'\n');(out/'interactions.json').write_text(json.dumps(interactions,indent=2)+'\n');(out/'renderer.json').write_text(json.dumps(dict(requested=renderer,actual=w.get_renderer().__class__.__name__ if version=='4' else 'GTK3 native',scale=scale,large_fonts=large),indent=2)+'\n')
w.destroy();print('Phase2 native passed',version,variant,scale,renderer,large)
