"""Real menu/Pango allocation regression and native review capture (GTK3/4)."""
import os, sys, json, subprocess, ctypes, atexit, re
os.environ["GSK_RENDERER"]="cairo"
from pathlib import Path
import gi
version=sys.argv[1] if len(sys.argv)>1 else '4'
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk, GLib, Gio, Pango
root=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light')
scale=os.environ.get('GDK_SCALE','1')
baseline=os.environ.get('MAJORIS_MENU_BASELINE')
theme_root=Path(baseline) if baseline else root/'theme/Majoris'
out=root/'artifacts/menu-v2/after'/(('before-' if baseline else '')+f'gtk{version}-{variant}-{scale}x')
out.mkdir(parents=True,exist_ok=True)
if version=='4':
 gi.require_version('Adw','1')
 from gi.repository import Adw
 Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(theme_root)
 ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
 Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
else:
 Gtk.init([])
 provider=Gtk.CssProvider();provider.load_from_path(str(theme_root/'gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 from gi.repository import Gdk
 Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);atexit.register(wm.terminate)

app=Gtk.Application(application_id='com.majoris.MenuRegression',flags=Gio.ApplicationFlags.NON_UNIQUE);app.register(None)
window=Gtk.ApplicationWindow(application=app,title='Majoris native menu measurements');window.set_default_size(720,720)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16)
strings=['New Folder…','File','Find','Format','Move to Folder with a longer descriptive name','Open With','Preferences']
model=Gio.Menu();group=Gio.SimpleActionGroup()
for i,text in enumerate(strings):
 action=Gio.SimpleAction.new('item'+str(i),None);group.add_action(action)
 item=Gio.MenuItem.new(text,'test.item'+str(i));item.set_attribute_value('accel',GLib.Variant('s','<Control>F'));model.append_item(item)
disabled=Gio.SimpleAction.new('disabled',None);disabled.set_enabled(False);group.add_action(disabled);model.append('Unavailable action','test.disabled')
checked=Gio.SimpleAction.new_stateful('hidden',None,GLib.Variant('b',True));group.add_action(checked);model.append('Show Hidden Files','test.hidden')
radio=Gio.SimpleAction.new_stateful('sort',GLib.VariantType.new('s'),GLib.Variant('s','name'));group.add_action(radio)
model.append('By Name','test.sort::name');model.append('By Date','test.sort::date')
icon=Gio.MenuItem.new('Open','test.item0');icon.set_icon(Gio.ThemedIcon.new('document-open-symbolic'));model.prepend_item(icon)
trash=Gio.MenuItem.new('Move to Trash','test.item0')
if version=='4':trash.set_attribute_value('custom',GLib.Variant('s','trash'))
section=Gio.Menu();section.append_item(trash);model.append_section(None,section)
sub=Gio.Menu();sub.append('Text Editor','test.item0');model.append_submenu('Open With',sub)
window.insert_action_group('test',group)
if version=='4':
 window.set_child(box);box.append(Gtk.Label(label='Underlying application text — opaque native menu surface'))
 button=Gtk.MenuButton(label='File context menu');popover=Gtk.PopoverMenu.new_from_model(model);button.set_popover(popover);box.append(button)
 trash_button=Gtk.Button(label='Move to Trash');trash_button.add_css_class('majoris-menu-danger');popover.add_child(trash_button,'trash')
 dropdown=Gtk.DropDown.new_from_strings(['Automatic','Ask every time','Never']);box.append(dropdown)
else:
 window.add(box);box.pack_start(Gtk.Label(label='Underlying application text — opaque native menu surface'),False,False,0)
 button=Gtk.MenuButton(label='File context menu');menu=Gtk.Menu.new_from_model(model);button.set_popup(menu);box.pack_start(button,False,False,0)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(250,lambda:(loop.quit(),False)[1]);loop.run()
def children(w):
 if version=='3':return w.get_children() if isinstance(w,Gtk.Container) else []
 result=[];c=w.get_first_child()
 while c:result.append(c);c=c.get_next_sibling()
 return result
def walk(w):
 yield w
 for child in children(w):yield from walk(child)
def capture(name):
 settle()
 path=out/(name+'.xwd');subprocess.run(['xwd','-silent','-root','-out',str(path)],check=True)
 subprocess.run(['magick',str(path),str(out/(name+'.png'))],check=True);path.unlink()
 tree=subprocess.check_output(['xwininfo','-root','-tree'],text=True)
 (out/(name+'-xwindows.txt')).write_text(tree)
 ids=re.findall(r'^     (0x[0-9a-f]+) .*?  ([0-9]+)x([0-9]+)\+',tree,re.M)
 ids=[wid for wid,width,height in ids if int(width)>100 and int(height)>100 and ('has no name' in next(line for line in tree.splitlines() if wid in line) or version=='3')]
 for index,wid in enumerate(ids):
  info=subprocess.check_output(['xwininfo','-id',wid],text=True)
  if 'Map State: IsViewable' not in info:continue
  path=out/(name+f'-surface-{index}.xwd')
  subprocess.run(['xwd','-silent','-id',wid,'-out',str(path)],check=True)
  subprocess.run(['magick',str(path),str(path.with_suffix('.png'))],check=True);path.unlink()
