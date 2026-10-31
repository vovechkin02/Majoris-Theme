"""Native libadwaita geometry, typography, semantics, input and renderer evidence."""
import ctypes,json,os,re,subprocess,sys
from pathlib import Path
import gi
gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
from gi.repository import Gtk,Adw,Gdk,GLib,Pango
root=Path(__file__).resolve().parents[1];variant=os.environ.get('MAJORIS_VARIANT','light');scale=int(os.environ.get('GDK_SCALE','1'));renderer=os.environ.get('GSK_RENDERER','default');large=bool(os.environ.get('MAJORIS_LARGE_FONT'))
out=root/'artifacts/actionrow-finalisation'/variant/(renderer+'-'+str(scale)+'x'+('-large-font' if large else ''));out.mkdir(parents=True,exist_ok=True)
Adw.init();os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris');ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
settings=Gtk.Settings.get_default();settings.set_property('gtk-enable-animations',False)
if large:settings.set_property('gtk-xft-dpi',144*1024)
w=Adw.Window(title='Majoris preferences validation',default_width=760,default_height=900)
scroll=Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER);w.set_content(scroll)
body=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16,margin_start=24,margin_end=24,margin_top=24,margin_bottom=24);scroll.set_child(body)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(180,lambda:(loop.quit(),False)[1]);loop.run()
def children(x):
 c=x.get_first_child()
 while c:yield c;c=c.get_next_sibling()
def nodes(x):
 yield x
 for c in children(x):yield from nodes(c)
def box_of(x,cls):return next(c for c in children(x) if c.get_css_name()=='box' and c.has_css_class(cls))
def bounds(x,parent):
 ok,r=x.compute_bounds(parent);assert ok;return [r.get_x(),r.get_y(),r.get_width(),r.get_height()]
def alloc(x):return [x.get_allocated_width(),x.get_allocated_height()]
def group(title='',description=''):
 g=Adw.PreferencesGroup(title=title,description=description);body.append(g);return g
def action(g,title,subtitle='',**kwargs):
 r=Adw.ActionRow(title=title,subtitle=subtitle,**kwargs);g.add(r);return r
g=group('Information','Selectable properties and native controls')
header_button=Gtk.Button(icon_name='list-add-symbolic',valign=Gtk.Align.CENTER);g.set_header_suffix(header_button)
single=action(g,'Single line')
two=action(g,'Size','19 bytes',subtitle_selectable=True)
passive=action(g,'Passive information','Independent Copy suffix',subtitle_selectable=True)
copy=Gtk.Button(label='Copy',valign=Gtk.Align.CENTER);passive.add_suffix(copy);copied=[];copy.connect('clicked',lambda *_:(copied.append(True),copy.get_clipboard().set('19 bytes')))
interactive=action(g,'Interactive action','Keyboard activation')
activate=Gtk.Button(label='Activate',valign=Gtk.Align.CENTER);interactive.add_suffix(activate);interactive.set_activatable_widget(activate);activated=[];activate.connect('clicked',lambda *_:activated.append(True))
prefix=action(g,'Prefix and suffix',icon_name='document-properties-symbolic');suffix=Gtk.Switch(valign=Gtk.Align.CENTER);prefix.add_suffix(suffix)
prop=action(g,'Type','Plain text document',subtitle_selectable=True);prop.add_css_class('property')
disabled=action(g,'Disabled row','Still legible');disabled.set_sensitive(False)
# A heading-only group makes the gap independently measurable.
heading_only=group('Organisation');heading_row=Adw.SwitchRow(title='Favorite');heading_only.add(heading_row)
w.present();settle()
wid=subprocess.check_output(['xdotool','search','--name','^Majoris preferences validation$'],text=True).splitlines()[-1]
subprocess.run(['xdotool','windowfocus',wid],check=True)
lib=ctypes.CDLL('libgtk-4.so.1');lib.gtk_snapshot_to_node.argtypes=[ctypes.c_void_p];lib.gtk_snapshot_to_node.restype=ctypes.c_void_p
lib.gsk_render_node_write_to_file.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_void_p];lib.gsk_render_node_write_to_file.restype=ctypes.c_int;lib.gsk_render_node_unref.argtypes=[ctypes.c_void_p]
def render(widget,name):
 settle();snap=Gtk.Snapshot();Gtk.WidgetPaintable.new(widget).snapshot(snap,*alloc(widget));node=lib.gtk_snapshot_to_node(hash(snap));assert node
 p=out/(name+'.node');assert lib.gsk_render_node_write_to_file(node,str(p).encode(),None);lib.gsk_render_node_unref(node);return p.read_text()
