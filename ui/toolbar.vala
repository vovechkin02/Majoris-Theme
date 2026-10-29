namespace Majoris.Ui {
    // Keep GTK's native keyboard navigation; only reset its sticky window flag
    // when an actionable toolbar item receives pointer input. Text editing is untouched.
    internal class ToolbarPointerFocus : GLib.Object {
        Gtk.GestureClick click=new Gtk.GestureClick();
        public ToolbarPointerFocus(Gtk.Widget widget) {
            click.propagation_phase=Gtk.PropagationPhase.CAPTURE;
            click.pressed.connect(on_pressed);widget.add_controller(click);
        }
        void on_pressed(int count,double x,double y) {
            var widget=click.get_widget();
            var window=widget==null?null:widget.get_root() as Gtk.Window;
            if(window!=null)window.focus_visible=false;
        }
    }

    // Label attributes/text can change after mapping (including accessibility sizing).
    // The label owns this binding; the receiver and label references do not form a cycle.
    internal class ToolbarLabelSize : GLib.Object {
        weak Gtk.Label label;
        int application_width;
        int applied_width=-1;
        public ToolbarLabelSize(Gtk.Label label) {
            this.label=label;application_width=label.width_request;
            label.notify["label"].connect(changed);
            label.notify["attributes"].connect(changed);
            label.notify["width-request"].connect(width_changed);
        }
        void changed(ParamSpec property) { if(label!=null)Toolbar.reserve_label(label); }
        void width_changed(ParamSpec property) {
            if(label!=null && label.width_request!=applied_width){application_width=label.width_request;Toolbar.reserve_label(label);}
        }
        public void reserve(int width) {
            applied_width=int.max(application_width,width);label.width_request=applied_width;
        }
    }
    internal class ToolbarSegments : GLib.Object {
        weak Gtk.Widget box;
        GLib.ListModel children;
        public ToolbarSegments(Gtk.Widget box) {
            this.box=box;children=box.observe_children();children.items_changed.connect(changed);
        }
        void changed(uint position,uint removed,uint added) { if(box!=null)Toolbar.prepare_segment_children(box); }
    }
    /** A native horizontal strip. Applications own actions and overflow policy. */
    public class Toolbar : Gtk.Box {
        public bool compact {
            get { return has_css_class("majoris-toolbar-compact"); }
            set { if (value) add_css_class("majoris-toolbar-compact"); else remove_css_class("majoris-toolbar-compact"); }
        }
        public bool divider {
            get { return has_css_class("majoris-toolbar-divider"); }
            set { if (value) add_css_class("majoris-toolbar-divider"); else remove_css_class("majoris-toolbar-divider"); }
        }
        GLib.ListModel children_model;
        Gtk.Widget[] watched={};
        ulong[] handlers={};
        bool refreshing=false;
        public Toolbar() {
            Object(orientation: Gtk.Orientation.HORIZONTAL, spacing: 4);
            add_css_class("majoris-toolbar");
            children_model=observe_children();
            children_model.items_changed.connect(children_changed);
            map.connect(()=>refresh_separators());
        }
        void children_changed(uint position,uint removed,uint added) { refresh_separators(); }
        void visibility_changed(ParamSpec property) { refresh_separators(); }
        internal static void reserve_label(Gtk.Label label) {
            if(label.get_data<ToolbarLabelSize>("majoris-toolbar-label-size")==null)
                label.set_data<ToolbarLabelSize>("majoris-toolbar-label-size",new ToolbarLabelSize(label));
            int width=0;
            foreach(var weight in new Pango.Weight[]{Pango.Weight.MEDIUM,Pango.Weight.SEMIBOLD}) {
                var font=label.get_pango_context().get_font_description().copy();font.set_weight(weight);
                var layout=label.create_pango_layout(label.label);layout.set_font_description(font);layout.set_attributes(label.attributes);
                int w,h;layout.get_pixel_size(out w,out h);width=int.max(width,w);
            }
            label.get_data<ToolbarLabelSize>("majoris-toolbar-label-size").reserve(width);
        }
        static void reserve_labels(Gtk.Widget widget) {
            if(widget is Gtk.Label){reserve_label((Gtk.Label)widget);return;}
            if(widget is Gtk.Popover || widget is Gtk.Entry || widget is Gtk.SearchEntry)return;
            for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling())reserve_labels(child);
        }
        static void prepare_pointer_focus(Gtk.Widget widget) {
            if(widget.get_data<ToolbarPointerFocus>("majoris-toolbar-pointer-focus")==null)
                widget.set_data<ToolbarPointerFocus>("majoris-toolbar-pointer-focus",new ToolbarPointerFocus(widget));
        }
        internal static void prepare_segment_children(Gtk.Widget widget) {
            if(widget.has_css_class("majoris-toolbar-segmented") || widget.has_css_class("majoris-toolbar-view-switcher"))
                for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling())if(child is Gtk.Button){reserve_labels(child);prepare_pointer_focus(child);}
        }
        internal static void prepare_segments(Gtk.Widget widget) {
            if(!widget.has_css_class("majoris-toolbar-segmented") && !widget.has_css_class("majoris-toolbar-view-switcher"))return;
            if(widget.get_data<ToolbarSegments>("majoris-toolbar-segments")==null)
                widget.set_data<ToolbarSegments>("majoris-toolbar-segments",new ToolbarSegments(widget));
            prepare_segment_children(widget);
        }
        /** Designate only the supplied control, never its nested descendants. */
        public static void prepare_control(Gtk.Widget widget) {
            widget.valign = Gtk.Align.CENTER;
            if (widget is Gtk.Button || widget is Gtk.MenuButton) {
                widget.add_css_class("majoris-toolbar-control");
                prepare_pointer_focus(widget);
                if (widget is Gtk.MenuButton) { widget.add_css_class("majoris-toolbar-menu"); if (((Gtk.MenuButton)widget).icon_name != null) widget.add_css_class("majoris-toolbar-icon"); }
                var button = widget as Gtk.Button;
                if(button!=null && widget.has_css_class("majoris-toolbar-action") && button.child is Gtk.Box)((Gtk.Box)button.child).spacing=8;
                if (button != null && (button.icon_name != null || button.child is Gtk.Image))
                    widget.add_css_class("majoris-toolbar-icon");
            } else if (widget is Gtk.Entry || widget is Gtk.SearchEntry) {
                widget.add_css_class("majoris-toolbar-field");
            } else if (widget is Gtk.DropDown) {
                widget.add_css_class("majoris-toolbar-select");
            }
        }
        public static void set_item_flat(Gtk.Widget widget, bool flat = true) {
            if (flat) widget.add_css_class("majoris-toolbar-item-flat");
            else widget.remove_css_class("majoris-toolbar-item-flat");
        }
        public void append_control(Gtk.Widget widget) { prepare_control(widget); append(widget); refresh_separators(); }
        public void prepend_control(Gtk.Widget widget) { prepare_control(widget); prepend(widget); refresh_separators(); }
        /** Insert at a zero-based position; positions past the end append. */
        public void insert_control(Gtk.Widget widget, uint position) {
            prepare_control(widget);
            Gtk.Widget? previous = null;
            var current = get_first_child();
            for (uint i=0; current != null && i<position; i++) { previous=current; current=current.get_next_sibling(); }
            insert_child_after(widget, previous); refresh_separators();
        }
        public void remove_control(Gtk.Widget widget) { remove(widget); refresh_separators(); }
        public void move_control(Gtk.Widget widget, uint position) {
            return_if_fail(widget.get_parent() == this);
            Gtk.Widget? previous = null;
            for (var current=get_first_child(); current != null; current=current.get_next_sibling()) {
                if (current == widget) continue;
                if (position == 0) break;
                previous=current; position--;
            }
            reorder_child_after(widget, previous); refresh_separators();
        }
        /** Append a custom child untouched, including application-owned composites. */
        public void append_widget(Gtk.Widget widget) { append(widget); refresh_separators(); }
        internal void refresh_separators() {
            if(refreshing)return;refreshing=true;
            Gtk.Widget[] current={};ulong[] signals={};
            for(var child=get_first_child();child!=null;child=child.get_next_sibling()) {
                int index=-1;for(int i=0;i<watched.length;i++)if(watched[i]==child){index=i;break;}
                current+=child;signals+=index>=0?handlers[index]:child.notify["visible"].connect(visibility_changed);
            }
            for(int i=0;i<watched.length;i++)if(watched[i].get_parent()!=this){watched[i].disconnect(handlers[i]);watched[i].remove_css_class("majoris-toolbar-group-gap");}
            watched=current;handlers=signals;
            bool before=false;
            Gtk.Widget? previous=null;
            for (var item=get_first_child(); item!=null; item=item.get_next_sibling()) {
                if (item is Gtk.Separator && item.has_css_class("majoris-toolbar-separator")) {
                    bool after=false;
                    for (var next=item.get_next_sibling(); next!=null; next=next.get_next_sibling()) {
                        if (next.visible && !(next is Gtk.Separator) && !next.has_css_class("majoris-toolbar-spacer")) {after=true;break;}
                    }
                    item.visible=before && after; if(item.visible)before=false;
                } else if(item.visible && !item.has_css_class("majoris-toolbar-spacer")) before=true;
                item.remove_css_class("majoris-toolbar-group-gap");
                if(item.visible) {
                    bool boundary=previous!=null && (item is ToolbarGroup || previous is ToolbarGroup);
                    if(boundary && !(item is Gtk.Separator) && !(previous is Gtk.Separator) && !item.has_css_class("majoris-toolbar-spacer") && !previous.has_css_class("majoris-toolbar-spacer"))item.add_css_class("majoris-toolbar-group-gap");
                    prepare_segments(item);
                    if(item is Gtk.ToggleButton && item.has_css_class("majoris-toolbar-control"))reserve_labels(item);
                    if(item is ToolbarGroup)for(var c=item.get_first_child();c!=null;c=c.get_next_sibling()){prepare_segments(c);if(c is Gtk.ToggleButton && c.has_css_class("majoris-toolbar-control"))reserve_labels(c);}
                    previous=item;
                }
            }
            refreshing=false;
        }
        public ToolbarGroup append_group() { var group=new ToolbarGroup(); append(group); return group; }
        public Gtk.Separator append_separator() {
            var item=new Gtk.Separator(Gtk.Orientation.VERTICAL);
            item.add_css_class("majoris-toolbar-separator"); append(item); refresh_separators(); return item;
        }
        public Gtk.Box append_spacer() {
            var item=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0); item.hexpand=true;
            item.add_css_class("majoris-toolbar-spacer"); append(item); return item;
        }
    }
    /** Transparent arbitrary-content group; removal uses ordinary Gtk.Box APIs. */
    public class ToolbarGroup : Gtk.Box {
        GLib.ListModel children_model;
        Gtk.Widget[] watched={};ulong[] handlers={};bool syncing=false;
        public ToolbarGroup() {
            Object(orientation:Gtk.Orientation.HORIZONTAL,spacing:4,valign:Gtk.Align.CENTER);
            add_css_class("majoris-toolbar-group");
            add_css_class("majoris-toolbar-native-group");
            visible=false;
            children_model=observe_children();children_model.items_changed.connect((position,removed,added)=>sync_visibility());
        }
        public new void append(Gtk.Widget widget) { base.append(widget); sync_visibility(); }
        public new void remove(Gtk.Widget widget) { base.remove(widget); sync_visibility(); }
        void visibility_changed(ParamSpec property){sync_visibility();}
        void sync_visibility() {
            if(syncing)return;syncing=true;
            Gtk.Widget[] current={};ulong[] signals={};bool any=false;
            for(var child=get_first_child();child!=null;child=child.get_next_sibling()){
                int index=-1;for(int i=0;i<watched.length;i++)if(watched[i]==child){index=i;break;}
                current+=child;signals+=index>=0?handlers[index]:child.notify["visible"].connect(visibility_changed);any=any||child.visible;
            }
            for(int i=0;i<watched.length;i++)if(watched[i].get_parent()!=this)watched[i].disconnect(handlers[i]);
            watched=current;handlers=signals;visible=any;syncing=false;
            var toolbar=get_parent() as Toolbar;if(toolbar!=null)toolbar.refresh_separators();
        }
        public void remove_control(Gtk.Widget widget) { remove(widget); }
        public void append_control(Gtk.Widget widget) { Toolbar.prepare_control(widget); append(widget); }
        public void append_widget(Gtk.Widget widget) { append(widget); }
    }
}
