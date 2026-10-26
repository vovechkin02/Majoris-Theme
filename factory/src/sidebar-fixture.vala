namespace MajorisThemeFactory {
    // A composition helper in the factory, not a new theme runtime/widget library.
    public class SidebarRow : Gtk.ListBoxRow {
        public Gtk.Label label;
        public Gtk.Image? icon;
        public Gtk.Label? badge;
        public string title;
        public SidebarRow(string text,string? icon_name=null,string? count=null,bool nested=false) {
            title=text; tooltip_text=text;
            var box=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);
            if(icon_name!=null) {icon=new Gtk.Image.from_icon_name(icon_name);icon.pixel_size=16;icon.valign=Gtk.Align.CENTER;icon.halign=Gtk.Align.CENTER;box.append(icon);}
            label=new Gtk.Label(text);label.xalign=0;label.hexpand=true;label.ellipsize=Pango.EllipsizeMode.END;label.valign=Gtk.Align.CENTER;box.append(label);
            if(count!=null) {badge=new Gtk.Label(count);badge.add_css_class("majoris-sidebar-badge");badge.valign=Gtk.Align.CENTER;box.append(badge);}
            child=box;
            if(nested)add_css_class("majoris-sidebar-child");
            update_property(Gtk.AccessibleProperty.LABEL,text,-1);
            if(count!=null)update_property(Gtk.AccessibleProperty.DESCRIPTION,"Count: "+count,-1);
        }
    }
    public class SidebarPage : Gtk.Box {
        public SidebarPage(Gtk.Application app) {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:16);
            add_css_class("majoris-page-content");
            var title=new Gtk.Label("Sidebar Design");title.xalign=0;title.add_css_class("title-1");append(title);
            var note=new Gtk.Label("32px rows, 4px gaps, optional symbolic icons and trailing counts. Open the native adaptive fixture for groups, scrolling and reveal/hide.");note.wrap=true;note.xalign=0;append(note);
            var open=new Gtk.Button.with_label("Open adaptive Sidebar Design");open.halign=Gtk.Align.START;open.clicked.connect(()=>new SidebarFixture(app).present());append(open);
            var previews=new Gtk.Box(Gtk.Orientation.HORIZONTAL,16);
            foreach(bool icons in new bool[]{false,true}) {
                var surface=new Gtk.Box(Gtk.Orientation.VERTICAL,0);surface.add_css_class("majoris-sidebar");surface.set_size_request(224,-1);surface.valign=Gtk.Align.START;
                var heading=new Gtk.Label(icons?"Icon navigation":"Plain navigation");heading.xalign=0;heading.add_css_class("majoris-sidebar-heading");surface.append(heading);
                var list=new Gtk.ListBox();list.selection_mode=Gtk.SelectionMode.SINGLE;
                foreach(var text in new string[]{"Home","Documents","Downloads","Shared Network Locations"})list.append(new SidebarRow(text,icons?"folder-symbolic":null,text=="Documents"?"12":null));
                list.select_row(list.get_row_at_index(0));surface.append(list);previews.append(surface);
            }
            append(previews);
        }
    }
    public class SidebarFixture : Adw.ApplicationWindow {
        public Adw.NavigationSplitView split;
        public Gtk.ListBox navigation;
        public Gtk.ListBox children;
        public Gtk.Expander group;
        Gtk.Box surface;
        Gtk.ScrolledWindow scroll;
        Gtk.Label current;
        Gtk.Button reveal_button;
        Gtk.Button forward_button;
        string selected_title="Home";
        public SidebarFixture(Gtk.Application app,string mode="sidebar") {
            Object(application:app,title:"Majoris Sidebar Design",default_width:900,default_height:650);
            split=new Adw.NavigationSplitView();split.min_sidebar_width=224;split.max_sidebar_width=320;split.sidebar_width_fraction=224.0/900.0;
            var sidebar_view=new Adw.ToolbarView();var sidebar_bar=new Adw.HeaderBar();sidebar_bar.show_back_button=false;sidebar_bar.title_widget=new Gtk.Label("Places");sidebar_view.add_top_bar(sidebar_bar);
            var forward=icon_button("go-next-symbolic","Show content");forward_button=forward;forward.clicked.connect(()=>split.show_content=true);sidebar_bar.pack_end(forward);split.bind_property("collapsed",forward,"visible",BindingFlags.SYNC_CREATE);
            surface=new Gtk.Box(Gtk.Orientation.VERTICAL,0);surface.add_css_class("majoris-sidebar");
            navigation=new Gtk.ListBox();navigation.selection_mode=Gtk.SelectionMode.SINGLE;
            string[] labels={"Home","Documents","Downloads","Recently Opened Files","Settings","Preferences","Network","A Very Long Shared Network Folder Name"};
            for(int i=0;i<labels.length;i++) {
                var row=new SidebarRow(labels[i],mode=="sidebar-basic"?null:(i==0?"user-home-symbolic":"folder-symbolic"),i==1?"12":(i==7?"3":null));
                if(i==5)row.sensitive=false;
                navigation.append(row);
            }
            navigation.set_header_func((row,before)=>{
                string text="";if(row.get_index()==0)text="Favorites";if(row.get_index()==4)text="Locations";if(row.get_index()==6)text="Network";
                if(text!=""){var heading=new Gtk.Label(text);heading.xalign=0;heading.add_css_class("majoris-sidebar-heading");row.set_header(heading);}else row.set_header(null);
            });
            surface.append(navigation);
            group=new Gtk.Expander(null);var group_title=new Gtk.Label("Devices");group_title.xalign=0;group_title.margin_start=8;group_title.add_css_class("majoris-sidebar-group-title");group.label_widget=group_title;group.add_css_class("majoris-sidebar-group");group.expanded=true;
            children=new Gtk.ListBox();children.selection_mode=Gtk.SelectionMode.SINGLE;
            children.append(new SidebarRow("Internal Drive","drive-harddisk-symbolic",null,true));children.append(new SidebarRow("External Storage Devices","drive-removable-media-symbolic",null,true));group.child=children;surface.append(group);
            if(mode=="sidebar-scroll") for(int i=0;i<30;i++)navigation.append(new SidebarRow("Shared location %d".printf(i+1),"folder-symbolic"));
            scroll=new Gtk.ScrolledWindow();scroll.hscrollbar_policy=Gtk.PolicyType.NEVER;scroll.overlay_scrolling=true;scroll.child=surface;sidebar_view.content=scroll;
            split.sidebar=new Adw.NavigationPage(sidebar_view,"Places");
            var content_view=new Adw.ToolbarView();var content_bar=new Adw.HeaderBar();content_bar.show_back_button=false;content_bar.pack_end(menu_button());
            var reveal=icon_button("sidebar-show-symbolic","Show navigation");reveal_button=reveal;reveal.clicked.connect(()=>split.show_content=false);content_bar.pack_start(reveal);split.bind_property("collapsed",reveal,"visible",BindingFlags.SYNC_CREATE);content_view.add_top_bar(content_bar);
            var body=new Gtk.Box(Gtk.Orientation.VERTICAL,16);body.add_css_class("majoris-page-content");
            current=new Gtk.Label(selected_title);current.xalign=0;current.wrap=true;current.add_css_class("title-1");body.append(current);
            var explanation=new Gtk.Label("Native selection, section headers and GtkExpander groups. Resize below 650px to switch pages; the header controls reveal navigation or content. Sidebar width is chosen by this fixture, not forced by CSS.");explanation.xalign=0;explanation.wrap=true;body.append(explanation);
            var toggle=new Gtk.Button.with_label("Expand / collapse Devices");toggle.halign=Gtk.Align.START;toggle.clicked.connect(()=>group.expanded=!group.expanded);body.append(toggle);
            var footer=new Gtk.Label("Selection persists while groups collapse and the window resizes.");footer.wrap=true;footer.xalign=0;footer.add_css_class("majoris-sidebar-description");body.append(footer);
            content_view.content=body;split.content=new Adw.NavigationPage(content_view,"Content");content=split;
            navigation.row_selected.connect((row)=>{if(row!=null){children.unselect_all();selected_title=((SidebarRow)row).title;current.label=selected_title;}});
            children.row_selected.connect((row)=>{if(row!=null){navigation.unselect_all();selected_title=((SidebarRow)row).title;current.label=selected_title;}});
            navigation.row_activated.connect((row)=>{row.grab_focus();split.show_content=true;});children.row_activated.connect((row)=>{row.grab_focus();split.show_content=true;});
            navigation.select_row(navigation.get_row_at_index(0));
            var breakpoint=new Adw.Breakpoint(Adw.BreakpointCondition.parse("max-width: 650px"));
            breakpoint.apply.connect(()=>change_layout(true));breakpoint.unapply.connect(()=>change_layout(false));add_breakpoint(breakpoint);
            if(mode=="sidebar-narrow" || mode=="sidebar-narrow-content") {set_default_size(390,650);split.show_content=mode=="sidebar-narrow-content";}
            if(mode=="sidebar-rtl")set_tree_direction(this,Gtk.TextDirection.RTL);
            var width=Environment.get_variable("MAJORIS_CONTENT_WIDTH");if(width!=null)set_default_size(int.parse(width),650);
            install_menu_actions(this);
            // The gallery's Files-menu placeholder accelerators must not consume
            // Space/Return before native disclosure/list activation in this window.
            ((SimpleAction)lookup_action("open")).set_enabled(false);
            ((SimpleAction)lookup_action("preview")).set_enabled(false);
            if(mode=="sidebar-states" || mode=="sidebar-focus")Timeout.add(500,()=>{
                var selected=navigation.get_row_at_index(0);selected.set_state_flags(Gtk.StateFlags.PRELIGHT,false);
                if(mode=="sidebar-states")navigation.get_row_at_index(1).set_state_flags(Gtk.StateFlags.ACTIVE,false);
                var focused=navigation.get_row_at_index(2);focused.grab_focus();focused.set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);navigation.select_row(selected);
                return Source.REMOVE;
            });
            if(mode=="sidebar-selected-pressed")Timeout.add(500,()=>{navigation.get_row_at_index(0).set_state_flags(Gtk.StateFlags.SELECTED|Gtk.StateFlags.ACTIVE,false);return Source.REMOVE;});
            if(mode=="sidebar-backdrop")Timeout.add(700,()=>{
                var target=new Adw.ApplicationWindow(app);target.title="Backdrop focus target";target.default_width=280;target.default_height=120;
                var view=new Adw.ToolbarView();view.add_top_bar(new Adw.HeaderBar());var note=new Gtk.Label("Native inactive-window check");note.wrap=true;view.content=note;target.content=view;target.present();return Source.REMOVE;
            });
            if(mode=="sidebar-scroll")Timeout.add(600,()=>{navigation.select_row(navigation.get_row_at_index(37));scroll.vadjustment.value=scroll.vadjustment.upper-scroll.vadjustment.page_size;return Source.REMOVE;});
            if(mode=="sidebar-large") {
                var attributes=new Pango.AttrList();attributes.insert(Pango.attr_scale_new(2.0));
                for(var row=navigation.get_first_child();row!=null;row=row.get_next_sibling()) {
                    var item=row as SidebarRow;if(item!=null)item.label.attributes=attributes;
                }
            }
            var report=Environment.get_variable("MAJORIS_SIDEBAR_REPORT");
            if(report!=null)Timeout.add(200,()=>{write_report(report);return Source.CONTINUE;});
        }
        void change_layout(bool collapsed) {
            // Native page reparenting restores focus; keep the application's
            // chosen navigation row authoritative across that focus restoration.
            var owner=navigation;var selected=owner.get_selected_row();
            if(selected==null){owner=children;selected=owner.get_selected_row();}
            split.collapsed=collapsed;
            if(selected!=null){owner.select_row(selected);if(!collapsed)selected.grab_focus();}
        }
        void set_tree_direction(Gtk.Widget widget,Gtk.TextDirection direction) {
            widget.set_direction(direction);
            if(widget is Gtk.Label)((Gtk.Label)widget).xalign=direction==Gtk.TextDirection.RTL?1:0;
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling())set_tree_direction(c,direction);
        }
        string bounds(Gtk.Widget widget) {
            Graphene.Rect rect;widget.compute_bounds(this,out rect);
            return "[%g,%g,%g,%g]".printf(rect.origin.x,rect.origin.y,rect.size.width,rect.size.height);
        }
        void write_report(string path) {
            var json=new StringBuilder("{");
            json.append("\"sidebar_width\":%d,\"collapsed\":%s,\"show_content\":%s,\"selected\":\"%s\",\"expanded\":%s,\"scroll\":%g,\"rows\":[".printf(split.sidebar.get_allocated_width(),split.collapsed.to_string(),split.show_content.to_string(),selected_title,group.expanded.to_string(),scroll.vadjustment.value));
            bool first=true;
            for(int i=0;i<8;i++) {
                var row=navigation.get_row_at_index(i) as SidebarRow;if(!first)json.append(",");first=false;
                var font=row.label.get_pango_context().get_font_description();Pango.Rectangle ink,logical;row.label.get_layout().get_pixel_extents(out ink,out logical);
                json.append("{\"title\":\"%s\",\"height\":%d,\"bounds\":%s,\"label\":%s,\"baseline\":%d,\"ink\":[%d,%d,%d,%d],\"font_size\":%g,\"weight\":%d,\"ellipsized\":%s,\"icon\":%s,\"badge\":%s}".printf(row.title,row.get_height(),bounds(row),bounds(row.label),row.label.get_layout().get_baseline()/Pango.SCALE,ink.x,ink.y,ink.width,ink.height,(double)font.get_size()/Pango.SCALE,(int)font.get_weight(),row.label.get_layout().is_ellipsized().to_string(),row.icon==null?"null":bounds(row.icon),row.badge==null?"null":bounds(row.badge)));
            }
            json.append("]");
            var focused=get_focus();
            bool group_focus=focused!=null && (focused==group || focused.is_ancestor(group));
            json.append(",\"group_focus\":%s,\"focus_type\":\"%s\"".printf(group_focus.to_string(),focused==null?"none":focused.get_type().name()));
            json.append(",\"group\":%s,\"group_title\":%s,\"reveal\":%s,\"forward\":%s".printf(bounds(group),bounds(group.label_widget),bounds(reveal_button),bounds(forward_button)));
            var selected=navigation.get_selected_row();if(selected==null)selected=children.get_selected_row();
            json.append(",\"selected_bounds\":%s}".printf(selected==null?"null":bounds(selected)));try{FileUtils.set_contents(path,json.str);}catch(Error e){warning("Sidebar report: %s",e.message);}
        }
    }
}