def capture(name):
 scroll.get_vadjustment().set_value(0);settle();p=out/(name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(p)],check=True);subprocess.run(['magick',str(p),str(p.with_suffix('.png'))],check=True);p.unlink()
def padding(widget):
 p=widget.get_style_context().get_padding();return [p.top,p.right,p.bottom,p.left]
def border(widget):
 b=widget.get_style_context().get_border();return [b.top,b.right,b.bottom,b.left]
def label_metrics(label,row):
 layout=label.get_layout();ink,logical=layout.get_pixel_extents();x,y=label.get_layout_offsets();font=layout.get_context().get_font_description();resolved=layout.get_context().load_font(font).describe().to_string()
 result=dict(text=label.get_text(),allocation=alloc(label),baseline=label.get_allocated_baseline(),layout_baseline=layout.get_baseline()/Pango.SCALE,offset=[x,y],ink=[ink.x,ink.y,ink.width,ink.height],logical=[logical.x,logical.y,logical.width,logical.height],font=font.to_string(),resolved=resolved,size=font.get_size()/Pango.SCALE,weight=int(font.get_weight()),bounds_in_row=bounds(label,row),padding=padding(label),margins=[label.get_style_context().get_margin().top,label.get_style_context().get_margin().right,label.get_style_context().get_margin().bottom,label.get_style_context().get_margin().left])
 parents=[];ancestor=label.get_parent()
 while ancestor is not None:
  parents.append({'node':ancestor.get_css_name(),'classes':list(ancestor.get_css_classes()),'content_clip_bounds':[0,0,ancestor.get_width(),ancestor.get_height()],'label_bounds':bounds(label,ancestor),'overflow':ancestor.get_overflow().value_nick})
  if ancestor==row:break
  ancestor=ancestor.get_parent()
 result['parent_clipping_bounds']=parents
 assert 'Plus Jakarta Sans' in resolved,resolved
 assert y+ink.y>=0 and y+ink.y+ink.height<=alloc(label)[1],result
 assert y+logical.y>=0 and y+logical.y+logical.height<=alloc(label)[1],result
 return result
measurements={};typography={};groups={};states={}
def measure_row(name,row):
 settle();header=box_of(row,'header');titlebox=box_of(header,'title');labels=[c for c in children(titlebox) if isinstance(c,Gtk.Label) and c.get_visible() and c.get_text()]
 measurements[name]=dict(allocation=alloc(row),header=alloc(header),padding=padding(row),border=border(row),titlebox=alloc(titlebox),labels=[label_metrics(c,row) for c in labels])
 assert padding(row)==[8,16,8,16],measurements[name]
 assert border(row)[2] in (0,1)
 if len(labels)==2:
  a,b=(bounds(c,titlebox) for c in labels);assert abs(b[1]-(a[1]+a[3])-4)<=.1,(name,a,b)
 for c in labels:
  if row.has_css_class('property'):continue
  expected=14 if c.has_css_class('title') else 12
  font=c.get_layout().get_context().get_font_description();expected*=1.5 if large else 1
  assert abs(font.get_size()/Pango.SCALE-expected)<.1,(name,font.to_string(),expected)
  assert int(font.get_weight())==(500 if c.has_css_class('title') else 400),(name,font.to_string())
 for c in labels:assert bounds(c,row)[1]>=0 and bounds(c,row)[1]+alloc(c)[1]<=alloc(row)[1]
 return measurements[name]
for name,row in [('single',single),('subtitle',two),('informational',passive),('interactive',interactive),('prefix-suffix',prefix),('property',prop)]:measure_row(name,row)
if large:assert alloc(two)[1]>=70,alloc(two)
if not large:
 assert alloc(single)[1]==48,alloc(single)
 assert 55<=alloc(two)[1]<=56,alloc(two)
 assert alloc(copy)[1]==32 and alloc(header_button)==[32,32]
