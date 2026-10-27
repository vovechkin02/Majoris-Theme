namespace Majoris.Ui {
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
        public Toolbar() {
            Object(orientation: Gtk.Orientation.HORIZONTAL, spacing: 0);
            add_css_class("majoris-toolbar");
        }
        /** Designate only the supplied control, never its nested descendants. */
        public static void prepare_control(Gtk.Widget widget) {
            widget.valign = Gtk.Align.CENTER;
            if (widget is Gtk.Button || widget is Gtk.MenuButton) {
                widget.add_css_class("majoris-toolbar-control");
                if (widget is Gtk.MenuButton) { widget.add_css_class("majoris-toolbar-menu"); if (((Gtk.MenuButton)widget).icon_name != null) widget.add_css_class("majoris-toolbar-icon"); }
                var button = widget as Gtk.Button;
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
            bool before=false;
            for (var item=get_first_child(); item!=null; item=item.get_next_sibling()) {
                if (item is Gtk.Separator && item.has_css_class("majoris-toolbar-separator")) {
                    bool after=false;
                    for (var next=item.get_next_sibling(); next!=null; next=next.get_next_sibling()) {
                        if (next.visible && !(next is Gtk.Separator) && !next.has_css_class("majoris-toolbar-spacer")) {after=true;break;}
                    }
                    item.visible=before && after; if(item.visible)before=false;
                } else if(item.visible && !item.has_css_class("majoris-toolbar-spacer")) before=true;
            }
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
        public ToolbarGroup() {
            Object(orientation:Gtk.Orientation.HORIZONTAL,spacing:0,valign:Gtk.Align.CENTER);
            add_css_class("majoris-toolbar-group");
            visible=false;
        }
        public new void append(Gtk.Widget widget) { base.append(widget); sync_visibility(); }
        public new void remove(Gtk.Widget widget) { base.remove(widget); sync_visibility(); }
        void sync_visibility() { visible=get_first_child()!=null;var toolbar=get_parent() as Toolbar;if(toolbar!=null)toolbar.refresh_separators(); }
        public void remove_control(Gtk.Widget widget) { remove(widget); }
        public void append_control(Gtk.Widget widget) { Toolbar.prepare_control(widget); append(widget); }
        public void append_widget(Gtk.Widget widget) { append(widget); }
    }
}
