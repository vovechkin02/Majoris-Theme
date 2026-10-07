namespace MajorisThemeFactory {
    public class Application : Adw.Application {
        bool report;
        public Application (bool geometry) {
            Object (application_id: "com.majoris.ThemeFactory", flags: ApplicationFlags.NON_UNIQUE);
            report = geometry;
        }
        protected override void activate () {
            Adw.StyleManager.get_default ().color_scheme = Adw.ColorScheme.FORCE_LIGHT;
            Gtk.Settings.get_default ().gtk_decoration_layout = ":minimize,maximize,close";
            Gtk.Settings.get_default ().gtk_icon_theme_name = "Majoris";
            set_accels_for_action ("win.new", {"<Control>n"});
            if (report) {
                var simple = new HeaderFixture (this, false);
                var dense = new HeaderFixture (this, true);
                simple.present (); dense.present ();
                Timeout.add (1200, () => {
                    GeometryReport.print (simple, dense);
                    simple.close (); dense.close (); quit (); return Source.REMOVE;
                });
            } else new Window (this).present ();
        }
    }
}
