"""Native GTK3 equivalents; renderer padding is application-owned."""
import gi,sys,os,json
from pathlib import Path
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk,GdkPixbuf,Pango,GLib
root=Path(__file__).resolve().parents[1]
Gtk.IconTheme.get_default().append_search_path(str(root/'icons'))
Gtk.Settings.get_default().set_property('gtk-icon-theme-name','Majoris')
def build(compact=False,grid=False,list_mode=False):
 model=Gtk.ListStore(str,str,int)
 for i,name in enumerate(('Documents','Downloads','Photos','Majoris Design.md','Majoris-Theme-Implementation-Notes.txt','A Very Long Filename That Exceeds The Available View Width.txt','Wallpaper.png','Project Requirements.pdf','gjpqy','ABCDEFGHIJKLMNOPQRSTUVWXYZ')):model.append([name,'Folder' if i<3 else 'Document',(i+1)*1024])
 if grid:
  view=Gtk.IconView.new();view.set_model(model);view.get_style_context().add_class('majoris-data-grid');view.set_item_width(80 if compact else 112);view.set_item_padding(8);view.set_margin(8 if compact else 16);view.set_column_spacing(8 if compact else 16);view.set_row_spacing(8 if compact else 16);view.set_spacing(8)
  icon=Gtk.CellRendererPixbuf();info=Gtk.IconTheme.get_default().lookup_icon('folder-symbolic',32 if compact else 64,Gtk.IconLookupFlags.FORCE_SIZE);pixbuf,symbolic=info.load_symbolic_for_context(view.get_style_context());icon.set_property('pixbuf',pixbuf);icon.set_fixed_size(64 if compact else 96,64 if compact else 96);view.pack_start(icon,False)
  text=Gtk.CellRendererText();text.set_property('wrap-width',80 if compact else 112);text.set_property('wrap-mode',Pango.WrapMode.WORD_CHAR);text.set_property('ellipsize',Pango.EllipsizeMode.END);text.set_property('alignment',Pango.Alignment.CENTER);view.pack_start(text,False);view.add_attribute(text,'text',0);view.set_selection_mode(Gtk.SelectionMode.MULTIPLE);view.select_path(Gtk.TreePath.new_from_indices([1]));return view,model
 view=Gtk.TreeView(model=model);view.get_style_context().add_class('majoris-data-list' if list_mode else 'majoris-data-view');view.set_grid_lines(Gtk.TreeViewGridLines.NONE if list_mode else Gtk.TreeViewGridLines.HORIZONTAL);view.set_headers_visible(not list_mode)
 if compact:view.get_style_context().add_class('majoris-density-compact')
 view.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE);view.get_selection().select_path(1)
 for i,title in enumerate(('Name','Type','Size')):
  text=Gtk.CellRendererText();text.set_property('ypad',4 if compact else 8);text.set_property('xpad',0);text.set_property('ellipsize',Pango.EllipsizeMode.END)
  col=Gtk.TreeViewColumn(title)
  if i==0:
   icon=Gtk.CellRendererPixbuf();icon.set_property('icon-name','folder-symbolic');icon.set_property('stock-size',Gtk.IconSize.SMALL_TOOLBAR);col.pack_start(icon,False);col.set_spacing(8)
  col.pack_start(text,True);col.add_attribute(text,'text',i);col.set_resizable(True);col.set_sort_column_id(i);col.set_min_width((192,128,96)[i]);col.set_expand(i==0);view.append_column(col)
 return view,model
if __name__=='__main__':
 variant=os.environ.get('MAJORIS_VARIANT','light');provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')));Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1)
 window=Gtk.Window(title='Majoris GTK3 Data Views');window.set_default_size(900,600);view,model=build('--compact' in sys.argv,'--grid' in sys.argv,'--list' in sys.argv);scroll=Gtk.ScrolledWindow();scroll.add(view);window.add(scroll);window.connect('destroy',Gtk.main_quit);window.show_all();Gtk.main()
