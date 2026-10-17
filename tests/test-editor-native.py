"""Realized GTK4 editor geometry, native state stability and document operations."""
import ctypes, json, os, gi, subprocess
from pathlib import Path
gi.require_version('Gtk','4.0');gi.require_version('Adw','1');gi.require_version('GtkSource','5')
from gi.repository import Gtk, Adw, GtkSource, GLib, Gio
root=Path(__file__).resolve().parents[1]
os.environ['MAJORIS_THEME_ROOT']=str(root/'theme/Majoris')
os.environ['GTK_A11Y']='none'
Adw.init();ctypes.CDLL(str(root/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
manager=Adw.StyleManager.get_default()
schemes=GtkSource.StyleSchemeManager.get_default();schemes.append_search_path(str(root/'theme/Majoris/gtksourceview-5/styles'))
w=Adw.Window();w.set_default_size(900,600)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
tabs=Adw.TabView(vexpand=True)
bar=Adw.TabBar(view=tabs,autohide=False,expand_tabs=False);bar.add_css_class('majoris-document-tabs');box.append(bar)
toolbar=Gtk.Box(spacing=4);toolbar.add_css_class('majoris-editor-toolbar')
button=Gtk.ToggleButton(icon_name='format-text-bold-symbolic',valign=Gtk.Align.CENTER);toolbar.append(button)
menu=Gtk.MenuButton(label='More',valign=Gtk.Align.CENTER);menu.set_popover(Gtk.Popover(child=Gtk.Label(label='Menu content')));toolbar.append(menu)
box.append(toolbar)
buffer=GtkSource.Buffer();buffer.set_language(GtkSource.LanguageManager.get_default().get_language('vala'));buffer.set_text('public class Document : Object { string title = "Majoris"; }')
source=GtkSource.View(buffer=buffer,monospace=True,show_line_numbers=True,highlight_current_line=True)
scroll=Gtk.ScrolledWindow(child=source)
page=tabs.append(scroll);page.set_title('source.vala');page.set_icon(Gio.ThemedIcon.new('text-x-generic-symbolic'))
for name in ('short.txt','a-long-filename-with-many-characters.md','Unsaved document'):
 p=tabs.append(Gtk.Label(label='Document'));p.set_title(name)
p.set_needs_attention(True);p.set_indicator_icon(Gio.ThemedIcon.new('document-save-symbolic'))
box.append(tabs)
status=Gtk.Box(spacing=4);status.add_css_class('majoris-statusbar');status.append(Gtk.Label(label='Ln 1, Col 1',hexpand=True,xalign=0))
status_menu=Gtk.MenuButton(label='UTF-8',valign=Gtk.Align.CENTER);status_menu.set_popover(Gtk.Popover(child=Gtk.Label(label='UTF-8')));status.append(status_menu);box.append(status)
w.set_content(box);w.present()
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(150,lambda:(loop.quit(),False)[1]);loop.run()
def nodes(x):
 yield x
 c=x.get_first_child()
 while c:
  yield from nodes(c);c=c.get_next_sibling()
def allocation(x):return [x.get_allocated_width(),x.get_allocated_height()]
def geometry():
 return {name:allocation(x) for name,x in [('bar',bar),('toolbar',toolbar),('action',button),('status',status),('status-control',status_menu.get_first_child())]}
results=[]
try:
 for variant in ('light','dark','light'):
  manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
  buffer.set_style_scheme(schemes.get_scheme('majoris-'+variant));settle()
  found=[x for x in nodes(bar) if x.get_css_name()=='tab']
  assert found and any(x.get_state_flags() & Gtk.StateFlags.SELECTED for x in found)
  assert [bar.get_allocated_height(),toolbar.get_allocated_height(),button.get_allocated_height(),status.get_allocated_height(),status_menu.get_first_child().get_allocated_height()]==[38,40,28,34,28],geometry()
  initial=geometry()
  for flag in (Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,Gtk.StateFlags.INSENSITIVE,Gtk.StateFlags.SELECTED,Gtk.StateFlags.BACKDROP):
   held=[(x,x.get_state_flags()) for x in (found[0],button,status_menu.get_first_child())]
   for x,original in held:x.set_state_flags(flag,False)
   settle();assert geometry()==initial,(flag,geometry(),initial)
   for x,original in held:x.set_state_flags(original,True)
  button.set_active(True);settle();assert geometry()==initial
  assert buffer.get_style_scheme().get_id()=='majoris-'+variant
  assert source.get_pango_context().get_font_description().get_family()=='monospace'
  for language in ('vala','python','markdown','diff','xml'):
   buffer.set_language(GtkSource.LanguageManager.get_default().get_language(language))
   buffer.ensure_highlight(buffer.get_start_iter(),buffer.get_end_iter())
  results.append({'variant':variant,'scale':int(os.environ.get('GDK_SCALE','1')),'geometry':initial,'source-font':source.get_pango_context().get_font_description().to_string()})
 # A generic theme appearance change must not replace an explicitly selected third-party scheme.
 buffer.set_style_scheme(schemes.get_scheme('classic'))
 manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK);settle()
 assert buffer.get_style_scheme().get_id()=='classic'
 # Exercise native operations; CSS must not substitute custom tab behavior.
 tabs.set_page_pinned(page,True);assert tabs.get_n_pinned_pages()==1
 last=tabs.get_nth_page(3);assert tabs.reorder_page(last,1)
 assert tabs.get_nth_page(1)==last
 tabs.set_selected_page(last);assert tabs.get_selected_page()==last
 tabs.close_page(last);assert tabs.get_n_pages()==3
 for i in range(20):
  extra=tabs.append(Gtk.Label(label='Overflow'));extra.set_title('Long filename %d with spaces.vala'%i)
 w.set_default_size(390,600);settle();assert bar.get_is_overflowing()
 assert bar.get_allocated_height()==38
finally:w.destroy()
(root/('artifacts/editor-native-2x.json' if os.environ.get('GDK_SCALE')=='2' else 'artifacts/editor-native.json')).write_text(json.dumps(results,indent=2)+'\n')
print('Native editor geometry, state stability, switching, pin/reorder/close and overflow passed')

# Exercise the actual Vala fixture's shared app.scheme action and notification bridge.
probe=subprocess.run([str(root/'build/factory/majoris-theme-factory'),'--page=editor','--light'],env={**os.environ,'MAJORIS_EDITOR_SWITCH_PROBE':'1'},capture_output=True,text=True,check=True,timeout=10)
assert 'CRITICAL' not in probe.stderr and 'Theme parser error' not in probe.stderr,probe.stderr
switches=[json.loads(line) for line in probe.stdout.splitlines() if line.startswith('{')]
assert [item['mode'] for item in switches]==['light','dark','light'],switches
for item in switches:
 assert set(item['schemes'])=={'majoris-'+item['mode']},item
 assert (item['tab_height'],item['toolbar_height'],item['status_height'])==(38,40,34),item
(root/('artifacts/editor-factory-switching-2x.json' if os.environ.get('GDK_SCALE')=='2' else 'artifacts/editor-factory-switching.json')).write_text(json.dumps(switches,indent=2)+'\n')
print('Actual factory app.scheme light/dark/light action updates every SourceView buffer')
