namespace MajorisThemeFactory {
    /** Native custom child of GtkPopoverMenu. Actions and accelerators belong to
     * the application, just as they do for ordinary GMenu rows. */
    public class MenuRow : Gtk.Button {
        static construct { set_accessible_role(Gtk.AccessibleRole.MENU_ITEM); }
        public MenuRow(string text, string action, string shortcut, string[] keys, string? icon=null) {
            add_css_class("majoris-menu-row");
            action_name=action;
            var row=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);
            var title=new Gtk.Label(text); title.xalign=0; title.hexpand=true; row.append(title);
            var caps=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0); caps.add_css_class("majoris-menu-shortcut"); caps.valign=Gtk.Align.CENTER;
            foreach(var key in keys) { var cap=new Gtk.Label(key); cap.add_css_class("majoris-menu-keycap"); caps.append(cap); }
            row.append(caps); child=row;
            update_property(Gtk.AccessibleProperty.LABEL,text,Gtk.AccessibleProperty.KEY_SHORTCUTS,shortcut,-1);
            clicked.connect(()=>{ var pop=get_ancestor(typeof(Gtk.Popover)) as Gtk.Popover; if(pop!=null)pop.popdown(); });
        }
    }
}
