namespace MajorisThemeFactory {
    public class Application : Adw.Application {
        bool report;
        string page;
        public Application (bool geometry,string selected="overview") {
            Object (application_id: "com.majoris.ThemeFactory", flags: ApplicationFlags.NON_UNIQUE);
            report = geometry;
            page=selected;
        }
        protected override void activate () {
            Adw.StyleManager.get_default ().color_scheme = Adw.ColorScheme.FORCE_LIGHT;
            Gtk.Settings.get_default ().gtk_decoration_layout = ":minimize,maximize,close";
            Gtk.Settings.get_default ().gtk_icon_theme_name = "Majoris";
            if(Environment.get_variable("MAJORIS_CAPTURE")=="1") Gtk.Settings.get_default().gtk_enable_animations=false;
            set_accels_for_action ("win.new", {"<Control>n"});
            set_accels_for_action ("win.open", {"Return"}); set_accels_for_action("win.rename",{"F2"});
            if (report) {
                var simple = new HeaderFixture (this, false);
                var dense = new HeaderFixture (this, true);
                var split=new SplitFixture(this); var main=new Window(this);
                simple.present (); dense.present (); split.present(); main.present();
                Timeout.add (1200, () => {
                    GeometryReport.print (simple, dense,split,main);
                    simple.close (); dense.close (); split.close(); main.close(); quit (); return Source.REMOVE;
                });
            } else if(page=="simple") new HeaderFixture(this,false).present();
            else if(page=="dense") new HeaderFixture(this,true).present();
            else if(page=="split") new SplitFixture(this).present();
            else new Window (this,page).present ();
            if(Environment.get_variable("MAJORIS_TREE")=="1") Timeout.add(1500,()=>{foreach(var w in get_windows())GeometryReport.dump(w);quit();return Source.REMOVE;});
        }
    }
}
