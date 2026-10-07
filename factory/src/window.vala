namespace MajorisThemeFactory {
    public class Window : Adw.ApplicationWindow {
        public Window (Gtk.Application app) {
            Object (application: app, title: "Majoris Widget Factory", default_width: 1180, default_height: 860);
            var view = new Adw.ToolbarView ();
            var bar = new Adw.HeaderBar ();
            bar.pack_start (icon_button ("go-previous-symbolic", "Back"));
            bar.pack_start (icon_button ("go-next-symbolic", "Forward"));
            bar.pack_end (menu_button ());
            bar.pack_end (icon_button ("view-grid-symbolic", "View"));
            bar.pack_end (icon_button ("system-search-symbolic", "Search"));
            view.add_top_bar (bar);
            var stack = new Gtk.Stack (); stack.hexpand = true;
            var gallery = new FactoryPage (this);
            var scroll = new Gtk.ScrolledWindow (); scroll.child = gallery;
            stack.add_titled (scroll, "widgets", "Widgets");
            var headers = new Gtk.Box (Gtk.Orientation.VERTICAL, 16);
            headers.margin_top = 24; headers.margin_start = 24; headers.margin_end = 24;
            headers.append (new Gtk.Label ("Native headerbars: hover, focus, maximize and restore both fixtures."));
            foreach (bool dense in new bool[] {false,true}) {
                var button = new Gtk.Button.with_label (dense ? "Open dense / Files-style window" : "Open simple / Clock-style window");
                button.clicked.connect (() => new HeaderFixture (app,dense).present ()); headers.append (button);
            }
            stack.add_titled (headers,"headerbars","Headerbars");
            var status = new Adw.StatusPage (); status.title = "Everything is up to date"; status.description = "Native status, tooltip and scrolling checks"; status.icon_name = "emblem-ok-symbolic";
            stack.add_titled (status,"status","Status");
            var sidebar = new Gtk.StackSidebar (); sidebar.stack = stack; sidebar.add_css_class ("navigation-sidebar"); sidebar.set_size_request (212,-1);
            var split = new Gtk.Box (Gtk.Orientation.HORIZONTAL,0); split.append (sidebar); split.append (stack);
            var overlay = new Adw.ToastOverlay (); overlay.child = split; gallery.toast_overlay = overlay;
            view.content = overlay; content = view;
            var action = new SimpleAction ("new", null); action.activate.connect (() => new Window(app).present()); add_action (action);
            var del = new SimpleAction ("delete", null); del.activate.connect (() => { var toast = new Adw.Toast ("Example action activated"); overlay.add_toast(toast); }); add_action (del);
        }
    }
}
