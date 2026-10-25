"""Real tab trees: Pango ink, baselines, close allocations and native operations."""
import os,sys,ctypes,json,subprocess,atexit,time
from pathlib import Path
os.environ['GSK_RENDERER']='cairo'
import gi
version=sys.argv[1] if len(sys.argv)>1 else '4'
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk,GLib,Gio,Pango
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light');scale=os.environ.get('GDK_SCALE','1')
text_scale=float(os.environ.get('MAJORIS_TAB_TEXT_SCALE','1'))
out=root/'artifacts/tab-finalisation'/(variant+('-2x' if scale=='2' else '')+('-text-125' if text_scale>1 else ''));out.mkdir(parents=True,exist_ok=True)
if version=='4':
 gi.require_version('Adw','1')
 from gi.repository import Adw
 Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris')
 ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
 Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
else:
 Gtk.init([])
 from gi.repository import Gdk
 provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
Gtk.Settings.get_default().set_property('gtk-icon-theme-name','Majoris')
if version=='4':Gtk.IconTheme.get_for_display(__import__('gi').repository.Gdk.Display.get_default()).add_search_path(str(root/'icons'))
else:Gtk.IconTheme.get_default().append_search_path(str(root/'icons'))
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);atexit.register(wm.terminate)
for attempt in range(40):
 if 'window id' in subprocess.check_output(['xprop','-root','_NET_SUPPORTING_WM_CHECK'],text=True):break
 time.sleep(.05)
w=Adw.Window(title='Majoris native tabs GTK'+version) if version=='4' else Gtk.Window(title='Majoris native tabs GTK'+version);w.set_default_size(1100,360)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16)
if version=='4':w.set_content(box)
else:w.add(box)
def append(container,child):
 container.append(child) if version=='4' else container.pack_start(child,False,False,0)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(180,lambda:(loop.quit(),False)[1]);loop.run()
def nodes(widget):
 yield widget
 if version=='3':
  children=widget.get_children() if isinstance(widget,Gtk.Container) else []
  if isinstance(widget,Gtk.Notebook):children += [widget.get_tab_label(widget.get_nth_page(i)) for i in range(widget.get_n_pages())]
 else:
  children=[];child=widget.get_first_child()
  while child:children.append(child);child=child.get_next_sibling()
 for child in children:yield from nodes(child)
def capture(name):
 settle();path=out/(('gtk3-' if version=='3' else '')+name+'.xwd')
 wid=subprocess.check_output(['xdotool','search','--name','^Majoris native tabs GTK'+version+'$'],text=True).splitlines()[0]
 subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True)
 subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
labels=['Favorites','Files','Find','Format','Documents','Downloads','Preferences','New Folder','notes.md','main.vala','Project Requirements.md','Majoris-Theme-Implementation-Notes.txt','A Very Long Document Filename That Exceeds Normal Tab Width.txt','gyp;!? ascenders']
if version=='4':
 view=Adw.TabView(vexpand=True);bar=Adw.TabBar(view=view,autohide=False,expand_tabs=False);bar.add_css_class('majoris-document-tabs');append(box,bar)
 for title in labels:
  page=view.append(Gtk.Label(label='Native document content'));page.set_title(title);page.set_icon(Gio.ThemedIcon.new('text-x-generic-symbolic'))
 view.set_page_pinned(view.get_nth_page(1),True)
 view.get_nth_page(4).set_needs_attention(True)
 append(box,view)
notebook=Gtk.Notebook()
for title in labels[:4]:notebook.append_page(Gtk.Label(label='Navigation'),Gtk.Label(label=title))
append(box,notebook)
stack=Gtk.Stack()
for title in ('List','Grid','Columns'):stack.add_titled(Gtk.Label(label=title),title,title)
switcher=Gtk.StackSwitcher(stack=stack);append(box,switcher);append(box,stack)
w.present() if version=='4' else w.show_all();settle()
if version=='4':
 for attempt in range(15):
  if bar.get_allocated_height()>1:break
  settle()
results=[]
if version=='4' and text_scale>1:
 # Xvfb does not forward GNOME's text scaling to fixed-pixel CSS fonts.
 # Apply the equivalent native Pango size to exercise actual enlarged ink.
 for label in nodes(box):
  if isinstance(label,Gtk.Label) and label.get_text() in labels+['List','Grid','Columns']:
   attrs=Pango.AttrList();attrs.insert(Pango.attr_size_new_absolute(round(14*text_scale*Pango.SCALE)));label.set_attributes(attrs)
 settle()
