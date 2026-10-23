// Exercise the actual factory implementation, including native input dispatch.
namespace MajorisThemeFactory {
    [CCode(cname="majoris_theme_attach")] extern static void attach_theme();
    public Gtk.Button icon_button(string icon,string label) {var b=new Gtk.Button.from_icon_name(icon);b.tooltip_text=label;b.valign=Gtk.Align.CENTER;return b;}
    public Gtk.MenuButton menu_button() {return new Gtk.MenuButton();}
    public void install_menu_actions(Gtk.ApplicationWindow w) {}
    void key(string value) {try {Process.spawn_command_line_sync("xdotool key --clearmodifiers "+value);}catch(Error e){error("%s",e.message);}}
    int main(string[] args) {
        var app=new Adw.Application("com.majoris.LocationTest",ApplicationFlags.NON_UNIQUE);
        app.activate.connect(()=>{
            attach_theme();var window=new LocationFixture(app);window.present();
            var bar=window.location;int phase=0;
            Adw.StyleManager.get_default().color_scheme=Adw.ColorScheme.FORCE_LIGHT;
            Timeout.add(400,()=>{
                switch(phase++) {
                case 0: assert(!bar.editing);
                    for(var button=bar.get_parent().get_first_child();button!=bar;button=button.get_next_sibling())assert(button.get_allocated_width()==32 && button.get_allocated_height()==32);
                    key("ctrl+l");break;
                case 1: assert(bar.editing);int start,end;assert(bar.entry.get_selection_bounds(out start,out end));assert(end-start==bar.path.length);bar.entry.text="/cancelled";key("Escape");break;
                case 2: assert(!bar.editing && bar.path=="/home/demo/Documents");key("alt+d");break;
                case 3: assert(bar.editing);bar.entry.text="relative";key("Return");break;
                case 4: assert(bar.editing && bar.path=="/home/demo/Documents");bar.entry.text="/home/demo/Downloads";key("Return");break;
                case 5: assert(!bar.editing && bar.path=="/home/demo/Downloads");bar.back();assert(bar.path=="/home/demo/Documents");bar.forward();assert(bar.path=="/home/demo/Downloads");bar.up();assert(bar.path=="/home/demo");bar.home();bar.begin_edit();bar.entry.text="/outside";try{Process.spawn_command_line_sync("xdotool mousemove 400 170 click 1");}catch(Error e){error("%s",e.message);}break;
                case 6: assert(!bar.editing && bar.path=="/home/demo");Graphene.Rect crumb_bounds;assert(bar.crumbs.get_first_child().compute_bounds(window,out crumb_bounds));
                    try{Process.spawn_command_line_sync("xdotool mousemove %d %d click 1".printf((int)crumb_bounds.origin.x+10,(int)crumb_bounds.origin.y+12));}catch(Error e){error("%s",e.message);}break;
                case 7: assert(bar.path=="/" && !bar.editing);
                    Graphene.Rect bounds;assert(bar.compute_bounds(window,out bounds));
                    try{Process.spawn_command_line_sync("xdotool mousemove %d %d click 1".printf((int)(bounds.origin.x+bounds.size.width-20),(int)(bounds.origin.y+12)));}catch(Error e){error("%s",e.message);}break;
                case 8: assert(bar.editing);bar.end_edit();bar.navigate("/home/demo/Documents/An extremely long folder/Projects/References/Archive");window.set_default_size(480,650);Adw.StyleManager.get_default().color_scheme=Adw.ColorScheme.FORCE_DARK;break;
                case 9: assert(bar.get_width()>48);assert(bar.viewport.hadjustment.value>0);assert(bar.get_color().to_string()=="rgb(244,244,245)");Adw.StyleManager.get_default().color_scheme=Adw.ColorScheme.FORCE_LIGHT;bar.begin_edit();break;
                case 10: assert(bar.editing);assert(bar.get_color().to_string()=="rgb(28,28,31)");assert(!bar.navigate("/home/../"+".."));bar.end_edit();bar.navigate("/branch");assert(!bar.can_forward);stdout.printf("Location native keyboard, selection, validation, cancellation, crumbs, history, narrow layout and switching passed\n");window.close();app.quit();return Source.REMOVE;
                }
                return Source.CONTINUE;
            });
        });return app.run({args[0]});
    }
}


