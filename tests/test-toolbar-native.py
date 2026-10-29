"""Real GTK3/4 toolbar layout, Pango metrics, state stability and isolation."""
import os,sys,ctypes,json,subprocess,atexit,time
from pathlib import Path
os.environ['GSK_RENDERER']='cairo'
import gi
version=sys.argv[1] if len(sys.argv)>1 else '4'
gi.require_version('Gtk',version+'.0')
gi.require_version('GdkX11',version+'.0')
from gi.repository import Gtk,Gdk,GdkX11,GLib,Gio,Pango
root=Path(__file__).resolve().parents[1];variant=os.environ.get('MAJORIS_VARIANT','light');scale=os.environ.get('GDK_SCALE','1')
out=root/os.environ.get('MAJORIS_TOOLBAR_ARTIFACTS','artifacts/toolbar-polish')/(variant+('-2x' if scale=='2' else ''));out.mkdir(parents=True,exist_ok=True)
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris');ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
 Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
else:
 Gtk.init([]);provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')));Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
import re
icon_theme=Gtk.IconTheme.get_for_display(Gdk.Display.get_default()) if version=='4' else Gtk.IconTheme.get_default()
for icon_name in set(re.findall(r'"([a-z0-9-]+-symbolic)"',(root/'factory/src/toolbars.vala').read_text())):assert icon_theme.has_icon(icon_name),('Unavailable toolbar icon',icon_name)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);atexit.register(wm.terminate)
for attempt in range(40):
 if 'window id' in subprocess.check_output(['xprop','-root','_NET_SUPPORTING_WM_CHECK'],text=True):break
 time.sleep(.05)
def style(widget,*names):
 for name in names:widget.add_css_class(name) if version=='4' else widget.get_style_context().add_class(name)
def append(parent,child,expand=False):
 parent.append(child) if version=='4' else parent.pack_start(child,expand,expand,0)
def children(widget):
 if version=='3':return widget.get_children() if isinstance(widget,Gtk.Container) else []
 result=[];child=widget.get_first_child()
 while child:result.append(child);child=child.get_next_sibling()
 return result
def nodes(widget):
 yield widget
 for child in children(widget):yield from nodes(child)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(250,lambda:(loop.quit(),False)[1]);loop.run()
def box(*classes,spacing=0):
 widget=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=spacing);style(widget,*classes);return widget
def button(text=None,icon=None):
 widget=Gtk.Button();style(widget,'majoris-toolbar-control');widget.set_valign(Gtk.Align.CENTER)
 if icon:
  style(widget,'majoris-toolbar-icon');image=Gtk.Image.new_from_icon_name(icon) if version=='4' else Gtk.Image.new_from_icon_name(icon,Gtk.IconSize.MENU)
  widget.set_child(image) if version=='4' else widget.add(image)
 else:widget.set_label(text)
 return widget
def viewport(widget):
 scroll=Gtk.ScrolledWindow();scroll.set_policy(Gtk.PolicyType.EXTERNAL,Gtk.PolicyType.NEVER)
 if version=='4':scroll.set_propagate_natural_height(True);scroll.set_child(widget)
 else:scroll.set_propagate_natural_height(True);scroll.add(widget);widget.set_focus_hadjustment(scroll.get_hadjustment())
 return scroll
w=Adw.Window(title='Majoris native toolbar GTK'+version) if version=='4' else Gtk.Window(title='Majoris native toolbar GTK'+version)
w.set_default_size(1280,400)
page=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=0)
w.set_content(page) if version=='4' else w.add(page)
nav=box('majoris-toolbar','majoris-toolbar-divider',spacing=4)
group=box('majoris-toolbar-group',spacing=4);append(nav,group)
back=button(icon='go-previous-symbolic');forward=button(icon='go-next-symbolic');forward.set_sensitive(False);append(group,back);append(group,forward)
buttons=[back,forward]
for title in ('Back','Forward','Refresh','Locations'):
 item=button(title);append(group,item);buttons.append(item)
