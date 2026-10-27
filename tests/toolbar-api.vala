/* Public API consumer: deliberately GTK4-only, without factory or libadwaita. */
int main(string[] args) {
    Gtk.init();
    var window=new Gtk.Window();window.default_width=640;
    var toolbar=new Majoris.Ui.Toolbar();assert(toolbar.get_first_child()==null);
    var button=new Gtk.Button.with_label("Back");int calls=0;button.clicked.connect(()=>calls++);
    toolbar.append_control(button);assert(button.get_parent()==toolbar);
    var custom=new Gtk.Label("Custom");toolbar.append_widget(custom);
    var first=new Gtk.Button.with_label("First");toolbar.prepend_control(first);assert(toolbar.get_first_child()==first);
    var inserted=new Gtk.Button.with_label("Inserted");toolbar.insert_control(inserted,1);assert(first.get_next_sibling()==inserted);
    toolbar.move_control(custom,0);assert(toolbar.get_first_child()==custom);
    toolbar.remove_control(inserted);assert(inserted.get_parent()==null);
    var group=toolbar.append_group();assert(!group.visible);
    var grouped=new Gtk.Button.with_label("Group");group.append_control(grouped);assert(group.visible);
    var separator=toolbar.append_separator();assert(!separator.visible);
    var spacer=toolbar.append_spacer();assert(spacer.hexpand);
    var tail=new Gtk.Button.with_label("Tail");toolbar.append_control(tail);assert(separator.visible);
    group.remove_control(grouped);assert(!group.visible);group.append_control(grouped);
    toolbar.compact=true;assert(toolbar.has_css_class("majoris-toolbar-compact"));toolbar.compact=false;
    toolbar.divider=true;assert(toolbar.divider);
    Majoris.Ui.Toolbar.set_item_flat(button);assert(button.has_css_class("majoris-toolbar-item-flat"));
    Majoris.Ui.Toolbar.set_item_flat(button,false);assert(!button.has_css_class("majoris-toolbar-item-flat"));
    var segments=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);segments.add_css_class("majoris-toolbar-segmented");
    var left=new Gtk.ToggleButton.with_label("Left");var right=new Gtk.ToggleButton.with_label("Right");right.group=left;left.active=true;right.active=true;assert(!left.active && right.active);segments.append(left);segments.append(right);toolbar.append_widget(segments);
    var menu=new Gtk.MenuButton();menu.label="Menu";var popup=new Gtk.Popover();popup.child=new Gtk.Label("Native menu");menu.popover=popup;toolbar.append_control(menu);
    var field=new Gtk.Entry();toolbar.append_control(field);assert(field.has_css_class("majoris-toolbar-field"));
    var selector=new Gtk.DropDown.from_strings({"Files","Format"});toolbar.append_control(selector);assert(selector.has_css_class("majoris-toolbar-select"));
    window.child=toolbar;window.present();
    var loop=new MainLoop();
    Timeout.add(250,()=>{
        menu.popup();assert(popup.visible);menu.popdown();
        assert(button.grab_focus());assert(window.child_focus(Gtk.DirectionType.TAB_FORWARD));
        button.clicked();assert(calls==1);
        toolbar.remove_control(button);assert(button.get_parent()==null);button.clicked();assert(calls==2);
        window.set_focus(null);menu.popover=null;window.child=null;window.destroy();loop.quit();return Source.REMOVE;
    });loop.run();
    bool finalized=false;toolbar.weak_ref(()=>{finalized=true;});
    toolbar=null;window=null;
    var cleanup=new MainLoop();Timeout.add(350,()=>{cleanup.quit();return Source.REMOVE;});cleanup.run();assert(finalized);
    stdout.printf("GTK-only public API, dynamic items, native signals, focus, menu and lifetime passed\n");return 0;
}