if version=='4':
 if bar.get_allocated_height()!=40:
  for widget in nodes(bar):print(type(widget).__name__,widget.get_css_name(),widget.get_visible(),widget.get_mapped(),widget.get_allocated_height(),widget.measure(Gtk.Orientation.VERTICAL,-1),flush=True)
 assert bar.get_allocated_height()==40,('strip',bar.get_allocated_height(),w.get_allocated_height())
 # Visit all pages in a spacious window; collect actual title Pango and parent allocations.
 for index in range(view.get_n_pages()):
  view.set_selected_page(view.get_nth_page(index));settle()
  assert bar.get_allocated_height()==40
  for label in nodes(bar):
   if not isinstance(label,Gtk.Label) or label.get_text() not in labels or not label.get_mapped():continue
   tab=label.get_ancestor(Gtk.Widget) # Find the actual native tab node, not a guessed widget class.
   parent=label.get_parent()
   while parent is not None and parent.get_css_name()!='tab':parent=parent.get_parent()
   if parent is None:continue
   desc=label.get_layout().get_context().get_font_description();ink,logical=label.get_layout().get_pixel_extents();x,y=label.get_layout_offsets()
   if text_scale>1:assert logical.height>=22,('text enlargement inactive',label.get_text(),logical.height)
   selected=bool(parent.get_state_flags() & Gtk.StateFlags.SELECTED)
   assert desc.get_weight()==(Pango.Weight.SEMIBOLD if selected else Pango.Weight.MEDIUM),(label.get_text(),desc.to_string(),selected)
   assert desc.get_size()/Pango.SCALE>=14 if text_scale>1 else desc.get_size()/Pango.SCALE==14,desc.to_string()
   assert y+ink.y>=0 and y+ink.y+ink.height<=label.get_allocated_height(),(label.get_text(),'ink clipped',y,ink,label.get_allocated_height())
   measured_desc=desc.copy()
   if text_scale>1:measured_desc.set_absolute_size(14*text_scale*Pango.SCALE)
   metrics=label.get_pango_context().get_metrics(measured_desc,label.get_pango_context().get_language())
   ancestor=label.get_parent()
   while ancestor is not None:
    ok,bounds=label.compute_bounds(ancestor);assert ok
    glyph_top=bounds.get_y()+y+ink.y
    assert glyph_top>=0 and glyph_top+ink.height<=ancestor.get_allocated_height(),(label.get_text(),'ancestor clip',ancestor.get_css_name(),glyph_top,ink.height,ancestor.get_allocated_height())
    if ancestor==bar:break
    ancestor=ancestor.get_parent()
   results.append(dict(ascent=metrics.get_ascent()/Pango.SCALE,descent=metrics.get_descent()/Pango.SCALE,text=label.get_text(),selected=selected,font=desc.to_string(),allocation=[label.get_allocated_width(),label.get_allocated_height()],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.width,logical.height],layout_origin=[x,y],baseline=label.get_layout().get_baseline()/Pango.SCALE,tab_height=parent.get_allocated_height()))
  for button in nodes(bar):
   if isinstance(button,Gtk.Button) and button.get_ancestor(Gtk.Widget):
    parent=button.get_parent()
    while parent is not None and parent.get_css_name()!='tab':parent=parent.get_parent()
    if parent and button.get_mapped():
     assert [button.get_allocated_width(),button.get_allocated_height()]==[24,24],('close',button.get_allocated_width(),button.get_allocated_height())
     for image in nodes(button):
      if isinstance(image,Gtk.Image):assert [image.get_allocated_width(),image.get_allocated_height()]==[16,16],('glyph',image.get_allocated_width(),image.get_allocated_height())
 # Native page transfer makes the baseline review uncluttered; restore for overflow.
 holding=Adw.TabView()
 for i in reversed(range(view.get_n_pages())):
  candidate=view.get_nth_page(i)
  if candidate.get_title() not in ('Files','Favorites','Documents','notes.md','main.vala','Project Requirements.md'):view.transfer_page(candidate,holding,holding.get_n_pages())
 for title in labels:
  baseline_values=[item['baseline'] for item in results if item['text']==title]
  if baseline_values:assert max(baseline_values)-min(baseline_values)<.01,(title,'baseline moved',baseline_values)
 view.set_selected_page(next(view.get_nth_page(i) for i in range(view.get_n_pages()) if view.get_nth_page(i).get_title()=='Favorites'));settle();capture('document-tabs')
 tabs=[item for item in nodes(bar) if item.get_css_name()=='tab']
 for state,name in [(Gtk.StateFlags.PRELIGHT,'hover'),(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,'focus'),(Gtk.StateFlags.BACKDROP,'inactive')]:
  for tab in tabs:tab.set_state_flags(state,False)
  capture('document-tabs-'+name)
  for tab in tabs:tab.unset_state_flags(state)
 capture('favorites-glyphs')
 # A real second native window establishes actual inactive-window state.
 other=Gtk.Window(title='Tab backdrop probe');other.set_default_size(120,80);other.present();settle()
 other_id=subprocess.check_output(['xdotool','search','--name','^Tab backdrop probe$'],text=True).splitlines()[0]
 subprocess.run(['xdotool','windowmove',other_id,'1600','1200','windowactivate','--sync',other_id],check=True);settle()
 assert not w.is_active(),'Window did not enter native inactive state'
 native_backdrop=bool(w.get_state_flags() & Gtk.StateFlags.BACKDROP)
 if not native_backdrop:
  for tab in tabs:tab.set_state_flags(Gtk.StateFlags.BACKDROP,False)
  settle()
 (out/'backdrop-state.json').write_text(json.dumps({'window_inactive':not w.is_active(),'native_backdrop_received':native_backdrop,'held_backdrop_for_typography':not native_backdrop},indent=2)+'\n')
 for label in nodes(bar):
  if isinstance(label,Gtk.Label) and label.get_text() in labels:
   assert label.get_pango_context().get_font_description().get_weight()==Pango.Weight.MEDIUM,('inactive title must be Medium',label.get_text(),label.get_pango_context().get_font_description().to_string(),w.get_state_flags(),bar.get_state_flags(),label.get_state_flags())
 capture('document-tabs-inactive');other.destroy();w.present();
 if not native_backdrop:
  for tab in tabs:tab.unset_state_flags(Gtk.StateFlags.BACKDROP)
 settle()
 while holding.get_n_pages():holding.transfer_page(holding.get_nth_page(0),view,view.get_n_pages())
 # Native reorder, page transfer (detach primitive), close and overflow.
 extra=view.append(Gtk.Label(label='Detachable'));extra.set_title('Detachable')
 assert view.reorder_page(extra,2)
 destination=Adw.TabView();view.transfer_page(extra,destination,0);assert destination.get_n_pages()==1
 view.close_page(view.get_nth_page(view.get_n_pages()-1))
 w.set_default_size(480,360);settle();assert bar.get_is_overflowing();capture('document-tabs-overflow')
 assert results,'No native tab labels were measured'
 # Larger accessibility text must be measured naturally rather than clipped.
 for label in nodes(bar):
  if isinstance(label,Gtk.Label) and label.get_text() in labels:
   attrs=Pango.AttrList();attrs.insert(Pango.attr_size_new_absolute(40*Pango.SCALE));label.set_attributes(attrs)
 settle();assert bar.get_allocated_height()>40,bar.get_allocated_height();capture('document-tabs-large-text')
 for label in nodes(bar):
  if isinstance(label,Gtk.Label) and label.get_text() in labels:label.set_attributes(None)
 settle()