window.present() if version=='4' else window.show_all();settle()
wid=subprocess.check_output(['xdotool','search','--name','^Majoris native menu measurements$'],text=True).splitlines()[0]
subprocess.run(['xdotool','windowmove',wid,'400','240'],check=True);settle()
button.popup() if version=='4' else button.set_active(True);settle()
surface=popover if version=='4' else menu
if version=='3':
 for w in walk(surface):
  if isinstance(w,Gtk.Label) and w.get_text()=='Move to Trash':w.get_parent().get_style_context().add_class('majoris-menu-danger')
settle()
results=[]
for w in walk(surface):
 if not isinstance(w,Gtk.Label) or w.get_text() not in strings or not w.get_mapped():continue
 layout=w.get_layout();ink,logical=layout.get_pixel_extents();height=w.get_allocated_height();width=w.get_allocated_width()
 desc=layout.get_context().get_font_description()
 result=dict(text=w.get_text(),row_height=w.get_parent().get_allocated_height(),baseline=layout.get_baseline()/Pango.SCALE,allocation=[width,height],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.x,logical.y,logical.width,logical.height],font=desc.to_string())
 results.append(result)
 assert baseline or result['row_height']>=32,(result,'row below completed target')
 assert height>=logical.height,(result,'logical text clipped')
 assert ink.y>=0 and ink.y+ink.height<=height,(result,'glyph ink clipped')
 assert width>=logical.width,(result,'text width clipped')
 if version=='3' and isinstance(w,Gtk.AccelLabel) and w.get_accel_width():
  assert width>=logical.width+w.get_accel_width()+16,(result,'accelerator overlaps label')
 assert baseline or desc.get_weight()==Pango.Weight.MEDIUM,result
 pixels=desc.get_size()/Pango.SCALE
 if not desc.get_size_is_absolute():pixels*=w.get_pango_context().get_resolution()/72 if hasattr(w.get_pango_context(),'get_resolution') else 96/72
 assert baseline or abs(pixels-14)<.1,result
assert len(results)>=len(strings),results
if version=='4':
 for w in walk(surface):
  if isinstance(w,Gtk.Label) and w.get_mapped() and 'Ctrl' in w.get_text():
   desc=w.get_layout().get_context().get_font_description()
   assert desc.get_weight()==Pango.Weight.SEMIBOLD,(w.get_text(),desc.to_string())
   assert desc.get_size()/Pango.SCALE==12,(w.get_text(),desc.to_string())
capture('context-shortcuts-submenu')
for label in walk(surface):
 if isinstance(label,Gtk.Label) and label.get_mapped() and label.get_text()=='New Folder…':
  attrs=Pango.AttrList();attrs.insert(Pango.attr_size_new_absolute(32*Pango.SCALE));label.set_attributes(attrs);settle()
  ink,logical=label.get_layout().get_pixel_extents()
  assert label.get_allocated_height()>=logical.height
  assert label.get_parent().get_allocated_height()>32
  label.set_attributes(None);settle();break
# Capture native held states on the actual menu rows, with no application CSS.
rows=[]
for w in walk(surface):
 if isinstance(w,Gtk.Label) and w.get_mapped() and w.get_text() in strings:
  row=w.get_parent()
  if row not in rows:rows.append(row)
focus=Gtk.StateFlags.FOCUSED | (Gtk.StateFlags.FOCUS_VISIBLE if version=='4' else Gtk.StateFlags.NORMAL)
flags=[Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,focus,Gtk.StateFlags.INSENSITIVE]
for row,flag in zip(rows,flags):row.set_state_flags(flag,False)
settle();capture('interaction-states')
for row,flag in zip(rows,flags):row.unset_state_flags(flag)
# Open the real submenu and record its child surface.
for w in walk(surface):
 if isinstance(w,Gtk.Label) and w.get_mapped() and w.get_text()=='Open With':
  parent=w.get_parent()
  if version=='4' and parent.get_css_name()=='modelbutton' and parent.find_property('menu-name') and parent.get_property('menu-name'):parent.activate();settle();capture('submenu');break
  if version=='3' and isinstance(parent,Gtk.MenuItem) and parent.get_submenu():parent.select();parent.get_submenu().popup_at_widget(parent,Gdk.Gravity.NORTH_EAST,Gdk.Gravity.NORTH_WEST,None);settle();capture('submenu');break


