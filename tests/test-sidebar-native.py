"""Real GTK3/4 rows: allocations, font metrics, pixels, scale, RTL and accessibility."""
import gi,sys,os,json,subprocess
from pathlib import Path
from PIL import Image
root=Path(__file__).resolve().parents[1];version=sys.argv[1]
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk,Gdk,GLib,Pango
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init()
else:Gtk.init([])
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
Gtk.Settings.get_default().set_property('gtk-icon-theme-name','Adwaita')

def settle():
 loop=GLib.MainLoop();GLib.timeout_add(180,lambda:(loop.quit(),False)[1]);loop.run()
def append(box,widget):
 if version=='4':box.append(widget)
 else:box.pack_start(widget,widget.get_hexpand() if box.get_orientation()==Gtk.Orientation.HORIZONTAL else False,True,0)
def add_class(w,name):w.get_style_context().add_class(name)
def extent(w,ancestor):
 if version=='4':
  ok,r=w.compute_bounds(ancestor);assert ok
  return [round(r.get_x()),round(r.get_y()),round(r.get_width()),round(r.get_height())]
 x,y=w.translate_coordinates(ancestor,0,0);return [x,y,w.get_allocated_width(),w.get_allocated_height()]
def height(w):
 if version=='4':return w.get_height()
 margin=w.get_style_context().get_margin(w.get_state_flags())
 return w.get_allocated_height()-margin.top-margin.bottom
def color(context):
 c=context.get_color() if version=='4' else context.get_color(context.get_state())
 return tuple(round(v*255) for v in (c.red,c.green,c.blue))
