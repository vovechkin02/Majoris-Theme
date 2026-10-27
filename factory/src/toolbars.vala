namespace MajorisThemeFactory {
    public class ToolbarsPage : Gtk.Box {
        public Gtk.Box navigation;
        public Gtk.Box commands;
        public Gtk.Box switcher;
        public LocationBar location;
        public Gtk.SearchEntry search;
        public Gtk.Label result;
        public Gtk.Button back;
        public Gtk.Button forward;
        public ToolbarsPage(string mode="toolbars") {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:0);
            result=new Gtk.Label("Native toolbars — actions report here. Scroll either row at narrow widths."); result.wrap=true;result.add_css_class("majoris-toolbar-metadata");
            var actions=new SimpleActionGroup();var choice=new SimpleAction("choice",VariantType.STRING);choice.activate.connect((value)=>{var selected=value.get_string();result.label="Selected: "+selected;if(selected=="Documents" || selected=="Downloads")location.navigate("/home/demo/"+selected);if(selected=="Favorites")location.home();});actions.add_action(choice);insert_action_group("toolbar",actions);
            result.margin_top=16; result.margin_bottom=16;
            navigation=bar("majoris-toolbar-navigation");navigation.add_css_class("majoris-toolbar-divider");
            var history=group();navigation.append(history);
            location=new LocationBar(); location.valign=Gtk.Align.CENTER;
            back=icon("go-previous-symbolic","Back");forward=icon("go-next-symbolic","Forward");history.append(back);history.append(forward);
            back.clicked.connect(()=>location.back());forward.clicked.connect(()=>location.forward());
            var up=icon("go-up-symbolic","Up");up.clicked.connect(()=>location.up());history.append(up);
            var places=menu("Locations",{"Favorites","Files","Documents","Downloads"});history.append(places);
            var refresh=icon("view-refresh-symbolic","Refresh");refresh.clicked.connect(()=>result.label="Refreshed "+location.path);history.append(refresh);
            location.navigated.connect(()=>{back.sensitive=location.can_back;forward.sensitive=location.can_forward;result.label="Location: "+location.path;});back.sensitive=false;forward.sensitive=false;
            navigation.append(location);
            search=new Gtk.SearchEntry();search.add_css_class("majoris-toolbar-field");search.valign=Gtk.Align.CENTER;search.placeholder_text="Search"; search.width_request=160;
            search.search_changed.connect(()=>result.label=search.text==""?"Search cleared":"Search: "+search.text);navigation.append(search);
            append(viewport(navigation));
            commands=bar("majoris-toolbar-commands");var primary=group();commands.append(primary);
            var create=action("New Folder","folder-new-symbolic");create.clicked.connect(()=>result.label="New Folder created (fixture)");primary.append(create);
            foreach(var name in new string[]{"Cut","Copy","Paste"}) {var button=icon(name=="Cut"?"edit-cut-symbolic":(name=="Copy"?"edit-copy-symbolic":"edit-paste-symbolic"),name);button.clicked.connect(()=>result.label=name+" activated");primary.append(button);}
            var separator=new Gtk.Separator(Gtk.Orientation.VERTICAL);separator.add_css_class("majoris-toolbar-separator");commands.append(separator);
            var secondary=group();commands.append(secondary);
            foreach(var name in new string[]{"Rename","Share","Trash"}) {var button=icon(name=="Rename"?"document-edit-symbolic":(name=="Share"?"send-to-symbolic":"user-trash-symbolic"),name);button.clicked.connect(()=>result.label=name+" activated");secondary.append(button);}
            var spacer=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);spacer.hexpand=true;spacer.add_css_class("majoris-toolbar-spacer");commands.append(spacer);
            var view_group=group();commands.append(view_group);view_group.append(menu("Sort",{"Name","Date","Size"}));
            switcher=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);switcher.add_css_class("majoris-toolbar-view-switcher");switcher.valign=Gtk.Align.CENTER;
            Gtk.ToggleButton? leader=null;string[] views={"Grid","List","Columns","Gallery"};string[] icons={"view-grid-symbolic","view-list-symbolic","view-dual-symbolic","view-paged-symbolic"};
            for(int i=0;i<views.length;i++) {var toggle=new Gtk.ToggleButton();var glyph=new Gtk.Image.from_icon_name(icons[i]);glyph.pixel_size=16;glyph.valign=Gtk.Align.CENTER;glyph.halign=Gtk.Align.CENTER;toggle.child=glyph;toggle.tooltip_text=views[i];toggle.update_property(Gtk.AccessibleProperty.LABEL,views[i],-1);if(leader==null){leader=toggle;toggle.active=true;}else toggle.group=leader;string selected=views[i];toggle.toggled.connect(()=>{if(toggle.active)result.label="View: "+selected;});switcher.append(toggle);}
            view_group.append(switcher);view_group.append(menu("View Settings",{"Show hidden files","Show thumbnails"}));
            var preview=icon("view-reveal-symbolic","Preview");preview.clicked.connect(()=>result.label="Preview toggled");view_group.append(preview);
            append(viewport(commands));append(result);
            var note=new Gtk.Label("Editor comparison: existing 28px flat actions, independent from general toolbars");note.xalign=0;note.wrap=true;note.margin_start=16;append(note);
            var editor=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4);editor.add_css_class("majoris-editor-toolbar");foreach(var name in new string[]{"Bold","Italic","Underline"}){var button=new Gtk.ToggleButton.with_label(name);button.valign=Gtk.Align.CENTER;editor.append(button);}append(editor);
            var field_row=bar("majoris-toolbar-navigation");var entry=new Gtk.Entry();entry.add_css_class("majoris-toolbar-field");entry.placeholder_text="Native entry — Favorites / Files / Format";entry.hexpand=true;entry.valign=Gtk.Align.CENTER;field_row.append(entry);append(viewport(field_row));
            var keys=new Gtk.EventControllerKey();keys.propagation_phase=Gtk.PropagationPhase.CAPTURE;
            keys.key_pressed.connect((key,code,mods)=>{if(((mods&Gdk.ModifierType.CONTROL_MASK)!=0 && (key==Gdk.Key.l || key==Gdk.Key.L)) || ((mods&Gdk.ModifierType.ALT_MASK)!=0 && (key==Gdk.Key.d || key==Gdk.Key.D))){location.begin_edit();return true;}if((mods&Gdk.ModifierType.CONTROL_MASK)!=0 && (key==Gdk.Key.f || key==Gdk.Key.F)){search.grab_focus();return true;}return false;});add_controller(keys);
            if(mode=="toolbars-editing")Timeout.add(400,()=>{location.show_editing();return Source.REMOVE;});
            if(mode=="toolbars-states")Timeout.add(500,()=>{refresh.set_state_flags(Gtk.StateFlags.PRELIGHT,false);create.set_state_flags(Gtk.StateFlags.ACTIVE,false);preview.set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);return Source.REMOVE;});
            if(mode=="toolbars-popover")Timeout.add(600,()=>{places.popup();return Source.REMOVE;});
        }
        Gtk.Box bar(string variant) {var widget=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);widget.add_css_class("majoris-toolbar");widget.add_css_class(variant);return widget;}
        Gtk.Box group() {var widget=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);widget.add_css_class("majoris-toolbar-group");widget.valign=Gtk.Align.CENTER;return widget;}
        Gtk.ScrolledWindow viewport(Gtk.Widget child) {var scroll=new Gtk.ScrolledWindow();scroll.hscrollbar_policy=Gtk.PolicyType.EXTERNAL;scroll.vscrollbar_policy=Gtk.PolicyType.NEVER;scroll.propagate_natural_height=true;scroll.child=child;return scroll;}
        Gtk.Button icon(string name,string title) {var widget=new Gtk.Button.from_icon_name(name);widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-icon");widget.valign=Gtk.Align.CENTER;widget.tooltip_text=title;widget.update_property(Gtk.AccessibleProperty.LABEL,title,-1);return widget;}
        Gtk.Button action(string title,string name) {var widget=new Gtk.Button();widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-action");widget.valign=Gtk.Align.CENTER;var contents=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);var image=new Gtk.Image.from_icon_name(name);image.valign=Gtk.Align.CENTER;contents.append(image);contents.append(new Gtk.Label(title));widget.child=contents;return widget;}
        Gtk.MenuButton menu(string title,string[] options) {var widget=new Gtk.MenuButton();widget.label=title;widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-menu");widget.valign=Gtk.Align.CENTER;var model=new Menu();foreach(var option in options){var item=new MenuItem(option,null);item.set_action_and_target_value("toolbar.choice",new Variant.string(option));model.append_item(item);}widget.menu_model=model;return widget;}
    }
    public class ToolbarsFixture : Adw.ApplicationWindow {
        public ToolbarsFixture(Gtk.Application app,string mode="toolbars") {
            Object(application:app,title:"Majoris Toolbars",default_width:mode=="toolbars-narrow"?480:1280,default_height:420);
            var chrome=new Adw.ToolbarView();chrome.add_top_bar(new Adw.HeaderBar());var page=new ToolbarsPage(mode);chrome.content=page;content=chrome;
            if(Environment.get_variable("MAJORIS_TOOLBAR_PROBE")=="1")Timeout.add(700,()=>{stdout.printf("{\"window_width\":%d,\"entry\":%d,\"navigation\":%d,\"commands\":%d,\"back\":[%d,%d],\"location\":%d,\"crumb\":%d,\"search\":%d,\"switcher\":%d}\n",get_allocated_width(),page.location.entry.get_allocated_height(),page.navigation.get_allocated_height(),page.commands.get_allocated_height(),page.back.get_allocated_width(),page.back.get_allocated_height(),page.location.get_allocated_height(),page.location.crumbs.get_first_child().get_allocated_height(),page.search.get_allocated_height(),page.switcher.get_allocated_height());close();app.quit();return Source.REMOVE;});
            var action=new SimpleAction("toolbar-choice",null);action.activate.connect(()=>{});add_action(action);
        }
    }
}