(out/'measurements.json').write_text(json.dumps(results,indent=2)+'\n')
if version=='4':
 popover.popdown();dropdown.get_first_child().activate();settle();
 for w in walk(dropdown):
  if isinstance(w,Gtk.Popover) and w.get_mapped():
   for child in children(w):
    if child.get_css_name()=='contents':
     padding=child.get_style_context().get_padding()
     assert [padding.top,padding.right,padding.bottom,padding.left]==[8,8,8,8],('chooser padding changed',w.get_css_classes(),padding)
   w.queue_draw()
 settle();capture('dropdown')
 for w in walk(dropdown):
  if isinstance(w,Gtk.Popover):w.popdown()
 # Place the native window near the monitor edge; GTK owns popup anchoring.
 wid=subprocess.check_output(['xdotool','search','--name','^Majoris native menu measurements$'],text=True).splitlines()[0]
 subprocess.run(['xdotool','windowmove',wid,'2200','1450'],check=True);settle();button.popup();settle();capture('screen-boundary')
# Majoris-controlled native rows: individual keys, real actions and real input.
sys.path.insert(0,str(root/'integration'))
from menu_rows import menu_row
specs=[('Rename','rename','F2',['F2']),('Move to Trash','trash','Delete',['Delete']),('Properties','properties','<Alt>Return',['Alt','Return']),('Open Preview','preview','space',['Space']),('Copy','copy','<Control>c',['Ctrl','C']),('Paste','paste','<Control>v',['Ctrl','V']),('Long action with descending glyphs','long','<Control><Shift>g',['Ctrl','Shift','g']),('Punctuation','punctuation','<Control>semicolon',['Ctrl',';']),('Unavailable action','unavailable-v2','<Control>u',['Ctrl','U'])]
activated=[]
custom_model=Gio.Menu();custom_rows=[]
if version=='4':
 custom=Gtk.PopoverMenu.new_from_model(custom_model)
 custom_button=Gtk.MenuButton(label='Individual native keycaps');custom_button.set_popover(custom);box.append(custom_button)
 # Use the real application accelerator registry, as the factory does.
else:
 custom=Gtk.Menu();custom_button=Gtk.MenuButton(label='Individual native keycaps');custom_button.set_popup(custom);box.pack_start(custom_button,False,False,0)
 accel_group=Gtk.AccelGroup();window.add_accel_group(accel_group);custom.set_accel_group(accel_group)
for title,name,accel,keys in specs:
 action=Gio.SimpleAction.new(name,None);action.connect('activate',lambda action,param:activated.append(action.get_name()));group.add_action(action);window.add_action(action)
 row=menu_row(title,keys,action='win.'+name,shortcut=accel,icon='document-open-symbolic' if name=='rename' else None)
 if name=='trash':row.add_css_class('majoris-menu-danger') if version=='4' else row.get_style_context().add_class('majoris-menu-danger')
 if version=='4':
  slot=Gio.MenuItem.new(title,None);slot.set_attribute_value('custom',GLib.Variant('s',name));custom_model.append_item(slot);custom.add_child(row,name)
  app.set_accels_for_action('win.'+name,[accel])
 else:
  custom.append(row);key,mods=Gtk.accelerator_parse(accel);row.add_accelerator('activate',accel_group,key,mods,Gtk.AccelFlags.VISIBLE)
 app.set_accels_for_action('win.'+name,[accel])
 if name=='unavailable-v2':action.set_enabled(False)
 custom_rows.append(row)
if version=='4':popover.popdown();custom_button.popup()
else:
 for item in menu.get_children():
  if isinstance(item,Gtk.MenuItem) and item.get_submenu():item.get_submenu().popdown()
 menu.popdown();button.set_active(False);window.show_all();custom.show_all();custom_button.set_active(True)
settle()
key_results=[]
for w in walk(custom):
 is_cap=w.has_css_class('majoris-menu-keycap') if version=='4' else w.get_style_context().has_class('majoris-menu-keycap')
 if not is_cap:continue
 layout=w.get_layout();ink,logical=layout.get_pixel_extents();desc=layout.get_context().get_font_description()
 width,height=w.get_allocated_width(),w.get_allocated_height()
 # Label allocation includes CSS padding/border in GTK3; layout size is the content evidence.
 assert width>=logical.width and height>=logical.height,(w.get_text(),width,height,logical)
 assert ink.y>=0 and ink.y+ink.height<=logical.height,(w.get_text(),ink,logical)
 assert desc.get_weight()==Pango.Weight.SEMIBOLD,desc.to_string()
 offset_x,offset_y=w.get_layout_offsets()
 if version=='3':
  # GTK3 returns offsets in the shared GdkWindow coordinate system.
  allocation=w.get_allocation();offset_x-=allocation.x;offset_y-=allocation.y
 assert offset_y+ink.y>=0 and offset_y+ink.y+ink.height<=height,(w.get_text(),'parent glyph clip',offset_y,height,ink)
 metrics=layout.get_context().get_metrics(desc,layout.get_context().get_language())
 key_results.append(dict(key=w.get_text(),layout_origin=[offset_x,offset_y],allocation=[width,height],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.x,logical.y,logical.width,logical.height],baseline=layout.get_baseline()/Pango.SCALE,ascent=metrics.get_ascent()/Pango.SCALE,descent=metrics.get_descent()/Pango.SCALE,font=desc.to_string()))
