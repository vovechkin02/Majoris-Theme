namespace MajorisThemeFactory {
    public class ToolbarsPage : Gtk.Box {
        public Majoris.Ui.Toolbar navigation;
        public Majoris.Ui.Toolbar commands;
        public Gtk.Box switcher;
        public Majoris.Ui.Toolbar formatting;
        public Majoris.Ui.Toolbar media;
        public Gtk.Widget compact_sample;
        public Gtk.DropDown density_selector;
        public LocationBar location;
        public Gtk.SearchEntry search;
        public Gtk.Label result;
        public Gtk.Button back;
        public Gtk.Button forward;
        public Adw.TabBar? document_tabs;
        public ToolbarsPage(string mode="toolbars") {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:0);
            result=new Gtk.Label("Native toolbars — actions report here. Scroll either row at narrow widths."); result.wrap=true;result.add_css_class("majoris-toolbar-metadata");
            var actions=new SimpleActionGroup();var choice=new SimpleAction("choice",VariantType.STRING);choice.activate.connect((value)=>{var selected=value.get_string();result.label="Selected: "+selected;if(selected=="Documents" || selected=="Downloads")location.navigate("/home/demo/"+selected);if(selected=="Favorites")location.home();});actions.add_action(choice);insert_action_group("toolbar",actions);
            result.margin_top=16; result.margin_bottom=16;
            navigation=bar();navigation.add_css_class("majoris-toolbar-divider");
            var history=navigation.append_group();
            location=new LocationBar(); location.valign=Gtk.Align.CENTER;
            back=icon("go-previous-symbolic","Back");forward=icon("go-next-symbolic","Forward");history.append_control(back);history.append_control(forward);
            back.clicked.connect(()=>location.back());forward.clicked.connect(()=>location.forward());
            var up=icon("go-up-symbolic","Up");up.clicked.connect(()=>location.up());history.append_control(up);
            var places=menu("Locations",{"Favorites","Files","Documents","Downloads"});history.append_control(places);
            var refresh=icon("view-refresh-symbolic","Refresh");refresh.clicked.connect(()=>result.label="Refreshed "+location.path);history.append_control(refresh);
            location.navigated.connect(()=>{back.sensitive=location.can_back;forward.sensitive=location.can_forward;result.label="Location: "+location.path;});back.sensitive=false;forward.sensitive=false;
            navigation.append_widget(location);
            search=new Gtk.SearchEntry();search.add_css_class("majoris-toolbar-field");search.valign=Gtk.Align.CENTER;search.placeholder_text="Search"; search.width_request=160;
            search.search_changed.connect(()=>result.label=search.text==""?"Search cleared":"Search: "+search.text);navigation.append_control(search);
            append(viewport(navigation));
            commands=bar();commands.divider=true;var primary=commands.append_group();
            var create=action("New Folder","folder-new-symbolic");create.clicked.connect(()=>result.label="New Folder created (fixture)");primary.append_control(create);
            foreach(var name in new string[]{"Cut","Copy","Paste"}) {var button=icon(name=="Cut"?"edit-cut-symbolic":(name=="Copy"?"edit-copy-symbolic":"edit-paste-symbolic"),name);button.clicked.connect(()=>result.label=name+" activated");primary.append_control(button);}
            commands.append_separator();
            var secondary=commands.append_group();
            foreach(var name in new string[]{"Rename","Share","Trash"}) {var button=icon(name=="Rename"?"document-edit-symbolic":(name=="Share"?"send-to-symbolic":"user-trash-symbolic"),name);button.clicked.connect(()=>result.label=name+" activated");secondary.append_control(button);}
            commands.append_spacer();
            var view_group=commands.append_group();view_group.append_control(menu("Sort",{"Name","Date","Size"}));
            switcher=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);switcher.add_css_class("majoris-toolbar-segmented");switcher.valign=Gtk.Align.CENTER;
            Gtk.ToggleButton? leader=null;string[] views={"Grid","List","Columns","Gallery"};string[] icons={"view-grid-symbolic","view-list-symbolic","view-dual-symbolic","view-paged-symbolic"};
            for(int i=0;i<views.length;i++) {var toggle=new Gtk.ToggleButton();var glyph=new Gtk.Image.from_icon_name(icons[i]);glyph.pixel_size=16;glyph.valign=Gtk.Align.CENTER;glyph.halign=Gtk.Align.CENTER;toggle.child=glyph;toggle.tooltip_text=views[i];toggle.update_property(Gtk.AccessibleProperty.LABEL,views[i],-1);if(leader==null){leader=toggle;toggle.active=true;}else toggle.group=leader;string selected=views[i];toggle.toggled.connect(()=>{if(toggle.active)result.label="View: "+selected;});switcher.append(toggle);}
            view_group.append_widget(switcher);view_group.append_control(menu("View Settings",{"Show hidden files","Show thumbnails"}));
            var preview=icon("view-reveal-symbolic","Preview");preview.clicked.connect(()=>result.label="Preview toggled");view_group.append_control(preview);
            append(viewport(commands));append(result);
            var editor=bar(); formatting=editor; editor.compact=true;editor.divider=true;
            foreach(var name in new string[]{"Undo","Redo","Bold","Italic","Underline"}) {
                var button=new Gtk.ToggleButton.with_label(name); Majoris.Ui.Toolbar.set_item_flat(button);
                if(name=="Undo")compact_sample=button;
                button.toggled.connect(()=>result.label=name+(button.active?" enabled":" disabled")); editor.append_control(button);
            }
            var alignment=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);alignment.add_css_class("majoris-toolbar-segmented");alignment.valign=Gtk.Align.CENTER;
            Gtk.ToggleButton? alignment_leader=null;
            foreach(var name in new string[]{"Left","Centre","Right"}) {var button=new Gtk.ToggleButton.with_label(name);if(alignment_leader==null){alignment_leader=button;button.active=true;}else button.group=alignment_leader;alignment.append(button);}
            editor.append_widget(alignment);append(viewport(editor));
            var mixed=bar();media=mixed;mixed.divider=true;
            var play=icon("media-playback-start-symbolic","Play");var pause=icon("media-playback-pause-symbolic","Pause");mixed.append_control(play);mixed.append_control(pause);
            var progress=new Gtk.ProgressBar();progress.fraction=0.35;progress.hexpand=true;progress.valign=Gtk.Align.CENTER;progress.width_request=80;mixed.append_widget(progress);
            var time=new Gtk.Label("01:24 / 04:00");time.add_css_class("majoris-toolbar-metadata");mixed.append_widget(time);
            var spinner=new Gtk.Spinner();spinner.valign=Gtk.Align.CENTER;mixed.append_widget(spinner);
            play.clicked.connect(()=>{spinner.start();progress.fraction=double.min(1,progress.fraction+0.1);result.label="Playing";});pause.clicked.connect(()=>{spinner.stop();result.label="Paused";});
            var volume=new Gtk.Scale.with_range(Gtk.Orientation.HORIZONTAL,0,100,1);volume.set_value(60);volume.draw_value=false;volume.add_css_class("majoris-toolbar-scale");volume.width_request=80;volume.valign=Gtk.Align.CENTER;volume.update_property(Gtk.AccessibleProperty.LABEL,"Volume",-1);mixed.append_widget(volume);
            var selector=new Gtk.DropDown.from_strings({"Normal","Repeat","Shuffle"});mixed.append_control(selector);density_selector=selector;
            var extra_toggle=new Gtk.ToggleButton.with_label("Extra action");mixed.append_control(extra_toggle);
            var extra=new Gtk.Button.with_label("Queue");Majoris.Ui.Toolbar.set_item_flat(extra);extra.clicked.connect(()=>result.label="Queue opened");
            extra_toggle.toggled.connect(()=>{if(extra_toggle.active)mixed.append_control(extra);else mixed.remove_control(extra);});
            append(viewport(mixed));
            var field_row=bar();var entry=new Gtk.Entry();entry.add_css_class("majoris-toolbar-field");entry.placeholder_text="Native entry — Favorites / Files / Format";entry.hexpand=true;entry.valign=Gtk.Align.CENTER;field_row.append(entry);append(viewport(field_row));
            var keys=new Gtk.EventControllerKey();keys.propagation_phase=Gtk.PropagationPhase.CAPTURE;
            keys.key_pressed.connect((key,code,mods)=>{if(((mods&Gdk.ModifierType.CONTROL_MASK)!=0 && (key==Gdk.Key.l || key==Gdk.Key.L)) || ((mods&Gdk.ModifierType.ALT_MASK)!=0 && (key==Gdk.Key.d || key==Gdk.Key.D))){location.begin_edit();return true;}if((mods&Gdk.ModifierType.CONTROL_MASK)!=0 && (key==Gdk.Key.f || key==Gdk.Key.F)){search.grab_focus();return true;}return false;});add_controller(keys);
            if(mode=="toolbars-stacked" || mode=="toolbars-files-parent") {formatting.visible=false;media.visible=false;field_row.visible=false;}
            if(mode=="toolbars-dynamic")Timeout.add(400,()=>{extra_toggle.active=true;return Source.REMOVE;});
            if(mode=="toolbars-compact") {navigation.compact=true;commands.compact=true;media.compact=true;}
            if(mode=="toolbars-navigation" || mode=="toolbars-commands" || mode=="toolbars-editor" || mode=="toolbars-mixed") {
                navigation.visible=mode=="toolbars-navigation";commands.visible=mode=="toolbars-commands";
                formatting.visible=mode=="toolbars-editor";media.visible=mode=="toolbars-mixed";
                result.visible=false;field_row.visible=false;
            }
            if(mode=="toolbars-editing")Timeout.add(400,()=>{location.show_editing();return Source.REMOVE;});
            if(mode=="toolbars-states")Timeout.add(500,()=>{refresh.set_state_flags(Gtk.StateFlags.PRELIGHT,false);create.set_state_flags(Gtk.StateFlags.ACTIVE,false);preview.set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);return Source.REMOVE;});
            if(mode=="toolbars-popover")Timeout.add(600,()=>{places.popup();return Source.REMOVE;});
        }
        Majoris.Ui.Toolbar bar() {return new Majoris.Ui.Toolbar();}
        Majoris.Ui.ToolbarGroup group() {return new Majoris.Ui.ToolbarGroup();}
        Gtk.ScrolledWindow viewport(Gtk.Widget child) {var scroll=new Gtk.ScrolledWindow();scroll.hscrollbar_policy=Gtk.PolicyType.EXTERNAL;scroll.vscrollbar_policy=Gtk.PolicyType.NEVER;scroll.propagate_natural_height=true;scroll.child=child;return scroll;}
        Gtk.Button icon(string name,string title) {var widget=new Gtk.Button.from_icon_name(name);widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-icon");widget.valign=Gtk.Align.CENTER;widget.tooltip_text=title;widget.update_property(Gtk.AccessibleProperty.LABEL,title,-1);return widget;}
        Gtk.Button action(string title,string name) {var widget=new Gtk.Button();widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-action");widget.valign=Gtk.Align.CENTER;var contents=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);var image=new Gtk.Image.from_icon_name(name);image.valign=Gtk.Align.CENTER;contents.append(image);contents.append(new Gtk.Label(title));widget.child=contents;return widget;}
        Gtk.MenuButton menu(string title,string[] options) {var widget=new Gtk.MenuButton();widget.label=title;widget.add_css_class("majoris-toolbar-control");widget.add_css_class("majoris-toolbar-menu");widget.valign=Gtk.Align.CENTER;var model=new Menu();foreach(var option in options){var item=new MenuItem(option,null);item.set_action_and_target_value("toolbar.choice",new Variant.string(option));model.append_item(item);}widget.menu_model=model;return widget;}
    }
    public class ToolbarsFixture : Adw.ApplicationWindow {
        public ToolbarsFixture(Gtk.Application app,string mode="toolbars") {
            Object(application:app,title:"Majoris Toolbars",default_width:mode=="toolbars-narrow"?480:1280,default_height:480);
            var chrome=new Adw.ToolbarView();chrome.add_top_bar(new Adw.HeaderBar());var page=new ToolbarsPage(mode);if(mode=="toolbars-stacked" || mode=="toolbars-files-parent") {
                // Match Files: tabs are a top bar; the selected TabView page owns both rows.
                var documents=new Adw.TabView();documents.append(page).title="Files";
                documents.append(new Gtk.Box(Gtk.Orientation.VERTICAL,0)).title="Favorites";
                var tabs=new Adw.TabBar();tabs.view=documents;tabs.autohide=false;tabs.expand_tabs=false;
                tabs.add_css_class("majoris-document-tabs");page.document_tabs=tabs;
                if(mode=="toolbars-files-parent") {chrome.add_top_bar(tabs);chrome.content=documents;}
                else {
                    // Keep the native ToolbarView top-bar group's extra padding above
                    // the content, rather than between document tabs and browser rows.
                    var rows=new Gtk.Box(Gtk.Orientation.VERTICAL,0);
                    rows.append(tabs);rows.append(documents);documents.vexpand=true;chrome.content=rows;
                }
            } else chrome.content=page;content=chrome;
            if(Environment.get_variable("MAJORIS_TOOLBAR_PROBE")=="1")Timeout.add(700,()=>{Graphene.Rect nav_bounds,command_bounds;page.navigation.compute_bounds(this,out nav_bounds);page.commands.compute_bounds(this,out command_bounds);double origin=nav_bounds.origin.y;if(page.document_tabs!=null){Graphene.Rect tab_bounds;page.document_tabs.compute_bounds(this,out tab_bounds);origin=tab_bounds.origin.y;}stdout.printf("{\"tabs\":%d,\"navigation_y\":%g,\"commands_y\":%g,\"window_width\":%d,\"entry\":%d,\"navigation\":%d,\"commands\":%d,\"back\":[%d,%d],\"location\":%d,\"crumb\":%d,\"search\":%d,\"switcher\":%d,\"compact_toolbar\":%d,\"compact_button\":%d,\"mixed_toolbar\":%d,\"dropdown\":%d}\n",page.document_tabs==null?0:page.document_tabs.get_allocated_height(),nav_bounds.origin.y-origin,command_bounds.origin.y-origin,get_allocated_width(),page.location.entry.get_allocated_height(),page.navigation.get_allocated_height(),page.commands.get_allocated_height(),page.back.get_allocated_width(),page.back.get_allocated_height(),page.location.get_allocated_height(),page.location.crumbs.get_first_child().get_allocated_height(),page.search.get_allocated_height(),page.switcher.get_allocated_height(),page.formatting.get_allocated_height(),page.compact_sample.get_allocated_height(),page.media.get_allocated_height(),page.density_selector.get_allocated_height());close();app.quit();return Source.REMOVE;});
            var action=new SimpleAction("toolbar-choice",null);action.activate.connect(()=>{});add_action(action);
        }
    }
}
