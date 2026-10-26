namespace MajorisThemeFactory {
    public class GeometryReport {
        static string allocation (Gtk.Widget? w) {
            if(w==null) return "{\"available\":false,\"reason\":\"CSS node is not exposed as GtkWidget\"}";
            return "{\"width\":%d,\"height\":%d}".printf (w.get_allocated_width (), w.get_allocated_height ());
        }
        static void collect (Gtk.Widget w, StringBuilder b, ref bool first) {
            if (w is Gtk.WindowControls || (w is Gtk.Button && w.get_parent () is Gtk.WindowControls) || (w is Gtk.Image && w.get_parent () is Gtk.Button && w.get_parent ().get_parent () is Gtk.WindowControls)) {
                if (!first) b.append (","); first = false;
                b.append ("{\"type\":\"%s\",\"css\":\"%s\",\"classes\":\"%s\",\"width\":%d,\"height\":%d}".printf (w.get_type ().name (), w.get_css_name (), string.joinv (" ", w.get_css_classes ()), w.get_allocated_width (), w.get_allocated_height ()));
            }
            for (var c = w.get_first_child (); c != null; c = c.get_next_sibling ()) collect (c, b, ref first);
        }
        static string controls (Gtk.Widget w) {
            var b = new StringBuilder ("["); bool first = true; collect (w,b,ref first); b.append ("]"); return b.str;
        }
        public static Gtk.Widget? find_node(Gtk.Widget widget,string css_name) {
            if(widget.get_css_name()==css_name && widget.get_allocated_width()>0)return widget;
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling()){var found=find_node(c,css_name);if(found!=null)return found;}
            return null;
        }
        static string header(Gtk.Widget widget) {
            return "{\"content_height\":%d,\"allocation_height\":%d,\"divider\":1,\"painted_height\":%d,\"width\":%d}".printf(widget.get_height(),widget.get_allocated_height(),widget.get_allocated_height(),widget.get_allocated_width());
        }
        static string keyed_controls(Gtk.Widget widget) {
            var b=new StringBuilder("{"); bool first=true;
            foreach(var name in new string[]{"minimize","maximize","close"}) {
                var button=find_class(widget,name);
                if(button!=null) { if(!first)b.append(","); first=false; var image=find_node(button,"image"); b.append("\"%s\":{\"width\":%d,\"height\":%d,\"glyph\":%s}".printf(name,button.get_allocated_width(),button.get_allocated_height(),allocation(image))); }
            }
            b.append("}"); return b.str;
        }
        static Gtk.Widget? find_class(Gtk.Widget widget,string css_class) {
            if(widget.has_css_class(css_class) && widget is Gtk.Button)return widget;
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling()){var found=find_class(c,css_class);if(found!=null)return found;}return null;
        }
        static void tree(Gtk.Widget widget,StringBuilder b,ref bool first) {
            if(!first)b.append(","); first=false;
            b.append("{\"type\":\"%s\",\"css\":\"%s\",\"classes\":\"%s\",\"width\":%d,\"height\":%d}".printf(widget.get_type().name(),widget.get_css_name(),string.joinv(" ",widget.get_css_classes()),widget.get_allocated_width(),widget.get_allocated_height()));
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling())tree(c,b,ref first);
        }
        public static void print (HeaderFixture simple, HeaderFixture dense, SplitFixture split,Window main) {
            var context=main.gallery.get_first_child().get_pango_context();
            var font=context.load_font(context.get_font_description());
            stdout.printf("{\"resolved_pango_font\":\"%s\",",font.describe().to_string());
            stdout.printf("\"simple_headerbar\":%s,\"dense_headerbar\":%s,\"split_sidebar_headerbar\":%s,\"split_content_headerbar\":%s,\"simple_window_controls\":%s,\"dense_window_controls\":%s,",header(simple.bar),header(dense.bar),header(split.sidebar_bar),header(split.content_bar),keyed_controls(simple.bar),keyed_controls(dense.bar));
            foreach(var key in new string[]{"normal_icon_button","flat_icon_button","entry","dropdown","switch","switch_off","hidden_banner"}) stdout.printf("\"%s\":%s,",key,allocation(main.gallery.probes.lookup(key)));
            stdout.printf("\"main_sidebar\":%s,",allocation(main.sidebar));
            var notebook=(Gtk.Notebook)main.gallery.probes.lookup("notebook"); var tab_label=notebook.get_tab_label(notebook.get_nth_page(0));
            stdout.printf("\"tab\":{\"css_node_exposed\":false,\"label\":%s},\"view_switcher_button\":%s,",allocation(tab_label),allocation(find_node(main.gallery.probes.lookup("view_switcher"),"button")));
            stdout.printf("\"windowcontrols_simple\":%s,\"windowcontrols_dense\":%s,",controls(simple.bar),controls(dense.bar));
            var b=new StringBuilder("[");bool first=true;tree(main,b,ref first);b.append("]");stdout.printf("\"widget_tree\":%s}\n",b.str);
        }
        public static void dump(Gtk.Widget widget) { var b=new StringBuilder("[");bool first=true;tree(widget,b,ref first);b.append("]");stdout.printf("%s\n",b.str); }
    }
}