field=Gtk.SearchEntry();field.set_margin_start(4);style(field,'majoris-toolbar-field');field.set_text('Favorites Files Format gyp;!');field.set_valign(Gtk.Align.CENTER);field.set_hexpand(True);append(nav,field,True)
nav_menu=Gtk.MenuButton();nav_menu.set_label('Locations');style(nav_menu,'majoris-toolbar-control','majoris-toolbar-menu');nav_menu.set_valign(Gtk.Align.CENTER)
plain_popup=Gtk.Popover();popup_label=Gtk.Label(label='Favorites Files Format gyp;!')
plain_popup.set_child(popup_label) if version=='4' else plain_popup.add(popup_label)
nav_menu.set_popover(plain_popup);append(nav,nav_menu)
append(page,viewport(nav))
commands=box('majoris-toolbar','majoris-toolbar-divider',spacing=4)
actions=box('majoris-toolbar-group',spacing=4);append(commands,actions)
create=Gtk.Button();style(create,'majoris-toolbar-control','majoris-toolbar-action');create.set_valign(Gtk.Align.CENTER)
contents=box(spacing=8);image=Gtk.Image.new_from_icon_name('folder-new-symbolic') if version=='4' else Gtk.Image.new_from_icon_name('folder-new-symbolic',Gtk.IconSize.MENU);image.set_valign(Gtk.Align.CENTER);append(contents,image);action_label=Gtk.Label(label='New Folder');append(contents,action_label)
create.set_child(contents) if version=='4' else create.add(contents);append(actions,create);buttons.append(create)
for title in ('Cut','Copy','Paste','Rename','Share','Trash'):
 item=button(title);append(actions,item);buttons.append(item)
flat_toggle=Gtk.ToggleButton(label='Format gyp;!');style(flat_toggle,'majoris-toolbar-control','majoris-toolbar-item-flat');flat_toggle.set_valign(Gtk.Align.CENTER);append(actions,flat_toggle)
separator=Gtk.Separator(orientation=Gtk.Orientation.VERTICAL);style(separator,'majoris-toolbar-separator');append(commands,separator)
spacer=box('majoris-toolbar-spacer');spacer.set_hexpand(True);append(commands,spacer,True)
sort=Gtk.MenuButton();sort.set_label('Sort');style(sort,'majoris-toolbar-control','majoris-toolbar-menu');sort.set_valign(Gtk.Align.CENTER)
menu_actions=Gio.SimpleActionGroup()
for name in ('favorites','files','format'):menu_actions.add_action(Gio.SimpleAction.new(name,None))
w.insert_action_group('example',menu_actions)
menu_model=Gio.Menu();menu_model.append('Favorites','example.favorites');menu_model.append('Files','example.files');menu_model.append('Format','example.format')
model_popup=Gtk.PopoverMenu.new_from_model(menu_model) if version=='4' else Gtk.Menu.new_from_model(menu_model)
sort.set_popover(model_popup) if version=='4' else sort.set_popup(model_popup);append(commands,sort)
switcher=box('majoris-toolbar-segmented',spacing=2 if version=='3' else 0);switcher.set_valign(Gtk.Align.CENTER);append(commands,switcher)
segments=[]
for title,name in [('Grid','view-grid-symbolic'),('List','view-list-symbolic'),('Columns','view-dual-symbolic'),('Gallery','view-paged-symbolic')]:
 toggle=Gtk.ToggleButton() if version=='4' else Gtk.RadioButton.new_from_widget(segments[0] if segments else None)
 if version=='3':toggle.set_mode(False)
 toggle.set_tooltip_text(title)
 image_widget=Gtk.Image.new_from_icon_name(name) if version=='4' else Gtk.Image.new_from_icon_name(name,Gtk.IconSize.MENU);image_widget.set_valign(Gtk.Align.CENTER);image_widget.set_halign(Gtk.Align.CENTER)
 toggle.set_child(image_widget) if version=='4' else toggle.add(image_widget)
 if segments:
  if version=='4':toggle.set_group(segments[0])
  else:pass # GtkRadioButton owns exclusive selection and arrow navigation.
 else:toggle.set_active(True)
 append(switcher,toggle);segments.append(toggle)
