namespace MajorisThemeFactory {
    [CCode (cname = "majoris_theme_attach")]
    public extern static void attach_theme ();
    public class Application : Adw.Application {
        bool report;
        string page;
        string variant;
        public Application (bool geometry,string selected="overview",string scheme="light") {
            Object (application_id: "com.majoris.ThemeFactory", flags: ApplicationFlags.NON_UNIQUE);
            report = geometry;
            page=selected;
            variant=scheme;
        }
        protected override void activate () {
            var style = Adw.StyleManager.get_default ();
            style.color_scheme = variant=="dark" ? Adw.ColorScheme.FORCE_DARK : (variant=="system" ? Adw.ColorScheme.DEFAULT : Adw.ColorScheme.FORCE_LIGHT);
            attach_theme ();
            var scheme_action = new SimpleAction.stateful ("scheme", VariantType.STRING, new Variant.string (variant));
            scheme_action.activate.connect ((value) => {
                string mode=value.get_string ();
                style.color_scheme=mode=="dark" ? Adw.ColorScheme.FORCE_DARK : (mode=="system" ? Adw.ColorScheme.DEFAULT : Adw.ColorScheme.FORCE_LIGHT);
                scheme_action.set_state (value);
            });
            add_action (scheme_action);
            Gtk.Settings.get_default ().gtk_decoration_layout = ":minimize,maximize,close";
            Gtk.Settings.get_default ().gtk_icon_theme_name = "Majoris";
            if(Environment.get_variable("MAJORIS_CAPTURE")=="1") Gtk.Settings.get_default().gtk_enable_animations=false;
            set_accels_for_action("win.cut",{"<Control>x"}); set_accels_for_action("win.copy",{"<Control>c"}); set_accels_for_action("win.paste",{"<Control>v"}); set_accels_for_action("win.properties",{"<Alt>Return"}); set_accels_for_action("win.trash",{"Delete"});
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
            } else if(page.has_prefix("location")) new LocationFixture(this,page).present();
            else if(page.has_prefix("editor")) new EditorFixture(this,page).present();
            else if(page=="simple") new HeaderFixture(this,false).present();
            else if(page=="dense") new HeaderFixture(this,true).present();
            else if(page=="split") new SplitFixture(this).present();
            else if(page.has_prefix("window-edge")) new WindowEdgeFixture(this,page=="window-edge"?"floating":page.substring(12)).present();
            else new Window (this,page).present ();
            if(Environment.get_variable("MAJORIS_TREE")=="1") Timeout.add(1500,()=>{foreach(var w in get_windows())GeometryReport.dump(w);quit();return Source.REMOVE;});
        }
    }
}
