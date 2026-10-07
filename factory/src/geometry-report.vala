namespace MajorisThemeFactory {
    public class GeometryReport {
        static string allocation (Gtk.Widget w) {
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
        public static void print (HeaderFixture simple, HeaderFixture dense) {
            stdout.printf ("{\"headerbar_simple\":%s,\"headerbar_dense\":%s,\"windowcontrols_simple\":%s,\"windowcontrols_dense\":%s,\"menu_button\":%s,\"search_button\":%s,\"location_entry\":%s}\n", allocation (simple.bar), allocation (dense.bar), controls (simple.bar), controls (dense.bar), allocation (simple.menu), allocation (dense.search), allocation (dense.location));
        }
    }
}