settings=Gtk.MenuButton();settings.set_label('View Settings');style(settings,'majoris-toolbar-control','majoris-toolbar-menu');settings.set_valign(Gtk.Align.CENTER);settings.set_menu_model(menu_model);append(commands,settings)
command_scroll=viewport(commands);append(page,command_scroll)
legacy=box('majoris-toolbar-navigation',spacing=4 if version=='3' else 0)
legacy_a=button('Back');legacy_b=button('Refresh');append(legacy,legacy_a);append(legacy,legacy_b)
legacy_group=box('majoris-toolbar-group',spacing=4 if version=='3' else 0);legacy_c=button('Undo');legacy_d=button('Redo');append(legacy_group,legacy_c);append(legacy_group,legacy_d);append(legacy,legacy_group);append(page,legacy)
editor=box('majoris-editor-toolbar',spacing=4);edit_button=Gtk.Button(label='Bold');edit_button.set_valign(Gtk.Align.CENTER);append(editor,edit_button)
if version=='4':append(page,editor)
note=Gtk.Label(label='32px standard controls; native scrolling at narrow widths; editor actions remain 28px.');style(note,'majoris-toolbar-metadata');note.set_wrap(True) if version=='4' else note.set_line_wrap(True);append(page,note)
plain_entry=Gtk.Entry();style(plain_entry,'majoris-toolbar-field');plain_entry.set_text('Favorites Files Format gyp;!');plain_entry.set_valign(Gtk.Align.CENTER);append(page,plain_entry)
w.present() if version=='4' else w.show_all();settle()
def bounds(widget,parent):
 if version=='4':
  ok,rect=widget.compute_bounds(parent);assert ok;return [rect.get_x(),rect.get_y(),rect.get_width(),rect.get_height()]
 x,y=widget.translate_coordinates(parent,0,0);return [x,y,widget.get_allocated_width(),widget.get_allocated_height()]
def capture(name):
 settle();wid=subprocess.check_output(['xdotool','search','--name','^Majoris native toolbar GTK'+version+'$'],text=True).splitlines()[0]
 path=out/(('gtk3-' if version=='3' else '')+name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
def geometry():return dict(navigation=nav.get_allocated_height(),commands=commands.get_allocated_height(),icon=[back.get_allocated_width(),back.get_allocated_height()],text=create.get_allocated_height(),search=field.get_allocated_height(),switcher=switcher.get_allocated_height())
assert legacy.get_allocated_height()==40
la,lb,lc,ld=[bounds(item,page) for item in (legacy_a,legacy_b,legacy_c,legacy_d)]
assert la[0]-bounds(legacy,page)[0]==8,(la,bounds(legacy,page))
assert lb[0]-la[0]-la[2]==4,(la,lb)
assert ld[0]-lc[0]-lc[2]==4,(lc,ld)
assert lc[0]-lb[0]-lb[2]==8,(lb,lc)
style(legacy,'majoris-toolbar-major-groups');settle()
assert bounds(legacy_c,page)[0]-bounds(legacy_b,page)[0]-legacy_b.get_allocated_width()==16
legacy.remove_css_class('majoris-toolbar-major-groups') if version=='4' else legacy.get_style_context().remove_class('majoris-toolbar-major-groups');settle()
assert not Gtk.Settings.get_default().get_property('gtk-enable-animations'),'Reduced motion setting was lost'
assert plain_entry.get_allocated_height()==32,('native entry',plain_entry.get_allocated_height())
# Measure the same strip and existing controls at both densities.
padding=nav.get_style_context().get_padding() if version=='4' else nav.get_style_context().get_padding(Gtk.StateFlags.NORMAL)
outer_x=padding.left
assert outer_x==8,('outer inset',outer_x)
standard=geometry()
assert bounds(back,nav)[1]+(padding.top if version=='4' else 0)==4,('standard centring',bounds(back,nav))
for strip in (nav,commands):style(strip,'majoris-toolbar-compact')
settle()
compact=geometry()
assert compact==dict(navigation=40,commands=40,icon=[28,28],text=28,search=28,switcher=32),compact
outer_y=padding.top if version=='4' else 0
assert bounds(back,nav)[1]+outer_y==6,('compact centring',bounds(back,nav),outer_y)
style(create,'majoris-toolbar-item-flat')
compact_text=[]
for label in nodes(page):
 if isinstance(label,Gtk.Label) and label.get_mapped() and label.get_text():
  layout=label.get_layout();ink,logical=layout.get_pixel_extents();x,y=label.get_layout_offsets()
  if version=='3':allocation=label.get_allocation();x-=allocation.x;y-=allocation.y
  assert y+ink.y>=0 and y+ink.y+ink.height<=label.get_allocated_height(),('compact glyph clip',label.get_text())
  assert logical.width<=label.get_allocated_width(),('compact label width',label.get_text())
  compact_text.append(dict(text=label.get_text(),ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.width,logical.height],allocation=[label.get_allocated_width(),label.get_allocated_height()],baseline=layout.get_baseline()/Pango.SCALE))