assert alloc(suffix)==[40,22]
header=box_of(prefix,'header');titlebox=box_of(header,'title');suffixbox=box_of(header,'suffixes');icon=next(c for c in children(header) if c.get_css_name()=='image')
a,b,c=bounds(icon,header),bounds(titlebox,header),bounds(suffixbox,header)
assert b[0]-a[0]-a[2]==8,(a,b)
assert c[0]-b[0]-b[2]==16,(b,c)
assert tuple(v-8 for v in icon.measure(Gtk.Orientation.HORIZONTAL,-1)[:2])==(16,16),icon.measure(Gtk.Orientation.HORIZONTAL,-1)
assert abs(bounds(suffix,header)[1]+alloc(suffix)[1]/2-header.get_height()/2)<=1
for name,component in [('description',g),('heading-only',heading_only)]:
 inner=next(children(component));head=box_of(inner,'header');labelsbox=box_of(head,'labels');labels=[c for c in children(labelsbox) if c.get_visible()];boxed=next(c for c in nodes(component) if isinstance(c,Gtk.ListBox))
 groups[name]=dict(allocation=alloc(component),header=bounds(head,component),list=bounds(boxed,component),labels=[label_metrics(c,component) for c in labels])
 assert bounds(boxed,component)[1]-(bounds(head,component)[1]+alloc(head)[1])==8,groups[name]
 assert bounds(head,component)[0]==bounds(boxed,component)[0]
 for c in labels:
  font=c.get_layout().get_context().get_font_description();assert int(font.get_weight())==(600 if c.has_css_class('heading') else 400),font.to_string()
 if len(labels)==2:
  a,b=(bounds(c,labelsbox) for c in labels);assert b[1]-a[1]-a[3]==4,(a,b)
 text=render(boxed,name+'-group');assert re.search(r'outline: [^;]+ / 8;',text),text
 if name=='heading-only':
  heading_row.set_state_flags(Gtk.StateFlags.PRELIGHT,False);corner=render(boxed,'exterior-corner-hover');capture('group-exterior-corner-hover');heading_row.unset_state_flags(Gtk.StateFlags.PRELIGHT)
  assert len(re.findall(r'clip: [^;]+ / 7;',corner))>=2,corner

# Isolate the old broad label resets; record whether they change logical glyph bounds.
ablation={}
for declaration in ('min-height:0','padding:0','margin:0'):
 provider=Gtk.CssProvider();provider.load_from_data(('.boxed-list > row .title, .boxed-list > row .subtitle {'+declaration+';}').encode())
 Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,1000);settle()
 ablation[declaration]=measure_row('reset-'+declaration,two)
 Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),provider);settle()
(out/'label-reset-investigation.json').write_text(json.dumps(ablation,indent=2)+'\n')
# Capture a reconstructed old row geometry without editing rendered pixels.
old=Gtk.CssProvider();old.load_from_data(b'.boxed-list > row { min-height:33px; padding:8px 12px 8px 16px; } .boxed-list > row > box.header {min-height:0;} .boxed-list > row > box.header > box.title {border-spacing:3px;} .boxed-list > row > box.header > box.title > label.subtitle {margin-top:2px;}')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),old,1000);capture('before');Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),old);capture('after')
for name,row in [('informational',passive),('interactive',interactive)]:
 row.set_state_flags(Gtk.StateFlags.PRELIGHT,False);states[name+'-hover']=render(row,name+'-hover');capture('actionrow-'+name+'-hover');row.unset_state_flags(Gtk.StateFlags.PRELIGHT)
 row.set_state_flags(Gtk.StateFlags.ACTIVE,False);states[name+'-pressed']=render(row,name+'-pressed');row.unset_state_flags(Gtk.StateFlags.ACTIVE)
