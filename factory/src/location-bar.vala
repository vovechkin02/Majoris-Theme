namespace MajorisThemeFactory {
    // Simulated absolute paths: application code owns real filesystem validation.
    public class LocationBar : Gtk.Box {
        public string path { get; private set; default = "/home/demo/Documents"; }
        public bool editing { get; private set; default = false; }
        public Gtk.Entry entry;
        public Gtk.Box crumbs;
        public Gtk.ScrolledWindow viewport;
        Gtk.Stack modes;
        string[] history = {"/home/demo/Documents"};
        int position = 0;
        public signal void navigated();
        public bool can_back { get { return position > 0; } }
        public bool can_forward { get { return position + 1 < history.length; } }
        public LocationBar() {
            Object(orientation:Gtk.Orientation.HORIZONTAL,spacing:0,hexpand:true,valign:Gtk.Align.CENTER);
            add_css_class("majoris-location-bar");
            modes=new Gtk.Stack(); modes.hexpand=true; modes.hhomogeneous=false;
            crumbs=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);
            var scroll=new Gtk.ScrolledWindow(); viewport=scroll; scroll.hscrollbar_policy=Gtk.PolicyType.EXTERNAL;
            scroll.vscrollbar_policy=Gtk.PolicyType.NEVER; scroll.hexpand=true;
            var trail_viewport=new Gtk.Viewport(null,null);trail_viewport.hscroll_policy=Gtk.ScrollablePolicy.NATURAL;trail_viewport.scroll_to_focus=true;trail_viewport.child=crumbs;scroll.child=trail_viewport;
            double previous_upper=-1,previous_page=-1;
            scroll.add_tick_callback((widget,clock)=>{
                var adjustment=scroll.hadjustment;
                if(adjustment.upper!=previous_upper || adjustment.page_size!=previous_page) {
                    previous_upper=adjustment.upper;previous_page=adjustment.page_size;
                    adjustment.value=get_direction()==Gtk.TextDirection.RTL?0:double.max(0,adjustment.upper-adjustment.page_size);
                }
                return Source.CONTINUE;
            });
            var normal=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0); normal.append(scroll);
            // Separate native button: crumb clicks never bubble into an edit gesture.
            var empty=new Gtk.Button(); empty.add_css_class("majoris-location-crumb");
            empty.set_size_request(48,-1); empty.hexpand=false; empty.tooltip_text="Edit location (Ctrl+L or Alt+D)";
            empty.update_property(Gtk.AccessibleProperty.LABEL,"Edit location",-1);
            empty.clicked.connect(begin_edit); normal.append(empty);
            modes.add_named(normal,"crumbs");
            entry=new Gtk.Entry(); entry.hexpand=true; entry.add_css_class("majoris-location-entry");
            entry.update_property(Gtk.AccessibleProperty.LABEL,"Full folder path",-1);
            entry.activate.connect(()=>{if(navigate(entry.text))end_edit();else {entry.add_css_class("error");entry.tooltip_text="Enter an absolute path without parent traversal";}});
            var focus=new Gtk.EventControllerFocus(); focus.leave.connect(()=>end_edit()); entry.add_controller(focus);
            var cancel=new Gtk.EventControllerKey();cancel.key_pressed.connect((key,code,mods)=>{if(key==Gdk.Key.Escape){end_edit();return true;}return false;});entry.add_controller(cancel);
            modes.add_named(entry,"entry"); append(modes); rebuild();
            var background=new Gtk.GestureClick();
            background.pressed.connect((n,x,y)=>{
                if(editing)return;
                var picked=pick(x,y,Gtk.PickFlags.DEFAULT);
                for(var node=picked;node!=null && node!=this;node=node.get_parent())if(node is Gtk.Button)return;
                begin_edit();
            });add_controller(background);
        }
        public void show_editing() {
            editing=true; entry.text=path; add_css_class("majoris-location-editing"); modes.visible_child_name="entry";
        }
        public void begin_edit() {
            editing=true; entry.text=path; entry.remove_css_class("error"); entry.tooltip_text=null;
            add_css_class("majoris-location-editing"); modes.visible_child_name="entry";
            entry.grab_focus(); entry.select_region(0,-1);
        }
        public void end_edit() {
            if(!editing)return;
            editing=false; remove_css_class("majoris-location-editing"); modes.visible_child_name="crumbs";
        }
        public bool navigate(owned string target) {
            target=target.strip();
            if(!target.has_prefix("/") || target.contains("\n") || target.contains("/../") || target.has_suffix("/.."))return false;
            target=Filename.canonicalize(target,"/");
            end_edit();
            if(target!=path) {
                history=history[0:position+1]; history+=target; position++;
                path=target; rebuild(); navigated();
            }
            return true;
        }
        public void back() { if(can_back){end_edit();path=history[--position];rebuild();navigated();} }
        public void forward() { if(can_forward){end_edit();path=history[++position];rebuild();navigated();} }
        public void up() { navigate(Path.get_dirname(path)); }
        public void home() { navigate("/home/demo"); }
        void rebuild() {
            for(var c=crumbs.get_first_child();c!=null;c=crumbs.get_first_child())crumbs.remove(c);
            add_crumb("Computer","/"); string accumulated="";
            foreach(var part in path.split("/")) {
                if(part=="")continue;
                var separator=new Gtk.Label(get_direction()==Gtk.TextDirection.RTL?"‹":"›");separator.add_css_class("majoris-location-separator");crumbs.append(separator);
                accumulated+="/"+part; add_crumb(part,accumulated);
            }
        }
        void add_crumb(string title,string target) {
            var button=new Gtk.Button(); var label=new Gtk.Label(title); label.ellipsize=Pango.EllipsizeMode.END; label.max_width_chars=24;
            button.child=label; button.tooltip_text=target;button.add_css_class("majoris-location-crumb");
            if(target==path)button.add_css_class("majoris-location-current");
            button.clicked.connect(()=>navigate(target)); crumbs.append(button);
        }
    }
    public class LocationFixture : Adw.ApplicationWindow {
        public LocationBar location;
        public Gtk.SearchEntry search;
        public Majoris.Ui.Toolbar toolbar;
        public LocationFixture(Gtk.Application app,string mode="location") {
            Object(application:app,title:"Majoris Files Components",default_width:900,default_height:650);
            var chrome=new Adw.ToolbarView();var header=new Adw.HeaderBar();header.pack_end(menu_button());chrome.add_top_bar(header);
            var layout=new Gtk.Box(Gtk.Orientation.VERTICAL,12);
            var documents=new Adw.TabView();documents.vexpand=true;
            var tabs=new Adw.TabBar();tabs.view=documents;tabs.autohide=false;tabs.add_css_class("majoris-document-tabs");layout.append(tabs);
            toolbar=new Majoris.Ui.Toolbar();
            var back=icon_button("go-previous-symbolic","Back");var forward=icon_button("go-next-symbolic","Forward");
            var up=icon_button("go-up-symbolic","Up");var home=icon_button("go-home-symbolic","Home");
            toolbar.append_control(back);toolbar.append_control(forward);toolbar.append_control(up);toolbar.append_control(home);
            location=new LocationBar();toolbar.append_widget(location);
            search=new Gtk.SearchEntry();search.placeholder_text="Search files";search.width_request=180;
            toolbar.append_control(search);layout.append(toolbar);
            back.clicked.connect(location.back);forward.clicked.connect(location.forward);up.clicked.connect(location.up);home.clicked.connect(location.home);
            var current=new Gtk.Label(location.path);current.wrap=true;
            location.navigated.connect(()=>{back.sensitive=location.can_back;forward.sensitive=location.can_forward;up.sensitive=location.path!="/";current.label=location.path;});
            back.sensitive=false;forward.sensitive=false;
            var page=documents.append(current);page.title="Files";
            page=documents.append(new Gtk.Label("Native second tab — application navigation is simulated"));page.title="Downloads";
            layout.append(documents);
            var note=new Gtk.Label("Click a folder or the empty end of the pill. Ctrl+L / Alt+D edits; Enter accepts an absolute simulated path; Escape or clicking outside cancels.");note.wrap=true;layout.append(note);
            var states=new Gtk.Box(Gtk.Orientation.VERTICAL,8);states.margin_start=12;states.margin_end=12;
            string[] names={"Default","Hover","Pressed","Keyboard focus","Disabled","Long path","High contrast","Editing","Backdrop"};
            for(int i=0;i<names.length;i++) {
                var row=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);var title=new Gtk.Label(names[i]);title.width_chars=16;title.xalign=0;row.append(title);
                var sample=new LocationBar();row.append(sample);states.append(row);
                if(i==4)sample.sensitive=false;
                if(i==5)sample.navigate("/home/demo/Documents/Projects/A very long folder name/Design/References/Archive");
                if(i==6)sample.add_css_class("majoris-high-contrast");
                if(i==7)sample.show_editing();
                Gtk.StateFlags flag=i==1?Gtk.StateFlags.PRELIGHT:(i==2?Gtk.StateFlags.ACTIVE:(i==3?Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE:(i==8?Gtk.StateFlags.BACKDROP:Gtk.StateFlags.NORMAL)));
                var crumb=sample.crumbs.get_first_child();
                Timeout.add(350,()=>{crumb.set_state_flags(flag,false);if(flag==Gtk.StateFlags.BACKDROP)sample.set_state_flags(flag,false);return Source.REMOVE;});
            }
            var scrolled=new Gtk.ScrolledWindow();scrolled.vexpand=true;scrolled.child=states;layout.append(scrolled);
            var keys=new Gtk.EventControllerKey();keys.propagation_phase=Gtk.PropagationPhase.CAPTURE;
            keys.key_pressed.connect((key,code,mods)=>{
                if(((mods&Gdk.ModifierType.CONTROL_MASK)!=0 && (key==Gdk.Key.l || key==Gdk.Key.L)) || ((mods&Gdk.ModifierType.ALT_MASK)!=0 && (key==Gdk.Key.d || key==Gdk.Key.D))){location.begin_edit();return true;}
                if(key==Gdk.Key.Escape && location.editing){location.end_edit();location.grab_focus();return true;}return false;
            });((Gtk.Widget)this).add_controller(keys);
            var outside=new Gtk.GestureClick();outside.propagation_phase=Gtk.PropagationPhase.CAPTURE;
            outside.pressed.connect((n,x,y)=>{var picked=pick(x,y,Gtk.PickFlags.DEFAULT);if(picked!=null && picked!=location && !picked.is_ancestor(location))location.end_edit();});((Gtk.Widget)this).add_controller(outside);
            chrome.content=layout;content=chrome;install_menu_actions(this);
            // Placeholder gallery actions must not consume Return/Space while editing paths.
            var open_action=lookup_action("open") as SimpleAction;if(open_action!=null)open_action.set_enabled(false);
            var preview_action=lookup_action("preview") as SimpleAction;if(preview_action!=null)preview_action.set_enabled(false);
            var width=Environment.get_variable("MAJORIS_CONTENT_WIDTH");if(width!=null)set_default_size(int.parse(width),650);
            if(mode.contains("rtl")){set_direction(Gtk.TextDirection.RTL);location.set_direction(Gtk.TextDirection.RTL);location.navigate("/home/demo/Downloads");}
            if(mode.contains("long"))location.navigate("/home/demo/Documents/Projects/A Very Long Folder Name With Multiple Words/References/Archive");
            if(mode.contains("large"))Timeout.add(500,()=>{enlarge_text(location);enlarge_text(search);return Source.REMOVE;});
            var report=Environment.get_variable("MAJORIS_LOCATION_REPORT");
            if(report!=null)Timeout.add(200,()=>{write_location_report(report);return Source.CONTINUE;});
            if(mode=="location-editing")Timeout.add(500,()=>{location.begin_edit();return Source.REMOVE;});
        }
        void enlarge_text(Gtk.Widget widget) {
            if(widget is Gtk.Label){var attrs=new Pango.AttrList();attrs.insert(Pango.attr_scale_new(2.0));((Gtk.Label)widget).attributes=attrs;}
            if(widget is Gtk.Text){var attrs=new Pango.AttrList();attrs.insert(Pango.attr_scale_new(2.0));((Gtk.Text)widget).attributes=attrs;}
            for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling())enlarge_text(child);
        }
        string rect(Gtk.Widget widget){Graphene.Rect r;widget.compute_bounds(this,out r);return "[%g,%g,%g,%g]".printf(r.origin.x,r.origin.y,r.size.width,r.size.height);}
        string quote(string value){return "\""+value.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n")+"\"";}
        void describe_node(Gtk.Widget widget,StringBuilder json,ref bool first) {
            if(!widget.get_mapped())return;
            if(!first)json.append(",");first=false;
            var context=widget.get_style_context();var border=context.get_border();var padding=context.get_padding();
            json.append("{\"node\":%s,\"classes\":%s,\"bounds\":%s,\"border\":[%d,%d,%d,%d],\"padding\":[%d,%d,%d,%d],\"flags\":%u".printf(quote(widget.get_css_name()),quote(string.joinv(" ",widget.get_css_classes())),rect(widget),border.top,border.right,border.bottom,border.left,padding.top,padding.right,padding.bottom,padding.left,(uint)widget.get_state_flags()));
            if(widget is Gtk.Label || widget is Gtk.Text) {
                Pango.Layout layout;int ox=0,oy=0;
                if(widget is Gtk.Label){layout=((Gtk.Label)widget).get_layout();((Gtk.Label)widget).get_layout_offsets(out ox,out oy);}else {layout=widget.create_pango_layout(((Gtk.Text)widget).text);layout.set_attributes(((Gtk.Text)widget).attributes);}
                var font=widget.get_pango_context().get_font_description();Pango.Rectangle ink,logical;layout.get_pixel_extents(out ink,out logical);
                json.append(",\"layout_source\":%s,\"text\":%s,\"font\":%s,\"size\":%g,\"weight\":%d,\"ink\":[%d,%d,%d,%d],\"logical\":[%d,%d,%d,%d],\"layout_offset\":[%d,%d],\"baseline\":%g".printf(quote((widget is Gtk.Label) ? "GtkLabel layout":"GtkText contextual metric layout"),quote(layout.get_text()),quote(font.to_string()),(double)font.get_size()/Pango.SCALE,(int)font.get_weight(),ink.x,ink.y,ink.width,ink.height,logical.x,logical.y,logical.width,logical.height,ox,oy,(double)layout.get_baseline()/Pango.SCALE));
            }
            json.append("}");
            for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling())describe_node(child,json,ref first);
        }
        void render_nodes(Gsk.RenderNode node,StringBuilder json,ref bool first) {
            if(!first)json.append(",");first=false;
            var bounds=node.get_bounds();
            json.append("{\"type\":%s,\"bounds\":[%g,%g,%g,%g]".printf(quote(node.get_node_type().to_string()),bounds.origin.x,bounds.origin.y,bounds.size.width,bounds.size.height));
            unowned Gsk.RoundedRect? outline=null;
            if(node is Gsk.BorderNode){var border=(Gsk.BorderNode)node;outline=border.get_outline();json.append(",\"color\":%s".printf(quote(border.get_colors().to_string())));var widths=border.get_widths();json.append(",\"widths\":[%g,%g,%g,%g]".printf(widths[0],widths[1],widths[2],widths[3]));}
            if(node is Gsk.RoundedClipNode)outline=((Gsk.RoundedClipNode)node).get_clip();
            if(node is Gsk.OutsetShadowNode){var shadow=(Gsk.OutsetShadowNode)node;outline=shadow.get_outline();json.append(",\"blur\":%g,\"spread\":%g,\"dx\":%g,\"dy\":%g,\"color\":%s".printf(shadow.get_blur_radius(),shadow.get_spread(),shadow.get_dx(),shadow.get_dy(),quote(shadow.get_color().to_string())));}
            if(node is Gsk.InsetShadowNode){var shadow=(Gsk.InsetShadowNode)node;outline=shadow.get_outline();json.append(",\"blur\":%g,\"spread\":%g,\"dx\":%g,\"dy\":%g,\"color\":%s".printf(shadow.get_blur_radius(),shadow.get_spread(),shadow.get_dx(),shadow.get_dy(),quote(shadow.get_color().to_string())));}
            if(node is Gsk.ColorNode)json.append(",\"color\":%s".printf(quote(((Gsk.ColorNode)node).get_color().to_string())));
            if(outline!=null)json.append(",\"radius\":[%g,%g,%g,%g]".printf(outline.corner[0].width,outline.corner[1].width,outline.corner[2].width,outline.corner[3].width));
            json.append("}");
            if(node is Gsk.ContainerNode){var container=(Gsk.ContainerNode)node;for(uint i=0;i<container.get_n_children();i++)render_nodes(container.get_child(i),json,ref first);}
            if(node is Gsk.TransformNode)render_nodes(((Gsk.TransformNode)node).get_child(),json,ref first);
            if(node is Gsk.ClipNode)render_nodes(((Gsk.ClipNode)node).get_child(),json,ref first);
            if(node is Gsk.RoundedClipNode)render_nodes(((Gsk.RoundedClipNode)node).get_child(),json,ref first);
            if(node is Gsk.OpacityNode)render_nodes(((Gsk.OpacityNode)node).get_child(),json,ref first);
        }
        string render_report(Gtk.Widget widget) {
            if(!widget.get_mapped())return "[]";
            var snapshot=new Gtk.Snapshot();var paintable=new Gtk.WidgetPaintable(widget);
            paintable.snapshot(snapshot,paintable.get_intrinsic_width(),paintable.get_intrinsic_height());
            var node=snapshot.to_node();var json=new StringBuilder("[");bool first=true;
            if(node!=null)render_nodes(node,json,ref first);json.append("]");return json.str;
        }
        void save_toolbar_snapshot() {
            var target=Environment.get_variable("MAJORIS_LOCATION_SNAPSHOT");if(target==null)return;
            var snapshot=new Gtk.Snapshot();var paintable=new Gtk.WidgetPaintable(toolbar);
            paintable.snapshot(snapshot,paintable.get_intrinsic_width(),paintable.get_intrinsic_height());
            var node=snapshot.to_node();if(node==null)return;
            var texture=get_native().get_renderer().render_texture(node,node.get_bounds());texture.save_to_png(target);
        }
        void write_location_report(string path) {
            var json=new StringBuilder("{\"location\":%s,\"search\":%s,\"toolbar\":%s,\"entry\":%s,\"path\":%s,\"editing\":%s,\"scale\":%d,\"nodes\":[".printf(rect(location),rect(search),rect(toolbar),rect(location.entry),quote(location.path),location.editing.to_string(),get_scale_factor()));
            bool first=true;describe_node(toolbar,json,ref first);
            json.append("],\"render_location\":%s,\"render_search\":%s,\"render_entry\":%s}".printf(render_report(location),render_report(search),render_report(location.entry)));
            save_toolbar_snapshot();
            try{FileUtils.set_contents(path,json.str);}catch(Error e){warning("%s",e.message);}
        }
    }
}
