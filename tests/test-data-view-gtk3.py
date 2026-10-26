"""Native GTK3 TreeView metrics, sort, density and IconView captures."""
import gi,sys,os,importlib.util,json,subprocess,time
from pathlib import Path
from PIL import Image
gi.require_version('Gtk','3.0');gi.require_version('GdkX11','3.0')
from gi.repository import Gtk,Gdk,GdkX11,GLib,Pango
root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('fixture',root/'tools/gtk3-data-fixture.py');fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture)
wm=subprocess.Popen(['openbox'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(250,lambda:(loop.quit(),False)[1]);loop.run()
reports=[]
try:
 for variant in ('light','dark'):
  provider=Gtk.CssProvider();provider.load_from_path(str(root/'theme/Majoris/gtk-3.0'/('gtk-dark.css' if variant=='dark' else 'gtk.css')));Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER+1)
  for compact in (False,True):
   for family in ("column","list","grid"):
    grid=family=="grid"
    window=Gtk.Window(title='Majoris GTK3 Data Views');window.set_default_size(900,600);view,model=fixture.build(compact,grid,family=="list");scroll=Gtk.ScrolledWindow();scroll.add(view);window.add(scroll);window.show_all();settle()
    font=view.get_pango_context().get_font_description();assert round(font.get_size()/Pango.SCALE*96/72)==14 and int(font.get_weight())==500,font.to_string()
    d={'variant':variant,'compact':compact,'family':family,'grid':grid,'font':font.to_string()}
    if not grid:
     heights=[view.get_background_area(Gtk.TreePath.new_from_indices([i]),view.get_column(0)).height for i in range(5)]
     assert heights==[32 if compact else 40]*5,heights
     headers=[c.get_button().get_allocated_height() for c in view.get_columns()]
     if family=='column':assert headers==[32]*3,headers
     headerfont=view.get_column(0).get_button().get_pango_context().get_font_description()
     if family=='column':assert int(headerfont.get_weight())==600 and round(headerfont.get_size()/Pango.SCALE*96/72)==12,headerfont.to_string()
     for text in ('Favorites','Files','Folders','Find','Format','Documents','Downloads','Properties','gjpqy','ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
      ink,logical=view.create_pango_layout(text).get_pixel_extents();assert ink.y>=0 and ink.y+ink.height<=logical.height
     model.set_sort_column_id(0,Gtk.SortType.DESCENDING);settle();assert model[0][0]!='Documents'
     d|={'rows':heights,'headers':headers,'header_font':headerfont.to_string()}
    window.present();subprocess.run(['xdotool','mousemove','0','0'],check=True);settle();assert window.get_window().is_viewable()
    out=root/'artifacts/data-view-finalisation/gtk3';out.mkdir(parents=True,exist_ok=True);name=f"{family}-{'compact' if compact else 'standard'}-{variant}-{os.environ.get('GDK_SCALE','1')}x";xwd=out/(name+'.xwd');png=xwd.with_suffix('.png');subprocess.run(['xwd','-silent','-screen','-root','-out',str(xwd)],check=True);subprocess.run(['magick',str(xwd),str(png)],check=True)
    # Real selected pixels catch GTK3 :focus specificity overriding item colour.
    if grid:
     path=Gtk.TreePath.new_from_indices([1]);ok,area=view.get_cell_rect(path,None);assert ok
     native_window=view.get_window()
    else:
     selected_model,paths=view.get_selection().get_selected_rows();assert len(paths)==1
     area=view.get_background_area(paths[0],view.get_column(0));native_window=view.get_bin_window()
    geometry=subprocess.check_output(['xdotool','getwindowgeometry','--shell',str(native_window.get_xid())],text=True)
    values=dict(line.split('=',1) for line in geometry.splitlines() if '=' in line);scale=int(os.environ.get('GDK_SCALE','1'))
    origin=native_window.get_origin();ox,oy=origin[-2:]
    px=round((ox+area.x+area.width-10)*scale);py=round((oy+area.y+area.height/2)*scale)
    actual=Image.open(png).convert('RGB').getpixel((px,py));expected=(238,242,255) if variant=='light' else (43,43,68)
    assert max(abs(a-b) for a,b in zip(actual,expected))<=2,(family,variant,actual,expected,(area.x,area.y,area.width,area.height),(px,py),values)
    d['selected_pixel']=actual
    reports.append(d);window.destroy();settle()
  Gtk.StyleContext.remove_provider_for_screen(Gdk.Screen.get_default(),provider)
finally:wm.terminate();wm.wait(timeout=5)
(root/'artifacts/data-view-finalisation/geometry'/f"gtk3-{os.environ.get('GDK_SCALE','1')}x.json").write_text(json.dumps(reports,indent=2)+'\n')
print('GTK3 standard/compact TreeView rows, headers, typography, sorting, IconView and native captures passed')