assert 'rgb(236,236,239)' not in states['informational-hover'] if variant=='light' else 'rgb(48,48,53)' not in states['informational-hover']
expected='rgb(236,236,239)' if variant=='light' else 'rgb(48,48,53)';assert expected in states['interactive-hover'],states['interactive-hover']
subprocess.run(['xdotool','key','Tab'],check=True);interactive.grab_focus();settle();subprocess.run(['xdotool','key','Return'],check=True);settle();settle();assert activated,('focus',w.get_focus(),interactive.get_focusable(),interactive.get_activatable())
focus=render(interactive,'interactive-focused');assert focus.count('widths: 2;')==1,focus
capture('actionrow-focused')
ok,rect=copy.compute_bounds(w);assert ok
subprocess.run(['xdotool','mousemove','--window',wid,str(int((rect.get_x()+rect.get_width()/2)*scale)),str(int((rect.get_y()+rect.get_height()/2)*scale)),'click','1'],check=True);settle();assert copied and not passive.get_activatable();assert two.get_subtitle_selectable()
Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL);g.set_direction(Gtk.TextDirection.RTL);settle()
header=box_of(prefix,'header');titlebox=box_of(header,'title');suffixbox=box_of(header,'suffixes');icon=next(c for c in children(header) if c.get_css_name()=='image')
a,b,c=bounds(icon,header),bounds(titlebox,header),bounds(suffixbox,header)
assert a[0]-b[0]-b[2]==8,(a,b)
assert b[0]-c[0]-c[2]==16,(b,c)
capture('prefix-suffix-rtl');Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR);g.set_direction(Gtk.TextDirection.LTR)

# Native subclass editing, selection, numeric adjustment, expansion and button activation.
for c in list(children(body)):body.remove(c)
g=group('General settings','Native subclasses retain their own layouts')
sw=Adw.SwitchRow(title='SwitchRow');g.add(sw)
combo=Adw.ComboRow(title='ComboRow',model=Gtk.StringList.new(['Standard','Compact']));g.add(combo)
spin=Adw.SpinRow.new_with_range(0,100,1);spin.set_title('SpinRow');g.add(spin)
entry=Adw.EntryRow(title='EntryRow');g.add(entry);password=Adw.PasswordEntryRow(title='PasswordEntryRow');g.add(password)
expander=Adw.ExpanderRow(title='ExpanderRow');nested=Adw.ActionRow(title='Nested information',subtitle='Native expansion');expander.add_row(nested);g.add(expander)
button=Adw.ButtonRow(title='ButtonRow');g.add(button);button_activated=[];button.connect('activated',lambda *_:button_activated.append(True))
suggested=Adw.ButtonRow(title='Suggested action');suggested.add_css_class('suggested-action');g.add(suggested)
destructive=Adw.ButtonRow(title='Destructive action');destructive.add_css_class('destructive-action');g.add(destructive)

settle();sw.grab_focus();subprocess.run(['xdotool','key','space'],check=True);settle();assert sw.get_active()
combo.set_selected(1);assert combo.get_selected()==1
spin.set_value(7);assert spin.get_value()==7
entry.set_text('Majoris');password.set_text('secret');assert entry.get_text()=='Majoris' and password.get_text()=='secret'
expander.set_expanded(True);settle();assert nested.get_mapped()
button.emit('activated');assert button_activated
capture('preference-subclasses');render(g,'subclass-group')
suggested.set_state_flags(Gtk.StateFlags.PRELIGHT,False);suggested_text=render(suggested,'buttonrow-suggested-hover');suggested.unset_state_flags(Gtk.StateFlags.PRELIGHT)
tokens=json.loads((root/'design'/('tokens-dark.json' if variant=='dark' else 'tokens.json')).read_text());color=tokens['semantic_color']['primary_hover'] if variant=='dark' else tokens['color']['primary_700'];rgb=tuple(bytes.fromhex(color.lstrip('#')))
assert 'rgb(%d,%d,%d)'%rgb in suggested_text,suggested_text

