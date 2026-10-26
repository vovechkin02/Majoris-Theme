"""Native first-visible section spacing, including mutations, GTK3/GTK4."""
import gi,sys,os,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];version=sys.argv[1]
gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk,Gdk,GLib
if version=='4':
 gi.require_version('Adw','1');from gi.repository import Adw
 Adw.init()
else:Gtk.init([])
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(160,lambda:(loop.quit(),False)[1]);loop.run()
def cls(w,c):w.get_style_context().add_class(c)
def style(w,name):
 ctx=w.get_style_context();return getattr(ctx,'get_'+name)() if version=='4' else getattr(ctx,'get_'+name)(w.get_state_flags())
def y(w,parent):
 if version=='4':return round(w.compute_bounds(parent)[1].get_y())+style(parent,'padding').top
 return w.translate_coordinates(parent,0,0)[1]+style(w,'margin').top
baseline=os.environ.get('MAJORIS_PADDING_BASELINE')=='1';reports=[]
for variant in ('light','dark'):
 provider=Gtk.CssProvider();provider.load_from_path(str(root/f'theme/Majoris/gtk-{version}.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')))
 if version=='4':
  Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1);window=Gtk.Window()
 else:
  Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1);window=Gtk.Window()
 surface=Gtk.Box(orientation=Gtk.Orientation.VERTICAL);cls(surface,'majoris-sidebar');surface.set_size_request(224,-1)
 listing=Gtk.ListBox();rows=[]
 def headers(row,before):
  text=getattr(row,'section',None)
  if text:
   label=Gtk.Label(label=text,xalign=0);cls(label,'majoris-sidebar-heading')
   if before is None:cls(label,'majoris-sidebar-heading-first')
   row.set_header(label)
  else:row.set_header(None)
 listing.set_header_func(headers)
 for i in range(6):
  row=Gtk.ListBoxRow();row.section=('Favorites','Locations','Network')[i//2] if i%2==0 else None
  label=Gtk.Label(label='Navigation '+str(i),xalign=0)
  if version=='4':row.set_child(label);listing.append(row)
  else:row.add(label);listing.add(row)
  rows.append(row)
 if version=='4':surface.append(listing);window.set_child(surface);window.present()
 else:surface.pack_start(listing,False,True,0);window.add(surface);window.show_all()
 settle()
 def check(stage,first):
  listing.invalidate_headers();settle()
  heading=first.get_header();margin=style(heading,'margin');padding=style(heading,'padding');outer=style(surface,'padding')
  expected=32 if baseline else 16
  measured=y(heading,surface)
  assert measured==expected,(version,variant,stage,measured,expected)
  assert margin.top==(16 if baseline else 0) and margin.bottom==8
  assert (padding.left,padding.right)==(8,8) and (outer.top,outer.bottom,outer.left,outer.right)==(16,16,8,8)
  for row in rows:
   if row.get_parent() is None or not row.get_visible():continue
   h=row.get_header()
   if h is not None and row!=first:assert style(h,'margin').top==16 and style(h,'margin').bottom==8
   assert style(row,'margin').bottom==4
   height=row.get_height() if version=='4' else row.get_allocated_height()-style(row,'margin').top-style(row,'margin').bottom
   assert height==32,(version,stage,height)
  visible=[r for r in rows if r.get_parent() is not None and r.get_visible()]
  for index,row in enumerate(visible[:-1]):
   following=visible[index+1]
   if following.get_header() is None:assert y(following,surface)-y(row,surface)==36
  reports.append(dict(gtk=version,variant=variant,stage=stage,scale=int(os.environ.get('GDK_SCALE','1')),top=measured,first_margin=margin.top,later_margin=16,bottom_margin=8,row_height=32,row_gap=4))
 check('initial',rows[0])
 for row in rows[:2]:row.hide()
 check('first section hidden',rows[2])
 for row in rows[:2]:listing.remove(row)
 check('first section removed',rows[2])
 # Move the last group ahead of the existing first group using public APIs.
 for i,row in enumerate(rows[4:]):listing.remove(row);listing.insert(row,i)
 check('sections reordered',rows[4])
 for row in rows[4:]:row.hide()
 check('reordered first hidden',rows[2])
 for row in rows[2:4]:row.section=None
 listing.invalidate_headers();settle()
 assert rows[2].get_header() is None
 listing.queue_resize();settle()
 assert y(rows[2],surface)==16,(version,variant,'direct row',y(rows[2],surface))
 if version=='4':window.destroy()
 else:window.destroy()
 settle()
 Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),provider) if version=='4' else Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),provider)
out=root/'artifacts/sidebar-padding/geometry';out.mkdir(parents=True,exist_ok=True)
(out/f"{'before' if baseline else 'after'}-gtk{version}-{os.environ.get('GDK_SCALE','1')}x.json").write_text(json.dumps(reports,indent=2)+'\n')
print(f'GTK{version}: first heading {reports[0]["top"]}px, later margins 16px; visibility/removal/reorder/direct rows passed')
