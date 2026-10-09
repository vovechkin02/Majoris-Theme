namespace MajorisThemeFactory {
    // Real native window and header; every appearance comes from global CSS.
    public class WindowEdgeFixture : Adw.ApplicationWindow {
        public Adw.HeaderBar bar;
        public WindowEdgeFixture (Gtk.Application app, string state) {
            Object(application:app,title:"Majoris window edge / "+state,default_width:640,default_height:360);
            bar=new Adw.HeaderBar();
            var view=new Adw.ToolbarView();view.add_top_bar(bar);
            var box=new Gtk.Box(Gtk.Orientation.VERTICAL,16);
            box.halign=Gtk.Align.CENTER;box.valign=Gtk.Align.CENTER;
            box.append(new Gtk.Label("Global CSD edge: "+state));
            box.append(new Gtk.Label("Floating: 8px corners, 1px edge and window shadow"));
            box.append(new Gtk.Label("Managed: square corners, no reserved outer inset"));
            view.content=box;content=view;
            if (state=="maximized") maximize();
            else if(state=="fullscreen") fullscreen();
            else if(state.has_prefix("tiled")) add_css_class(state);
            Timeout.add(1200,()=>{
                stdout.printf("edge-state=%s maximized=%s fullscreen=%s header=%d\n",state,is_maximized().to_string(),is_fullscreen().to_string(),bar.get_allocated_height());
                stdout.printf("classes=%s\n",string.joinv(" ",get_css_classes()));
                dump_controls(bar); stdout.flush();
                return Source.REMOVE;
            });
        }
        void dump_controls(Gtk.Widget widget) {
            if(widget is Gtk.WindowControls) {
                for(var button=widget.get_first_child();button!=null;button=button.get_next_sibling()) {
                    if(!(button is Gtk.Button)) continue;
                    var image=((Gtk.Button)button).child as Gtk.Image;
                    stdout.printf("control=%s plate=%dx%d glyph=%dx%d\n",image==null?"?":image.icon_name,button.get_allocated_width(),button.get_allocated_height(),image==null?0:image.get_allocated_width(),image==null?0:image.get_allocated_height());
                }
            }
            for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling()) dump_controls(child);
        }
    }
}