assert abs(entry.get_pango_context().get_font_description().get_size()/Pango.SCALE-(21 if large else 14))<.1
assert spin.get_allocated_height()<=56 if not large else True,alloc(spin)
# Realistic selectable glyph regression strings, multiline, narrow width and RTL.
for c in list(children(body)):body.remove(c)
g=group('Properties text rendering','No label height overrides; selectable native subtitles')
strings=['1.0 KiB (1028 bytes)','19 bytes','1 files, 0 folders','Plain text document','Home / Documents / Folder1','/etc/bluetooth/input.conf','Tue 03 Jun 2025 06:48:11 PM UTC','ABCDEFGHIJKLMNOPQRSTUVWXYZ','gjpqy','A multiline subtitle\nSecond line with gjpqy']
rows=[]
for i,text in enumerate(strings):rows.append(action(g,'Property '+str(i),text,subtitle_selectable=True,subtitle_lines=0))
settle()
for i,row in enumerate(rows):measure_row('text-'+str(i),row)
capture('long-subtitles');render(g,'text-rendering')
w.set_default_size(390,900);settle()
for i,row in enumerate(rows):measure_row('narrow-text-'+str(i),row)
capture('narrow-properties');Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL);g.set_direction(Gtk.TextDirection.RTL);settle();capture('rtl-properties');Gtk.Widget.set_default_direction(Gtk.TextDirection.LTR)
# No-heading, hidden and empty composition must not reserve a phantom header.
for c in list(children(body)):body.remove(c)
noheading=group();r=action(noheading,'No heading');hidden=action(noheading,'Hidden');hidden.set_visible(False)
empty=group();settle();assert not hidden.get_mapped();assert not empty.get_visible() or alloc(empty)[1]==0
capture('no-heading-hidden-rows')
# Real PreferencesPage owns the inter-group gap, without margins on each group.
prefpage=Adw.PreferencesPage();w.set_content(prefpage);w.set_default_size(760,900)
page_groups=[]
for title,description in [('Information','Selectable file properties'),('Open With',''),('Organisation','')]:
 component=Adw.PreferencesGroup(title=title,description=description);prefpage.add(component);page_groups.append(component)
for title,value in [('Type','Plain text document'),('Size','19 bytes'),('Location','Home / Documents'),('Modified','31 Oct 2026')]:
 r=Adw.ActionRow(title=title,subtitle=value,subtitle_selectable=True);r.add_css_class('property');page_groups[0].add(r)
change=Gtk.Button(label='Change…',valign=Gtk.Align.CENTER);r=Adw.ActionRow(title='Notepad',subtitle='Default application');r.add_suffix(change);r.set_activatable_widget(change);page_groups[1].add(r)
page_groups[2].add(Adw.SwitchRow(title='Favorite'))
settle();groups['page_composition']=[bounds(component,prefpage) for component in page_groups]
for a,b in zip(groups['page_composition'],groups['page_composition'][1:]):assert b[1]-a[1]-a[3]==16,(a,b)
capture('properties-dialog');render(prefpage,'properties-page')
# Dialog embedding uses the same native page/group controls.
dialog=Adw.PreferencesDialog(title='Properties');dialog.add(Adw.PreferencesPage(title='Properties'));dialog_group=Adw.PreferencesGroup(title='Information');dialog.get_visible_page().add(dialog_group);dialog_group.add(Adw.ActionRow(title='Size',subtitle='19 bytes',subtitle_selectable=True));dialog.present(w);capture('preferences-dialog');dialog.close()
(out/'actionrow-allocations.json').write_text(json.dumps(measurements,indent=2)+'\n')
(out/'preferences-group-geometry.json').write_text(json.dumps(groups,indent=2)+'\n')
(out/'interaction-states.json').write_text(json.dumps({'activation':bool(activated),'copy':bool(copied),'passive_activatable':passive.get_activatable(),'row_switch_activation':sw.get_active(),'entry':entry.get_text(),'password_editable':password.get_text()=='secret','expander':expander.get_expanded(),'button_activation':bool(button_activated),'hover_background':expected},indent=2)+'\n')
(out/'typography-metrics.json').write_text(json.dumps({name:item['labels'] for name,item in measurements.items()},indent=2)+'\n')
(out/'renderer-comparison.json').write_text(json.dumps({'actual_renderer':w.get_renderer().__class__.__name__,'requested_renderer':renderer,'scale':scale,'large_font':large,'geometry_and_ink_fit':True,'pixel_review_required':True},indent=2)+'\n')
w.destroy();print('Native preferences passed',variant,scale,renderer,large)
