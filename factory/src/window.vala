namespace MajorisThemeFactory {
    public class Window : Adw.ApplicationWindow {
        public FactoryPage gallery;
        public Gtk.Stack stack;
        public Gtk.StackSidebar sidebar;
        public Gtk.MenuButton main_menu;
        public Window (Gtk.Application app,string selected="overview") {
            Object (application: app, title: "Majoris Widget Factory", default_width: 1280, default_height: 960);
            var view = new Adw.ToolbarView ();
            var bar = new Adw.HeaderBar ();
            var back_button=icon_button ("go-previous-symbolic", "Back"); bar.pack_start(back_button);
            var forward_button=icon_button ("go-next-symbolic", "Forward"); bar.pack_start(forward_button);
            main_menu=menu_button(); bar.pack_end(main_menu);
            var view_button=icon_button("view-grid-symbolic","View"); view_button.add_css_class("flat"); bar.pack_end(view_button);
            var search_button=icon_button("system-search-symbolic","Search"); search_button.add_css_class("flat"); bar.pack_end(search_button);
            view.add_top_bar (bar);
            stack = new Gtk.Stack (); stack.hexpand = true;
            gallery = new FactoryPage (this);
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
            var states=new VisualStates(this); var state_scroll=new Gtk.ScrolledWindow(); state_scroll.child=states; stack.add_titled(state_scroll,"states","Visual States");
            var sb=new Gtk.Button.with_label("Open split/sidebar window"); sb.clicked.connect(()=>new SplitFixture(app).present()); headers.append(sb);
            var status = new Adw.StatusPage (); status.title = "No files found"; status.description = "Try a different search or clear the current filters."; status.icon_name = "system-search-symbolic";
            stack.add_titled (status,"status","Status");
            sidebar = new Gtk.StackSidebar (); sidebar.stack = stack; sidebar.add_css_class ("navigation-sidebar"); sidebar.set_size_request (212,-1);
            // Optional capture viewport: isolate available page width from navigation.
            var capture_width=Environment.get_variable("MAJORIS_CONTENT_WIDTH");
            if(capture_width!=null) {
                sidebar.visible=false;
                stack.hhomogeneous=false;
                if(int.parse(capture_width)<650) { back_button.visible=false; forward_button.visible=false; search_button.visible=false; view_button.visible=false; }
                set_default_size(int.parse(capture_width),960);
            }
            var split = new Gtk.Box (Gtk.Orientation.HORIZONTAL,0); split.append (sidebar); split.append (stack);
            var overlay = new Adw.ToastOverlay (); overlay.child = split; gallery.toast_overlay = overlay;
            view.content = overlay; content = view; install_menu_actions(this);
            if(selected.has_prefix("states-")) { var sc=new Gtk.ScrolledWindow(); sc.child=new VisualStates(this,selected.substring(7)); stack.add_titled(sc,"capture-states","Visual States"); stack.visible_child_name="capture-states"; }
            else if(selected=="scrolled") { stack.visible_child_name="widgets"; Timeout.add(700,()=>{scroll.vadjustment.value=scroll.vadjustment.upper-scroll.vadjustment.page_size;return Source.REMOVE;}); }
            else if(selected=="status" || selected=="states" || selected=="headerbars") stack.visible_child_name=selected;
            else if(selected!="overview") { var capture=new FactoryPage(this,selected=="dialog"?"menus":(selected=="tooltip"?"buttons":selected)); capture.toast_overlay=overlay; var sc=new Gtk.ScrolledWindow(); sc.child=capture; stack.add_titled(sc,"capture",selected); stack.visible_child_name="capture"; if(selected=="feedback") Timeout.add(700,()=>{capture.show_toast();return Source.REMOVE;}); if(selected=="dialog") Timeout.add(700,()=>{capture.show_dialog();return Source.REMOVE;}); if(selected=="menus") Timeout.add(700,()=>{ main_menu.get_popover().autohide=false; main_menu.active=true; main_menu.get_popover().popup(); main_menu.get_popover().present(); Timeout.add(300,()=>{main_menu.get_popover().queue_draw();return Source.REMOVE;});return Source.REMOVE;}); }
            var action = new SimpleAction ("new", null); action.activate.connect (() => new Window(app).present()); add_action (action);
            var del = new SimpleAction ("delete", null); del.activate.connect (() => { var toast = new Adw.Toast ("Example action activated"); overlay.add_toast(toast); }); add_action (del);
        }
    }
}
