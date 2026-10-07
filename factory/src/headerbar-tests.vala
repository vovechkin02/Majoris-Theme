namespace MajorisThemeFactory {
    public void install_menu_actions (Gtk.ApplicationWindow window) {
        foreach (var name in new string[]{"open","rename","duplicate","trash"}) {
            var action=new SimpleAction(name,null); action.activate.connect(()=>{}); window.add_action(action);
        }
    }
    public Gtk.Button icon_button (string icon, string tooltip) {
        var b = new Gtk.Button.from_icon_name (icon);
        b.tooltip_text = tooltip;
        b.valign = Gtk.Align.CENTER;
        return b;
    }
    public Gtk.MenuButton menu_button () {
        var model = new Menu ();
        model.append ("Open", "win.open"); model.append ("Rename", "win.rename"); model.append ("Duplicate", "win.duplicate");
        var section = new Menu (); var item=new MenuItem("Move to Trash",null); item.set_attribute_value("custom",new Variant.string("trash")); section.append_item(item); model.append_section(null,section);
        var popover=new Gtk.PopoverMenu.from_model(model);
        var trash=new Gtk.Button.with_label("Move to Trash"); trash.add_css_class("majoris-menu-danger"); trash.action_name="win.trash";
        popover.add_child(trash,"trash");
        var b = new Gtk.MenuButton (); b.icon_name = "open-menu-symbolic";
        b.popover=popover; b.valign = Gtk.Align.CENTER; b.add_css_class("flat");        return b;
    }
    public class HeaderFixture : Adw.ApplicationWindow {
        public Adw.HeaderBar bar;
        public Gtk.MenuButton menu;
        public Gtk.Button? search;
        public Gtk.Entry? location;
        public Gtk.Button? back;
        public Gtk.DropDown? dropdown;
        public HeaderFixture (Gtk.Application app, bool dense) {
            Object (application: app, title: dense ? "Dense / Files" : "Simple / Clock", default_width: dense ? 900 : 420, default_height: 220);
            bar = new Adw.HeaderBar ();
            var view = new Adw.ToolbarView (); view.add_top_bar (bar);
            view.content = new Gtk.Label (dense ? "Dense headerbar geometry fixture" : "Simple headerbar geometry fixture");
            content = view;
            menu = menu_button (); bar.pack_end (menu);
            if (dense) {
                back=icon_button ("go-previous-symbolic", "Back"); bar.pack_start(back);
                bar.pack_start (icon_button ("go-next-symbolic", "Forward"));
                location = new Gtk.Entry (); location.text = "/home/majoris/Documents";
                location.valign = Gtk.Align.CENTER; location.hexpand = true;
                bar.title_widget = location;
                search = icon_button ("system-search-symbolic", "Search"); search.add_css_class("flat"); bar.pack_end (search);
                var view_button=icon_button ("view-grid-symbolic", "View"); view_button.add_css_class("flat"); bar.pack_end(view_button);
                dropdown = new Gtk.DropDown.from_strings ({"Name", "Modified"}); dropdown.valign = Gtk.Align.CENTER; bar.pack_end (dropdown);
            }
            var action = new SimpleAction ("new", null); action.activate.connect (() => new HeaderFixture (app, dense).present ()); add_action (action);
            install_menu_actions(this);
            var del = new SimpleAction ("delete", null); del.activate.connect (() => {}); add_action (del);
        }
    }
    public class SplitFixture : Adw.ApplicationWindow {
        public Adw.HeaderBar sidebar_bar;
        public Adw.HeaderBar content_bar;
        public SplitFixture (Gtk.Application app) {
            Object(application:app,title:"Split / Sidebar",default_width:900,default_height:300);
            var box=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);
            var left=new Adw.ToolbarView(); left.set_size_request(212,-1); left.add_css_class("majoris-split-sidebar");
            sidebar_bar=new Adw.HeaderBar(); sidebar_bar.show_end_title_buttons=false; sidebar_bar.show_start_title_buttons=false;
            sidebar_bar.title_widget=new Gtk.Label("Places"); left.add_top_bar(sidebar_bar);
            var sidebar=new Gtk.ListBox(); sidebar.add_css_class("majoris-sidebar"); sidebar.append(new Gtk.Label("Documents")); sidebar.append(new Gtk.Label("Downloads")); sidebar.select_row(sidebar.get_row_at_index(0)); left.content=sidebar;
            var right=new Adw.ToolbarView(); right.hexpand=true;
            content_bar=new Adw.HeaderBar(); content_bar.pack_start(icon_button("go-previous-symbolic","Back")); content_bar.pack_end(menu_button()); right.add_top_bar(content_bar); right.content=new Gtk.Label("Content surface");
            box.append(left); box.append(right); content=box; install_menu_actions(this);
        }
    }
}
