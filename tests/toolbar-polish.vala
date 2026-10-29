[CCode(cname="majoris_theme_attach")] extern void attach_theme();
class PolishWindow : Adw.Window {
    public Majoris.Ui.Toolbar standard=new Majoris.Ui.Toolbar();
    public Majoris.Ui.Toolbar compact=new Majoris.Ui.Toolbar();
    Gtk.Button raised=new Gtk.Button.with_label("Back");
    Gtk.Button flat=new Gtk.Button.with_label("Refresh");
    Gtk.Button disabled=new Gtk.Button.with_label("Disabled");
    Gtk.ToggleButton segment_a=new Gtk.ToggleButton.with_label("Favorites");
    Gtk.ToggleButton segment_b=new Gtk.ToggleButton.with_label("Files");
    Gtk.Entry entry=new Gtk.Entry();
    Majoris.Ui.ToolbarGroup group;
    Majoris.Ui.ToolbarGroup next_group;
    Gtk.Button first=new Gtk.Button.with_label("New Folder");
    Gtk.Button second=new Gtk.Button.with_label("Properties");
    Gtk.Button third=new Gtk.Button.with_label("Format");
    Gtk.Button fourth=new Gtk.Button.with_label("Sort");
    Gtk.Button edge=new Gtk.Button.with_label("Forward");
    Gtk.Widget[] disabled_samples={};
    Gtk.Widget[] compact_buttons={};
    Gtk.Button legacy_first=new Gtk.Button.with_label("Undo");
    Gtk.Button legacy_second=new Gtk.Button.with_label("Redo");
    Gtk.Box choices;
    Gtk.ToggleButton? dynamic_segment;
    int stage=0;string report_path;
    Gtk.Button compact_disabled=new Gtk.Button.with_label("Redo");
    public PolishWindow(string path) {
        Object(title:"Majoris Toolbar Polish",default_width:1180,default_height:360);
        report_path=path;
        var root=new Gtk.Box(Gtk.Orientation.VERTICAL,0);
        standard.divider=true;compact.compact=true;compact.divider=true;
        Majoris.Ui.Toolbar.set_item_flat(flat);disabled.sensitive=false;
        standard.append_control(raised);standard.append_control(flat);standard.append_control(disabled);
        group=standard.append_group();group.append_control(first);group.append_control(second);
        next_group=standard.append_group();next_group.append_control(third);next_group.append_control(fourth);
        choices=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);choices.add_css_class("majoris-toolbar-segmented");choices.valign=Gtk.Align.CENTER;segment_b.group=segment_a;segment_a.active=true;choices.append(segment_a);choices.append(segment_b);standard.append_widget(choices);standard.append_spacer();standard.append_control(edge);
        foreach(var text in new string[]{"Undo","Redo","Bold","Italic"}){var button=new Gtk.ToggleButton.with_label(text);Majoris.Ui.Toolbar.set_item_flat(button);compact.append_control(button);compact_buttons+=button;}
        Majoris.Ui.Toolbar.set_item_flat(compact_disabled);compact_disabled.sensitive=false;compact.append_control(compact_disabled);
        entry.placeholder_text="Editing focus remains visible";compact.append_control(entry);
        root.append(standard);root.append(compact);
        var disabled_row=new Majoris.Ui.Toolbar();
        var disabled_flat=new Gtk.Button.with_label("Undo");Majoris.Ui.Toolbar.set_item_flat(disabled_flat);
        var disabled_icon=new Gtk.Button.from_icon_name("go-next-symbolic");
        var disabled_action=new Gtk.Button();disabled_action.add_css_class("majoris-toolbar-action");
        var action_box=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);action_box.append(new Gtk.Image.from_icon_name("folder-new-symbolic"));action_box.append(new Gtk.Label("New Folder"));disabled_action.child=action_box;
        var disabled_menu=new Gtk.MenuButton();disabled_menu.label="Sort";disabled_menu.popover=new Gtk.Popover();
        disabled_samples={disabled_flat,disabled_icon,disabled_action,disabled_menu};
        foreach(var sample in disabled_samples){sample.sensitive=false;disabled_row.append_control(sample);}
        var disabled_segments=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);disabled_segments.add_css_class("majoris-toolbar-segmented");disabled_segments.valign=Gtk.Align.CENTER;
        var disabled_segment=new Gtk.ToggleButton.with_label("Format");disabled_segment.sensitive=false;disabled_segments.append(disabled_segment);disabled_row.append_widget(disabled_segments);disabled_samples+=disabled_segment;disabled_samples+=compact_disabled;
        root.append(disabled_row);
        var legacy=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);legacy.add_css_class("majoris-toolbar-navigation");
        var native_group=new Majoris.Ui.ToolbarGroup();native_group.append_control(legacy_first);native_group.append_control(legacy_second);legacy.append(native_group);root.append(legacy);
        var note=new Gtk.Label("Two native Toolbar instances, no external padding or stacked gap");note.xalign=0;root.append(note);content=root;
        var keys=new Gtk.EventControllerKey();keys.key_pressed.connect((key,code,mods)=>{
            if(key==Gdk.Key.F6){stage++;mutate();return true;}return false;
        });((Gtk.Widget)this).add_controller(keys);
        Timeout.add(150,()=>{write_report();return Source.CONTINUE;});
    }
    void mutate(){
        if(stage==1){group.remove_control(second);}
        if(stage==2){group.insert_child_after(second,first);}
        if(stage==3){standard.move_control(next_group,0);}
        if(stage==4){group.remove_control(first);group.remove_control(second);}
        if(stage==5){group.append_control(first);group.append_control(second);}
        if(stage==6){standard.append_separator();standard.append_separator();standard.append_control(new Gtk.Button.with_label("Tail"));}
        if(stage==7){standard.add_css_class("majoris-toolbar-major-groups");}
        if(stage==8){standard.remove_css_class("majoris-toolbar-major-groups");standard.compact=true;}
        if(stage==9){segment_b.active=true;}
        if(stage==10){first.visible=false;second.visible=false;}
        if(stage==11){first.visible=true;second.visible=true;}
        if(stage==12){standard.remove_control(next_group);}
        if(stage==13){standard.insert_child_after(next_group,disabled);}
        if(stage==14){((Gtk.ToggleButton)compact_buttons[0]).active=true;}
        if(stage==15){standard.divider=false;}
        if(stage==16){Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL);}
        if(stage==17){var attrs=new Pango.AttrList();attrs.insert(Pango.AttrSize.new_absolute(24*Pango.SCALE));find_label(segment_a).attributes=attrs;find_label(segment_b).attributes=attrs;}
        if(stage==18){segment_a.active=true;}
        if(stage==19){find_label(segment_a).attributes=null;find_label(segment_b).attributes=null;}
        if(stage==20){segment_b.label="Files and Favorites";}
        if(stage==21){segment_b.active=true;}
        if(stage==22){dynamic_segment=new Gtk.ToggleButton.with_label("Format");dynamic_segment.group=segment_a;choices.append(dynamic_segment);}
        if(stage==23){dynamic_segment.active=true;}
    }
    string bounds(Gtk.Widget w){Graphene.Rect r;if(!w.compute_bounds(this,out r))return "[0,0,0,0]";return "[%g,%g,%g,%g]".printf(r.origin.x,r.origin.y,r.size.width,r.size.height);}
    Gtk.Label? find_label(Gtk.Widget widget){
        if(widget is Gtk.Label)return (Gtk.Label)widget;if(widget is Gtk.Popover)return null;
        for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling()){var label=find_label(child);if(label!=null)return label;}return null;
    }
    string font(Gtk.Widget widget){var label=find_label(widget);if(label==null)return "null";var d=label.get_pango_context().get_font_description().copy();if(label.attributes!=null){Pango.Language language;GLib.SList<Pango.Attribute> extra;var iterator=label.attributes.get_iterator();var attributes_font=new Pango.FontDescription();iterator.get_font(attributes_font,out language,out extra);d.merge(attributes_font,true);}int lx,ly;label.get_layout_offsets(out lx,out ly);Pango.Rectangle ink,logical;label.get_layout().get_pixel_extents(out ink,out logical);return "{\"size\":%g,\"weight\":%d,\"label\":%s,\"ink\":[%d,%d,%d,%d],\"logical\":[%d,%d,%d,%d],\"baseline\":%d,\"color\":\"%s\",\"resolved\":\"%s\",\"layout_offset\":[%d,%d]}".printf((double)d.get_size()/Pango.SCALE,(int)d.get_weight(),bounds(label),ink.x,ink.y,ink.width,ink.height,logical.x,logical.y,logical.width,logical.height,label.get_layout().get_baseline()/Pango.SCALE,label.get_style_context().get_color().to_string(),label.get_pango_context().load_font(d).describe().to_string(),lx,ly);}
    void write_report(){
        var s=new StringBuilder("{");s.append("\"stage\":%d,\"window\":%s,\"standard\":%s,\"compact\":%s,".printf(stage,bounds(this),bounds(standard),bounds(compact)));
        s.append("\"raised\":%s,\"flat\":%s,\"disabled\":%s,\"first\":%s,\"second\":%s,\"third\":%s,\"fourth\":%s,\"group_visible\":%s,\"group\":%s,\"next_group\":%s,\"segments\":[%s,%s],\"entry\":%s,".printf(bounds(raised),bounds(flat),bounds(disabled),bounds(first),bounds(second),bounds(third),bounds(fourth),group.visible.to_string(),bounds(group),bounds(next_group),bounds(segment_a),bounds(segment_b),bounds(entry)));
        s.append("\"legacy_controls\":[%s,%s],\"dynamic_segment\":%s,\"edge\":%s,\"text_metrics\":[%s,%s,%s,%s,%s".printf(bounds(legacy_first),bounds(legacy_second),dynamic_segment==null?"[0,0,0,0]":bounds(dynamic_segment),bounds(edge),font(first),font(second),font(third),font(fourth),font(edge)));
        foreach(var button in compact_buttons)s.append(","+font(button));s.append("],\"compact_first\":"+bounds(compact_buttons[0])+",\"disabled_samples\":[");
        for(int i=0;i<disabled_samples.length;i++){if(i>0)s.append(",");s.append("{\"bounds\":%s,\"font\":%s}".printf(bounds(disabled_samples[i]),font(disabled_samples[i])));}s.append("],");
        s.append("\"flags\":[%u,%u,%u,%u],\"fonts\":[%s,%s,%s,%s,%s],\"separators\":[".printf((uint)raised.get_state_flags(),(uint)flat.get_state_flags(),(uint)segment_a.get_state_flags(),(uint)segment_b.get_state_flags(),font(raised),font(flat),font(disabled),font(segment_a),font(segment_b)));
        bool first_item=true;for(var c=standard.get_first_child();c!=null;c=c.get_next_sibling())if(c is Gtk.Separator){if(!first_item)s.append(",");first_item=false;s.append(c.visible.to_string());}s.append("]}");try{FileUtils.set_contents(report_path,s.str);}catch(Error e){warning("%s",e.message);}
    }
}
int main(string[] args){Adw.init();var style=Adw.StyleManager.get_default();style.color_scheme=Environment.get_variable("MAJORIS_VARIANT")=="dark"?Adw.ColorScheme.FORCE_DARK:Adw.ColorScheme.FORCE_LIGHT;attach_theme();Gtk.Settings.get_default().gtk_enable_animations=false;var window=new PolishWindow(args[1]);window.present();var loop=new MainLoop();window.close_request.connect(()=>{loop.quit();return false;});loop.run();return 0;}