assert next(item for item in nodes(back) if isinstance(item,Gtk.Image)).get_allocated_height()==16
(out/('gtk'+version+'-compact-text.json')).write_text(json.dumps(compact_text,indent=2)+'\n')
capture('compact-toolbar')
# Native width reservation for GTK-only composition (the Vala component does this itself).
label=next(item for item in nodes(flat_toggle) if isinstance(item,Gtk.Label))
widths=[]
for weight in (Pango.Weight.MEDIUM,Pango.Weight.SEMIBOLD):
 desc=label.get_pango_context().get_font_description().copy();desc.set_weight(weight)
 layout=label.create_pango_layout(label.get_text());layout.set_font_description(desc);widths.append(layout.get_pixel_size()[0])
label.set_size_request(max(widths),-1);settle()
flat_position=bounds(flat_toggle,commands)
flat_label=next(item for item in nodes(flat_toggle) if isinstance(item,Gtk.Label))
flat_baseline=flat_label.get_layout().get_baseline()
compact_states=[]
for flag,name in [(Gtk.StateFlags.PRELIGHT,'hover'),(Gtk.StateFlags.ACTIVE,'pressed'),(Gtk.StateFlags.FOCUSED | (Gtk.StateFlags.FOCUS_VISIBLE if version=='4' else Gtk.StateFlags.NORMAL),'focus'),(Gtk.StateFlags.BACKDROP,'backdrop')]:
 flat_toggle.set_state_flags(flag,False);settle()
 assert geometry()==compact and bounds(flat_toggle,commands)==flat_position
 assert flat_label.get_layout().get_baseline()==flat_baseline
 compact_states.append(dict(state=name,geometry=geometry(),flat=bounds(flat_toggle,commands)))
 if name=='focus':capture('compact-flat-focus')
 flat_toggle.unset_state_flags(flag)
flat_toggle.set_active(True);settle();assert flat_toggle.get_active() and bounds(flat_toggle,commands)==flat_position;capture('compact-flat-selected')
flat_toggle.set_sensitive(False);settle();assert geometry()==compact;flat_toggle.set_sensitive(True)
(out/('gtk'+version+'-compact-focus.json')).write_text(json.dumps(compact_states,indent=2)+'\n')
create.remove_css_class('majoris-toolbar-item-flat') if version=='4' else create.get_style_context().remove_class('majoris-toolbar-item-flat')
for strip in (nav,commands):
 strip.remove_css_class('majoris-toolbar-compact') if version=='4' else strip.get_style_context().remove_class('majoris-toolbar-compact')
