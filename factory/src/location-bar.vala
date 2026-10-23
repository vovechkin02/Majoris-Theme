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
            Object(orientation:Gtk.Orientation.HORIZONTAL,spacing:0,hexpand:true);
            add_css_class("majoris-location-bar");
            modes=new Gtk.Stack(); modes.hexpand=true; modes.hhomogeneous=false;
            crumbs=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);
            var scroll=new Gtk.ScrolledWindow(); viewport=scroll; scroll.hscrollbar_policy=Gtk.PolicyType.EXTERNAL;
            scroll.vscrollbar_policy=Gtk.PolicyType.NEVER; scroll.hexpand=true; scroll.child=crumbs;
            double previous_upper=-1,previous_page=-1;
            scroll.add_tick_callback((widget,clock)=>{
                var adjustment=scroll.hadjustment;
                if(adjustment.upper!=previous_upper || adjustment.page_size!=previous_page) {
                    previous_upper=adjustment.upper;previous_page=adjustment.page_size;
                    adjustment.value=double.max(0,adjustment.upper-adjustment.page_size);
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
                var separator=new Gtk.Label("›");separator.add_css_class("majoris-location-separator");crumbs.append(separator);
                accumulated+="/"+part; add_crumb(part,accumulated);
            }
        }
        void add_crumb(string title,string target) {
            var button=new Gtk.Button(); var label=new Gtk.Label(title); label.ellipsize=Pango.EllipsizeMode.END; label.max_width_chars=24; label.width_chars=int.min(title.char_count(),24);
            button.child=label; button.tooltip_text=target;button.add_css_class("majoris-location-crumb");
            if(target==path)button.add_css_class("majoris-location-current");
            button.clicked.connect(()=>navigate(target)); crumbs.append(button);
        }
    }
    public class LocationFixture : Adw.ApplicationWindow {
        public LocationBar location;
        public LocationFixture(Gtk.Application app,string mode="location") {
            Object(application:app,title:"Majoris Files Components",default_width:900,default_height:650);
            var chrome=new Adw.ToolbarView();var header=new Adw.HeaderBar();header.pack_end(menu_button());chrome.add_top_bar(header);
            var layout=new Gtk.Box(Gtk.Orientation.VERTICAL,12);
            var documents=new Adw.TabView();documents.vexpand=true;
            var tabs=new Adw.TabBar();tabs.view=documents;tabs.autohide=false;tabs.add_css_class("majoris-document-tabs");layout.append(tabs);
            var toolbar=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4); toolbar.margin_start=12;toolbar.margin_end=12;
            var back=icon_button("go-previous-symbolic","Back");var forward=icon_button("go-next-symbolic","Forward");
            var up=icon_button("go-up-symbolic","Up");var home=icon_button("go-home-symbolic","Home");
            toolbar.append(back);toolbar.append(forward);toolbar.append(up);toolbar.append(home);
            location=new LocationBar();toolbar.append(location);layout.append(toolbar);
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
            var width=Environment.get_variable("MAJORIS_CONTENT_WIDTH");if(width!=null)set_default_size(int.parse(width),650);
            if(mode=="location-editing")Timeout.add(500,()=>{location.begin_edit();return Source.REMOVE;});
        }
    }
}