capture('navigation-tabs');capture('segmented-controls')
for label in nodes(notebook):
 if isinstance(label,Gtk.Label) and label.get_text() in labels[:4]:
  desc=label.get_layout().get_context().get_font_description();assert desc.get_weight() in (Pango.Weight.MEDIUM,Pango.Weight.SEMIBOLD),desc.to_string()
navigation=[]
for label in nodes(notebook):
 if not isinstance(label,Gtk.Label) or label.get_text() not in labels[:4]:continue
 ink,logical=label.get_layout().get_pixel_extents();x,y=label.get_layout_offsets()
 if version=='3':
  allocation=label.get_allocation();x-=allocation.x;y-=allocation.y
  position=label.translate_coordinates(notebook,0,0)
 else:
  ok,bounds=label.compute_bounds(notebook);assert ok;position=[bounds.get_x(),bounds.get_y()]
 assert y+ink.y>=0 and y+ink.y+ink.height<=label.get_allocated_height(),(version,label.get_text(),'notebook glyph clipped')
 navigation.append(dict(text=label.get_text(),font=label.get_layout().get_context().get_font_description().to_string(),baseline=position[1]+y+label.get_layout().get_baseline()/Pango.SCALE,allocation=[label.get_allocated_width(),label.get_allocated_height()],ink=[ink.x,ink.y,ink.width,ink.height]))
assert len(navigation)==4,navigation
assert max(item['baseline'] for item in navigation)-min(item['baseline'] for item in navigation)<=1.01,navigation
for child in nodes(switcher):
 if isinstance(child,Gtk.ToggleButton):assert child.get_allocated_height()==28,('segment',child.get_allocated_height())
(out/('gtk'+version+'-navigation.json')).write_text(json.dumps(navigation,indent=2)+'\n')
(out/('gtk'+version+'-measurements.json')).write_text(json.dumps(results,indent=2)+'\n')
w.destroy();print('Native tab typography, glyph bounds, geometry and operations passed',version,variant,scale)