settle()
(out/('gtk'+version+'-compact.json')).write_text(json.dumps(compact,indent=2)+'\n')
initial=geometry();assert initial==dict(navigation=40,commands=40,icon=[32,32],text=32,search=32,switcher=32),initial
if version=='4':assert editor.get_allocated_height()==40 and edit_button.get_allocated_height()==28
icon_widget=next(item for item in nodes(back) if isinstance(item,Gtk.Image));assert [icon_widget.get_allocated_width(),icon_widget.get_allocated_height()]==[16,16]
assert bounds(forward,group)[0]-sum(bounds(back,group)[::2])==4,('within-group gap',bounds(back,group),bounds(forward,group))
assert bounds(field,nav)[0]-(bounds(group,nav)[0]+bounds(group,nav)[2])==8,('group gap',bounds(field,nav),bounds(group,nav))
assert bounds(action_label,contents)[0]-(bounds(image,contents)[0]+bounds(image,contents)[2])==8,('icon-label gap',bounds(image,contents),bounds(action_label,contents))
for label in nodes(create):
 if isinstance(label,Gtk.Label):
  desc=label.get_pango_context().get_font_description()
  assert desc.get_weight()==Pango.Weight.SEMIBOLD,desc.to_string()
  size=desc.get_size()/Pango.SCALE*(1 if desc.get_size_is_absolute() else 96/72)
  assert size==14,desc.to_string()
field_layout=field.create_pango_layout(field.get_text());field_ink,field_logical=field_layout.get_pixel_extents()
assert field_logical.height<=field.get_allocated_height()-2 and field_ink.y>=0,'Field glyphs clipped'
metrics=[]
def measure_label(label,source='toolbar',absolute_size=None):
 layout=label.get_layout();ink,logical=layout.get_pixel_extents();x,y=label.get_layout_offsets()
 if version=='3':allocation=label.get_allocation();x-=allocation.x;y-=allocation.y
 assert y+ink.y>=0 and y+ink.y+ink.height<=label.get_allocated_height(),(label.get_text(),'glyph clip')
 assert logical.width<=label.get_allocated_width(),(label.get_text(),'label width clipped')
 desc=label.get_pango_context().get_font_description().copy()
 if absolute_size is not None:desc.set_absolute_size(absolute_size*Pango.SCALE)
 font_metrics=label.get_pango_context().get_metrics(desc,label.get_pango_context().get_language())
 resolved=label.get_pango_context().load_font(desc).describe().to_string()
 return dict(resolved_font=resolved,source=source,text=label.get_text(),allocation=[label.get_allocated_width(),label.get_allocated_height()],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.width,logical.height],layout_origin=[x,y],baseline=layout.get_baseline()/Pango.SCALE,ascent=font_metrics.get_ascent()/Pango.SCALE,descent=font_metrics.get_descent()/Pango.SCALE,font=desc.to_string())
for label in nodes(page):
 if isinstance(label,Gtk.Label) and label.get_text() and label.get_mapped():metrics.append(measure_label(label))
metrics.append(dict(source='search-field',text=field.get_text(),allocation=[field.get_allocated_width(),field.get_allocated_height()],ink=[field_ink.x,field_ink.y,field_ink.width,field_ink.height],logical=[field_logical.width,field_logical.height],baseline=field_layout.get_baseline()/Pango.SCALE,font=field.get_pango_context().get_font_description().to_string()))
for name in ('navigation-toolbar','command-toolbar','stacked-toolbars','toolbar-view-switcher','editor-toolbar-comparison'):capture(name)
state_records=[]
label_before=bounds(action_label,commands);baseline_before=action_label.get_layout().get_baseline()
for state,name in [(Gtk.StateFlags.PRELIGHT,'hover'),(Gtk.StateFlags.ACTIVE,'pressed'),(Gtk.StateFlags.FOCUSED | (Gtk.StateFlags.FOCUS_VISIBLE if version=='4' else Gtk.StateFlags.NORMAL),'focus'),(Gtk.StateFlags.BACKDROP,'inactive')]:
 for item in (back,create,segments[0],nav,commands,switcher):item.set_state_flags(state,False)
 settle();assert geometry()==initial,(name,geometry());assert bounds(action_label,commands)==label_before and action_label.get_layout().get_baseline()==baseline_before,(name,'text moved');state_records.append(dict(state=name,geometry=geometry()));capture('toolbar-'+name)
 for item in (back,create,segments[0],nav,commands,switcher):item.unset_state_flags(state)