assert len(key_results)==sum(len(keys) for _,_,_,keys in specs)
(out/'keycap-measurements.json').write_text(json.dumps(key_results,indent=2)+'\n')
tree_geometry=[]
for widget in walk(custom):
 if not widget.get_mapped():continue
 context=widget.get_style_context()
 padding=context.get_padding() if version=='4' else context.get_padding(widget.get_state_flags())
 margin=context.get_margin() if version=='4' else context.get_margin(widget.get_state_flags())
 if version=='4':
  ok,bounds=widget.compute_bounds(custom);position=[bounds.get_x(),bounds.get_y()] if ok else None
 else:position=widget.translate_coordinates(custom,0,0)
 tree_geometry.append(dict(type=type(widget).__name__,css_name=widget.get_css_name() if version=='4' else '',classes=list(context.list_classes()) if version=='3' else list(widget.get_css_classes()),position=position,size=[widget.get_allocated_width(),widget.get_allocated_height()],padding=[padding.top,padding.right,padding.bottom,padding.left],margin=[margin.top,margin.right,margin.bottom,margin.left]))
if version=='4':
 contents=next(item for item in tree_geometry if item['type']=='GtkPopoverContent')
 assert contents['padding']==[4,4,4,4],contents
 ok,row_bounds=custom_rows[0].compute_bounds(custom)
 assert ok and row_bounds.get_x()-contents['position'][0]==5 and row_bounds.get_y()-contents['position'][1]==5,('extra menu inset',row_bounds,contents)
else:
 padding=custom.get_style_context().get_padding(custom.get_state_flags())
 assert [padding.top,padding.right,padding.bottom,padding.left]==[4,4,4,4]
(out/'widget-geometry.json').write_text(json.dumps(tree_geometry,indent=2)+'\n')
capture('individual-keycaps')
assert not custom_rows[-1].get_sensitive(),'Disabled action did not disable its custom row'
for row,flag in zip(custom_rows[:3],[Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,focus]):row.set_state_flags(flag,False)
capture('keycap-states')
for row,flag in zip(custom_rows[:3],[Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,focus]):row.unset_state_flags(flag)
for cap in walk(custom_rows[0]):
 is_cap=cap.has_css_class('majoris-menu-keycap') if version=='4' else cap.get_style_context().has_class('majoris-menu-keycap')
 if not is_cap:continue
 attrs=Pango.AttrList();attrs.insert(Pango.attr_size_new_absolute(24*Pango.SCALE));cap.set_attributes(attrs);settle()
 assert cap.get_allocated_height()>=cap.get_layout().get_pixel_extents()[1].height,'Enlarged shortcut clipped'
 capture('keycaps-large-font');cap.set_attributes(None);settle();break
if version=='4':custom_rows[0].grab_focus()
else:custom.select_item(custom_rows[0])
settle();subprocess.run(['xdotool','key','Down'],check=True);settle()
assert (custom_rows[1].has_focus() if version=='4' else custom.get_selected_item()==custom_rows[1]),'Down did not navigate to next native row'
subprocess.run(['xdotool','key','Up'],check=True);settle()
settle();subprocess.run(['xdotool','key','Return'],check=True);settle()
assert 'rename' in activated,activated
assert not custom.get_mapped(),'Enter did not dismiss menu'
custom_button.popup() if version=='4' else custom_button.set_active(True);settle()
subprocess.run(['xdotool','key','Escape'],check=True);settle();assert not custom.get_mapped(),'Escape did not dismiss menu'
# Real accelerator is registered with GtkShortcutController/GtkAccelGroup.
window.present();custom_button.grab_focus();settle();subprocess.run(['xdotool','windowactivate','--sync',wid],check=True);settle();subprocess.run(['xdotool','key','F2'],check=True);settle();
assert activated.count('rename')==2,activated
window.destroy()
print(json.dumps(dict(toolkit=version,variant=variant,scale=scale,labels=len(results),measurements=str(out/'measurements.json'))))