report=[]
for variant in ('light','dark'):
 provider=Gtk.CssProvider();provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 if version=='4':
  Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
  Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1)
  window=Adw.Window()
 else:
  Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1)
  window=Gtk.Window()
 window.set_title('Majoris sidebar native probe');window.set_default_size(224,650)
 outer=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
 surface=Gtk.Box(orientation=Gtk.Orientation.VERTICAL);surface.set_halign(Gtk.Align.FILL);add_class(surface,'majoris-sidebar');append(outer,surface)
 heading=Gtk.Label(label='Favorites',xalign=0);add_class(heading,'majoris-sidebar-heading');append(surface,heading)
 listbox=Gtk.ListBox(selection_mode=Gtk.SelectionMode.SINGLE);append(surface,listbox)
 probes=[]
 for text in ('Favorites','Files','Folders','Documents','Downloads','Network','Settings','Preferences','A Very Long Shared Network Folder Name'):
  row=Gtk.ListBoxRow();box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=8)
  icon=Gtk.Image.new_from_icon_name('folder-symbolic') if version=='4' else Gtk.Image.new_from_icon_name('folder-symbolic',Gtk.IconSize.MENU)
  icon.set_pixel_size(16);icon.set_valign(Gtk.Align.CENTER);icon.set_halign(Gtk.Align.CENTER);append(box,icon)
  label=Gtk.Label(label=text,xalign=0,hexpand=True,ellipsize=Pango.EllipsizeMode.END,valign=Gtk.Align.CENTER);append(box,label)
  badge=Gtk.Label(label='12',valign=Gtk.Align.CENTER);add_class(badge,'majoris-sidebar-badge');append(box,badge)
  row.set_tooltip_text(text)
  if version=='4':row.set_child(box);listbox.append(row)
  else:row.add(box);listbox.add(row)
  probes.append((row,icon,label,badge))
 expander=Gtk.Expander();add_class(expander,'majoris-sidebar-group')
 title=Gtk.Label(label='Devices',xalign=0,margin_start=8);add_class(title,'majoris-sidebar-group-title');expander.set_label_widget(title)
 children=Gtk.ListBox();child=Gtk.ListBoxRow();add_class(child,'majoris-sidebar-child')
 child_label=Gtk.Label(label='Internal Drive',xalign=0)
 if version=='4':child.set_child(child_label);children.append(child);expander.set_child(children)
 else:child.add(child_label);children.add(child);expander.add(children)
 append(surface,expander);expander.set_expanded(True)
 focus=Gtk.Box();
 if version=='4':focus.set_focusable(True)
 else:focus.set_can_focus(True)
 append(outer,focus)
 if version=='4':window.set_content(outer);window.present()
 else:window.add(outer);window.show_all()
 listbox.select_row(probes[0][0]);focus.grab_focus();settle()
 padding=surface.get_style_context().get_padding() if version=='4' else surface.get_style_context().get_padding(Gtk.StateFlags.NORMAL)
 assert (padding.top,padding.bottom,padding.left,padding.right)==(16,16,8,8)
 border=surface.get_style_context().get_border() if version=='4' else surface.get_style_context().get_border(surface.get_state_flags())
 assert border.right==1 and border.left==0
 expected_baselines=[]
 for i,(row,icon,label,badge) in enumerate(probes):
  assert height(row)==32,(version,variant,height(row))
  assert [icon.get_allocated_width(),icon.get_allocated_height()]==[16,16]
  ri,rl,rb=extent(icon,window),extent(label,window),extent(badge,window)
  assert rl[0]-(ri[0]+ri[2])==8,(ri,rl)
  assert rb[0]-(rl[0]+rl[2])>=8
  font=label.get_pango_context().get_font_description()
  assert round(font.get_size()/Pango.SCALE*(1 if font.get_size_is_absolute() else 96/72),2)==14 and int(font.get_weight())==(600 if i==0 else 500),font.to_string()
  assert 'Plus Jakarta Sans' in font.get_family()
  badge_font=badge.get_pango_context().get_font_description()
  assert round(badge_font.get_size()/Pango.SCALE*(1 if badge_font.get_size_is_absolute() else 96/72),2)==12 and int(badge_font.get_weight())==600
  ink,logical=label.get_layout().get_pixel_extents()
  assert ink.y>=0 and ink.y+ink.height<=label.get_allocated_height(),(text,ink.y,ink.height,label.get_allocated_height())
  if i:assert extent(row,window)[1]-extent(probes[i-1][0],window)[1]==36
  before=extent(label,window)[1]-extent(row,window)[1]+label.get_layout().get_baseline()/Pango.SCALE
  listbox.select_row(row);settle()
  after=extent(label,window)[1]-extent(row,window)[1]+label.get_layout().get_baseline()/Pango.SCALE
  assert before==after,(before,after)
  listbox.select_row(probes[0][0]);settle()
 assert probes[-1][2].get_layout().is_ellipsized()
 hfont=heading.get_pango_context().get_font_description();assert round(hfont.get_size()/Pango.SCALE*(1 if hfont.get_size_is_absolute() else 96/72),2)==12 and int(hfont.get_weight())==600
 assert height(title)>=32
 assert extent(title,window)[0]==extent(probes[0][2],window)[0],(version,extent(title,window),extent(probes[0][2],window))
 selected=probes[0][0];old=extent(selected,window)
 for state in (Gtk.StateFlags.NORMAL,Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,Gtk.StateFlags.SELECTED,Gtk.StateFlags.SELECTED|Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.SELECTED|Gtk.StateFlags.ACTIVE,Gtk.StateFlags.FOCUSED,Gtk.StateFlags.INSENSITIVE,Gtk.StateFlags.SELECTED|Gtk.StateFlags.BACKDROP):
  selected.set_state_flags(state,True);settle();assert extent(selected,window)==old
  if state==Gtk.StateFlags.SELECTED:
   assert color(selected.get_style_context())==((199,210,254) if variant=='dark' else (67,56,202))
  if state==Gtk.StateFlags.FOCUSED:assert not selected.get_state_flags()&Gtk.StateFlags.SELECTED
 focus.grab_focus();selected.set_state_flags(Gtk.StateFlags.SELECTED,True);settle()
 # Sample genuine native pixels to prove 2px width and fixed 8px end insets.
 out=root/'artifacts/sidebar-finalisation/geometry';out.mkdir(parents=True,exist_ok=True)
 for direction in (Gtk.TextDirection.LTR,Gtk.TextDirection.RTL):
  surface.set_direction(direction)
  for row,icon,label,badge in probes:
   for widget in (row,row.get_child(),icon,label,badge):widget.set_direction(direction)
   label.set_xalign(1 if direction==Gtk.TextDirection.RTL else 0)
  settle()
  if direction==Gtk.TextDirection.RTL:
   icon_bounds,label_bounds=extent(probes[0][1],window),extent(probes[0][2],window)
   assert icon_bounds[0]-(label_bounds[0]+label_bounds[2])==8,(icon_bounds,label_bounds)
  wid=subprocess.check_output(['xdotool','search','--name','^Majoris sidebar native probe$'],text=True).splitlines()[-1]
  scale=int(os.environ.get('GDK_SCALE','1'))
  file=out/f'gtk{version}-{variant}-{direction.value_nick}-{scale}x.xwd'
  subprocess.run(['xwd','-silent','-id',wid,'-out',str(file)],check=True)
  subprocess.run(['magick',str(file),str(file.with_suffix('.png'))],check=True)
  image=Image.open(file.with_suffix('.png')).convert('RGB')
  r=extent(selected,window);accent=(129,140,248) if variant=='dark' else (99,102,241)
  # Locate the rendered stripe independently of CSD shadow offsets.
  points=[(x,y) for y in range(image.height) for x in range(image.width) if image.getpixel((x,y))==accent]
  assert points,(version,variant,direction,'indicator missing')
  xs=[p[0] for p in points];ys=[p[1] for p in points]
  assert max(xs)-min(xs)+1==2*scale and max(ys)-min(ys)+1==16*scale,(version,variant,direction,(min(xs),max(xs),min(ys),max(ys)))
  if direction==Gtk.TextDirection.LTR:assert min(xs)<image.width/2
  else:assert min(xs)>r[2]/2*scale
 surface.set_direction(Gtk.TextDirection.LTR)
 for row,icon,label,badge in probes:
  for widget in (row,row.get_child(),icon,label,badge):widget.set_direction(Gtk.TextDirection.LTR)
  label.set_xalign(0)
 # Native accessibility font scaling must grow content instead of clipping it.
 settings=Gtk.Settings.get_default();original_dpi=settings.get_property('gtk-xft-dpi')
 settings.set_property('gtk-xft-dpi',192*1024)
 # Absolute CSS pixels do not follow legacy Xft DPI. Request actual enlarged
 # text through the native Pango font setting, without an appearance stylesheet.
 attributes=Pango.AttrList();attributes.insert(Pango.attr_scale_new(2.0))
 for _,_,label,_ in probes:label.set_attributes(attributes)
 settle()
 assert height(selected)>32,(version,'font scale did not enlarge row',height(selected))
 ink,_=probes[0][2].get_layout().get_pixel_extents();assert ink.y+ink.height<=probes[0][2].get_allocated_height()
 large=height(selected)
 # The native indicator keeps fixed 8px caps even when the row is larger.
 file=out/f'gtk{version}-{variant}-large-{scale}x.xwd'
 subprocess.run(['xwd','-silent','-id',wid,'-out',str(file)],check=True)
 subprocess.run(['magick',str(file),str(file.with_suffix('.png'))],check=True)
 image=Image.open(file.with_suffix('.png')).convert('RGB')
 points=[(x,y) for y in range(image.height) for x in range(image.width) if image.getpixel((x,y))==accent]
 assert points
 xs=[p[0] for p in points];ys=[p[1] for p in points]
 assert max(xs)-min(xs)+1==2*scale and max(ys)-min(ys)+1==(large-16)*scale,(version,variant,large,min(ys),max(ys))
 settings.set_property('gtk-xft-dpi',original_dpi)
 for _,_,label,_ in probes:label.set_attributes(None)
 settle()
 expander.set_expanded(False);settle();assert listbox.get_selected_row()==selected
 expander.set_expanded(True);settle();assert listbox.get_selected_row()==selected
 report.append({'variant':variant,'scale':int(os.environ.get('GDK_SCALE','1')),'row_height':32,'pitch':36,'icon':[16,16],'gap':8,'font':14,'normal_weight':500,'selected_weight':600,'heading':[12,600],'large_row_height':large,'indicator':[2,8,8],'divider':1,'rtl':True})
 window.destroy();settle()
 # GtkStackSidebar owns a different native tree: wrapper padding must stay zero.
 stack=Gtk.Stack();stack_sidebar=Gtk.StackSidebar();stack_sidebar.set_stack(stack);add_class(stack_sidebar,'navigation-sidebar')
 for name in ('Files','Network'):
  stack.add_titled(Gtk.Label(label=name),name,name)
 check=Adw.Window() if version=='4' else Gtk.Window();check.set_default_size(400,220)
 composition=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL);append(composition,stack_sidebar);append(composition,stack)
 if version=='4':check.set_content(composition);check.present()
 else:check.add(composition);check.show_all()
 settle()
 def walk(widget):
  yield widget
  if version=='4':
   c=widget.get_first_child()
   while c:
    yield from walk(c);c=c.get_next_sibling()
  elif isinstance(widget,Gtk.Container):
   for c in widget.get_children():yield from walk(c)
 native_rows=[w for w in walk(stack_sidebar) if isinstance(w,Gtk.ListBoxRow)]
 assert len(native_rows)==2 and all(height(row)==32 for row in native_rows),[(type(w).__name__,height(w)) for w in native_rows]
 native_list=next(w for w in walk(stack_sidebar) if isinstance(w,Gtk.ListBox))
 def padding_of(widget):
  context=widget.get_style_context();return context.get_padding() if version=='4' else context.get_padding(widget.get_state_flags())
 wrapper_padding,inner_padding=padding_of(stack_sidebar),padding_of(native_list)
 assert wrapper_padding.top==wrapper_padding.left==0
 assert (inner_padding.top,inner_padding.bottom,inner_padding.left,inner_padding.right)==(16,16,8,8)
 report[-1]['native_stack_sidebar']=True
 check.destroy();settle()
 if version=='4':Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),provider)
 else:Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),provider)
(root/f'artifacts/sidebar-finalisation/geometry/gtk{version}-{os.environ.get("GDK_SCALE","1")}x.json').write_text(json.dumps(report,indent=2)+'\n')
print('GTK'+version+' native sidebar allocations, real fonts/ink, states, indicator pixels, RTL and accessibility passed')
