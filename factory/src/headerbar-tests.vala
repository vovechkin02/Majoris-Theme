namespace MajorisThemeFactory {
    public Gtk.Button icon_button (string icon, string tooltip) {
        var b = new Gtk.Button.from_icon_name (icon);
        b.tooltip_text = tooltip;
        b.valign = Gtk.Align.CENTER;
        return b;
    }
    public Gtk.MenuButton menu_button () {
        var model = new Menu ();
        model.append ("New window", "win.new");
        var section = new Menu (); section.append ("Delete example", "win.delete");
        model.append_section (null, section);
        var b = new Gtk.MenuButton (); b.icon_name = "open-menu-symbolic";
        b.menu_model = model; b.valign = Gtk.Align.CENTER;
        return b;
    }
    public class HeaderFixture : Adw.ApplicationWindow {
        public Adw.HeaderBar bar;
        public Gtk.MenuButton menu;
        public Gtk.Button? search;
        public Gtk.Entry? location;
        public HeaderFixture (Gtk.Application app, bool dense) {
            Object (application: app, title: dense ? "Dense / Files" : "Simple / Clock", default_width: dense ? 900 : 420, default_height: 220);
            bar = new Adw.HeaderBar ();
            var view = new Adw.ToolbarView (); view.add_top_bar (bar);
            view.content = new Gtk.Label (dense ? "Dense headerbar geometry fixture" : "Simple headerbar geometry fixture");
            content = view;
            menu = menu_button (); bar.pack_end (menu);
            if (dense) {
                bar.pack_start (icon_button ("go-previous-symbolic", "Back"));
                bar.pack_start (icon_button ("go-next-symbolic", "Forward"));
                location = new Gtk.Entry (); location.text = "/home/majoris/Documents";
                location.valign = Gtk.Align.CENTER; location.hexpand = true;
                bar.title_widget = location;
                search = icon_button ("system-search-symbolic", "Search"); bar.pack_end (search);
                bar.pack_end (icon_button ("view-grid-symbolic", "View"));
                var drop = new Gtk.DropDown.from_strings ({"Name", "Modified"}); drop.valign = Gtk.Align.CENTER; bar.pack_end (drop);
            }
            var action = new SimpleAction ("new", null); action.activate.connect (() => new HeaderFixture (app, dense).present ()); add_action (action);
            var del = new SimpleAction ("delete", null); del.activate.connect (() => {}); add_action (del);
        }
    }
}