back.set_sensitive(False);capture('toolbar-disabled');assert geometry()==initial;back.set_sensitive(True)
segments[1].set_active(True);assert segments[1].get_active() and not segments[0].get_active();segments[2].grab_focus();settle()
subprocess.run(['xdotool','key','space'],check=True);settle();assert segments[2].get_active() and sum(item.get_active() for item in segments)==1,'Native keyboard selection failed'
for menu in (nav_menu,sort):
 menu.popup() if version=='4' else menu.set_active(True);settle()
 popup=plain_popup if menu==nav_menu else model_popup
 if version=='3':popup.show_all();settle()
 assert popup.get_mapped()
 for label in nodes(popup):
  if isinstance(label,Gtk.Label) and label.get_text() in ('Favorites','Files','Format'):
   desc=label.get_pango_context().get_font_description()
   assert desc.get_weight()==Pango.Weight.MEDIUM,(label.get_text(),'toolbar style leaked into menu',desc.to_string())
   metrics.append(measure_label(label,'popup'))
 popup_name='toolbar-popover-'+('navigation' if menu==nav_menu else 'commands')
 capture(popup_name)
 native_surface=popup.get_native().get_surface() if version=='4' else popup.get_window()
 popup_id=native_surface.get_xid()
 path=out/(('gtk3-' if version=='3' else '')+popup_name+'-surface.xwd')
 subprocess.run(['xwd','-silent','-id',str(popup_id),'-out',str(path)],check=True);subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
 popup.popdown()
# Font changes must be measured naturally instead of cropped into a fixed strip.
action_label.set_text('New Folder gyp;!');attrs=Pango.AttrList();attrs.insert(Pango.attr_size_new_absolute(40*Pango.SCALE));action_label.set_attributes(attrs);settle();assert commands.get_allocated_height()>40;metrics.append(measure_label(action_label,'accessibility-40px',40));capture('toolbar-large-text');action_label.set_attributes(None);action_label.set_text('New Folder');settle()
w.set_default_size(480,400) if version=='4' else w.resize(480,400);settle();assert w.get_allocated_width()==480,('narrow resize',w.get_allocated_width());assert nav.get_allocated_height()==40 and commands.get_allocated_height()==40;segments[3].grab_focus();settle();assert command_scroll.get_hadjustment().get_value()>0,'Narrow row did not scroll to keyboard focus';capture('toolbar-narrow')
(out/('gtk'+version+'-measurements.json')).write_text(json.dumps(initial,indent=2)+'\n')
(out/('gtk'+version+'-text-metrics.json')).write_text(json.dumps(metrics,indent=2)+'\n')
(out/('gtk'+version+'-focus-states.json')).write_text(json.dumps(state_records,indent=2)+'\n')
w.destroy()
if version=='4':
 records=[]
 for mode in ('toolbars','toolbars-narrow','toolbars-editing','toolbars-stacked','toolbars-files-parent'):
  probe=subprocess.run([str(root/'build/factory/majoris-theme-factory'),'--page='+mode,'--'+variant],env={**os.environ,'MAJORIS_TOOLBAR_PROBE':'1'},capture_output=True,text=True,check=True,timeout=10)
  record=json.loads(next(line for line in probe.stdout.splitlines() if line.startswith('{')))
  expected=dict(navigation=40,commands=40,back=[32,32],location=32,search=32,switcher=32)
  if mode not in ('toolbars-stacked','toolbars-files-parent'):expected.update(compact_toolbar=40,compact_button=28,mixed_toolbar=40,dropdown=32)
  for name,value in expected.items():assert record[name]==value,(mode,record)
  assert record['window_width']==(480 if mode=='toolbars-narrow' else 1280),(mode,record)
  if mode=='toolbars-editing':assert record['entry']==26,record
  else:assert record['crumb']==26,record
  if mode=='toolbars-stacked':assert record['tabs']==40 and record['navigation_y']==40 and record['commands_y']==80,record
  if mode=='toolbars-files-parent':assert record['tabs']==40 and record['navigation_y']>=40 and record['commands_y']-record['navigation_y']==40,record
  records.append(dict(mode=mode,**record))
 (out/'factory-measurements.json').write_text(json.dumps(records,indent=2)+'\n')
print('Native toolbar geometry, text, state stability and isolation fixture passed',version,variant,scale)
