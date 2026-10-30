namespace MajorisThemeFactory {
    public class ControlFlow : Gtk.Box {
        Gtk.FlowBox flow;
        public ControlFlow () {
            Object (orientation: Gtk.Orientation.VERTICAL);
            flow=new Gtk.FlowBox(); flow.halign=Gtk.Align.START; flow.selection_mode=Gtk.SelectionMode.NONE; flow.column_spacing=8; flow.row_spacing=8; flow.max_children_per_line=6;
            base.append(flow);
        }
        public new void append (Gtk.Widget widget) {
            widget.halign=Gtk.Align.START; widget.valign=Gtk.Align.CENTER;
            flow.append(widget);
        }
    }
    public class FactoryPage : Gtk.Box {
        public Adw.ToastOverlay? toast_overlay;
        public HashTable<string,Gtk.Widget> probes = new HashTable<string,Gtk.Widget>(str_hash,str_equal);
        public string filter;
        Gtk.Window owner;
        Gtk.Grid gallery;
        int section_count = 0;
        Gtk.Box section (string title, string id) {
            var card = new Gtk.Box (Gtk.Orientation.VERTICAL, 0); card.add_css_class ("card");
            var head=new Gtk.Box(Gtk.Orientation.VERTICAL,3); head.add_css_class("majoris-card-header");
            var label = new Gtk.Label(title); label.xalign=0; label.wrap=true; label.add_css_class("heading"); head.append(label); card.append(head);
            string description="";
            switch(id) {
                case "buttons":description="General control gallery using the verified state treatments.";break;
                case "selection":description="Checkboxes, radio buttons and switches use strong indigo only for selected/active state.";break;
                case "inputs":description="Entry, search entry, password entry, dropdown, spin input, colour and font selectors.";break;
                case "ranges":description="GTK scale, progress bar, level bar and spinner treatments.";break;
                case "preferences":description="Action row, switch row, combo row, entry row, spin row, expander row and button row equivalents.";break;
                case "navigation":description="Tabs and view switchers keep active state simple: text emphasis plus a small indigo indicator.";break;
                case "data":description="Majoris keeps dense desktop information views available instead of forcing every data view into oversized cards.";break;
                case "menus":description="Transient surfaces receive stronger elevation. Menu rows themselves remain flat.";break;
                case "feedback":description="Transient feedback remains compact; informational surfaces use soft colour rather than giant cards.";break;
            }
            var subtitle=new Gtk.Label(description);subtitle.xalign=0;subtitle.wrap=true;subtitle.add_css_class("majoris-card-description");if(description!="") head.append(subtitle);
            var inner = new Gtk.Box (Gtk.Orientation.VERTICAL,12); inner.add_css_class("majoris-card-body");
            card.append(inner);
            card.hexpand=true; card.valign=Gtk.Align.START;
            if(filter != "overview") { if(filter == id) gallery.attach(card,0,0,2,1); }
            else if(section_count<4) gallery.attach(card,section_count%2,section_count/2,1,1);
            else gallery.attach(card,0,section_count-2,2,1);
            section_count++; return inner;
        }
        Gtk.Box layout_card(string title,bool header,bool footer) {
            var card=new Gtk.Box(Gtk.Orientation.VERTICAL,0); card.add_css_class("card");
            if(header) {
                var head=new Gtk.Box(Gtk.Orientation.VERTICAL,0); head.add_css_class("majoris-card-header");
                var label=new Gtk.Label(title); label.xalign=0; label.wrap=true; label.add_css_class("heading"); head.append(label); card.append(head);
            }
            var body=new Gtk.Box(Gtk.Orientation.VERTICAL,8); body.add_css_class("majoris-card-body");
            var label=new Gtk.Label(header?"One padding owner; native control spacing is 8px.":title); label.wrap=true; label.xalign=0; body.append(label);
            var actions=row(); var action=icon_button("go-next-symbolic","Expand"); action.add_css_class("flat"); actions.append(action);
            actions.append(new Gtk.Button.with_label("Action")); body.append(actions); card.append(body);
            if(footer) {
                var foot=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4); foot.add_css_class("majoris-card-footer");
                foot.append(new Gtk.Button.with_label("Cancel")); var save=new Gtk.Button.with_label("Save"); save.add_css_class("suggested-action"); foot.append(save); card.append(foot);
            }
            return card;
        }
        ControlFlow row () { return new ControlFlow(); }
        public void show_toast () {
            var t=new Adw.Toast("File copied successfully."); t.button_label="Undo"; t.timeout=0;
            toast_overlay.add_toast(t);
        }
        public void show_dialog () {
            var d=new Adw.AlertDialog("Discard changes?","Your unsaved changes will be lost. This action cannot be undone.");
            d.content_width=360;
            d.add_response("cancel","Cancel"); d.add_response("discard","Discard");
            d.set_response_appearance("discard",Adw.ResponseAppearance.DESTRUCTIVE); d.present(owner);
        }
        public FactoryPage (Gtk.Window window, string selected = "overview") {
            Object (orientation: Gtk.Orientation.VERTICAL, spacing: 16);
            owner=window; filter=selected; add_css_class("majoris-page-content");
            // Native layout selects compact gutters and a single gallery column.
            bool compact=false;
            add_tick_callback((widget,clock)=>{
                bool next=get_width()<650;
                if(next!=compact) {
                    compact=next;
                    if(compact) add_css_class("majoris-compact"); else remove_css_class("majoris-compact");
                    if(filter=="overview") {
                        int index=0;
                        for(var child=gallery.get_first_child();child!=null;child=child.get_next_sibling()) {
                            var layout=(Gtk.GridLayoutChild)gallery.get_layout_manager().get_layout_child(child);
                            layout.column=compact?0:(index<4?index%2:0);
                            layout.row=compact?index:(index<4?index/2:index-2);
                            layout.column_span=compact?1:(index<4?1:2);
                            index++;
                        }
                    }
                }
                return Source.CONTINUE;
            });
            var title=new Gtk.Label("GTK & libadwaita Controls"); title.xalign=0; title.wrap=true; title.add_css_class("title-1"); append(title);
            var description=new Gtk.Label("Majoris control gallery with revised titlebar controls and verified interaction states."); description.xalign=0; description.wrap=true; var description_box=new Gtk.Box(Gtk.Orientation.VERTICAL,0); description_box.append(description); append(description_box);
            var hidden_banner=new Adw.Banner("Hidden banner must not leave a surface");
            hidden_banner.revealed=false; description_box.append(hidden_banner); probes.insert("hidden_banner",hidden_banner);
            gallery=new Gtk.Grid(); gallery.column_spacing=16; gallery.row_spacing=16; gallery.column_homogeneous=true; append(gallery);
            var buttons=section("Buttons & Actions","buttons"); var r=row(); buttons.append(r);
            string[] labels={"Default","Suggested","Destructive","Flat","Disabled"};
            string[] classes={"","suggested-action","destructive-action","flat",""};
            for(int i=0;i<labels.length;i++){var b=new Gtk.Button.with_label(labels[i]); if(classes[i]!="")b.add_css_class(classes[i]); b.sensitive=i!=4; r.append(b);}
            var normal_icon=icon_button("document-save-symbolic","Save — real GTK tooltip"); r.append(normal_icon); probes.insert("normal_icon_button",normal_icon); var flat_icon=icon_button("open-menu-symbolic","Flat icon button"); flat_icon.add_css_class("flat"); r.append(flat_icon); probes.insert("flat_icon_button",flat_icon);
            var split=new Adw.SplitButton(); split.label="Split button"; var sm=new Menu(); sm.append("New window","win.new"); split.menu_model=sm; r=row(); r.append(split); buttons.append(r);
            var segmented=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0); segmented.add_css_class("majoris-segmented");
            Gtk.ToggleButton? leader=null;
            foreach(var label in new string[]{"Day","Week","Month"}) { var segment=new Gtk.ToggleButton.with_label(label); if(leader==null){leader=segment;segment.active=true;}else segment.group=leader; segmented.append(segment); }
            segmented.halign=Gtk.Align.START; buttons.append(segmented);
            var selection=section("Selection","selection"); r=row(); selection.append(r);
            var check=new Gtk.CheckButton.with_label("Checkbox"); r.append(check);
            var checked=new Gtk.CheckButton.with_label("Checked"); checked.active=true; r.append(checked);
            var mixed=new Gtk.CheckButton.with_label("Indeterminate"); mixed.inconsistent=true; r.append(mixed);
            var radio=new Gtk.CheckButton.with_label("Radio A"); var radio2=new Gtk.CheckButton.with_label("Radio B"); radio2.group=radio; radio.active=true; r.append(radio); r.append(radio2);
            var off=new Gtk.Switch(); off.valign=Gtk.Align.CENTER; r.append(off); probes.insert("switch_off",off); var sw=new Gtk.Switch(); sw.valign=Gtk.Align.CENTER; sw.active=true; r.append(sw); probes.insert("switch",sw); var disabled_check=new Gtk.CheckButton.with_label("Disabled"); disabled_check.active=true; disabled_check.sensitive=false; r.append(disabled_check);
            var inputs=section("Inputs","inputs"); r=row(); inputs.append(r);
            var entry=new Gtk.Entry(); entry.text="Standard text entry"; r.append(entry); probes.insert("entry",entry);
            var search=new Gtk.SearchEntry(); r.append(search);
            var password=new Gtk.PasswordEntry(); password.show_peek_icon=true; r.append(password);
            r=row(); inputs.append(r); var chooser=new Gtk.DropDown.from_strings({"Dropdown","Automatic updates","Ask every time"}); r.append(chooser); probes.insert("dropdown",chooser); r.append(new Gtk.SpinButton.with_range(0,100,1)); var color_button=new Gtk.ColorButton(); Gdk.RGBA indigo=Gdk.RGBA(); indigo.parse("#6366F1"); color_button.rgba=indigo; r.append(color_button); var font_button=new Gtk.FontButton(); font_button.font="Plus Jakarta Sans 10"; r.append(font_button);
            var ranges=section("Ranges & Progress","ranges"); var scale=new Gtk.Scale.with_range(Gtk.Orientation.HORIZONTAL,0,100,1); scale.set_value(62); ranges.append(scale);
            var progress=new Gtk.ProgressBar(); progress.fraction=0.68; ranges.append(progress);
            var level=new Gtk.LevelBar.for_interval(0,8); level.mode=Gtk.LevelBarMode.DISCRETE; level.value=6; ranges.append(level); var spinner=new Gtk.Spinner(); spinner.halign=Gtk.Align.START; spinner.start(); ranges.append(spinner); var stopped=new Gtk.Spinner(); stopped.halign=Gtk.Align.START; ranges.append(stopped);
            var rows=section("Adwaita Boxed Lists & Preference Rows","preferences"); var list=new Gtk.ListBox(); list.add_css_class("boxed-list"); list.selection_mode=Gtk.SelectionMode.NONE; rows.append(list);
            var action=new Adw.ActionRow(); action.title="Action row"; action.subtitle="Native subtitle and suffix"; action.add_suffix(icon_button("go-next-symbolic","Open")); list.append(action);
            var switchrow=new Adw.SwitchRow(); switchrow.title="Switch row"; switchrow.active=true; list.append(switchrow);
            var combo=new Adw.ComboRow(); combo.title="Combo row"; combo.model=new Gtk.StringList({"Standard","Compact"}); list.append(combo);
            var er=new Adw.EntryRow(); er.title="Entry row"; list.append(er);
            var pr=new Adw.PasswordEntryRow(); pr.title="Password row"; list.append(pr);
            var sr=new Adw.SpinRow.with_range(0,100,1); sr.title="Spin row"; list.append(sr);
            var exp=new Adw.ExpanderRow(); exp.title="Expander row"; var nested=new Adw.ActionRow(); nested.title="Expanded detail"; exp.add_row(nested); list.append(exp); exp.expanded=true; var buttonrow=new Adw.ActionRow(); buttonrow.title="Button Row"; buttonrow.subtitle="A direct action inside preferences"; var suffix_button=new Gtk.Button.with_label("Configure"); suffix_button.valign=Gtk.Align.CENTER; buttonrow.add_suffix(suffix_button); list.append(buttonrow);
            var group=new Adw.PreferencesGroup(); group.title="Native PreferencesGroup";
            var plain=new Adw.ActionRow(); plain.title="Normal action"; group.add(plain);
            var toggled=new Adw.ActionRow(); toggled.title="Switch suffix"; toggled.subtitle="Centred native suffix";
            var suffix_switch=new Gtk.Switch(); suffix_switch.valign=Gtk.Align.CENTER; toggled.add_suffix(suffix_switch); group.add(toggled);
            var configured=new Adw.ActionRow(); configured.title="Button suffix";
            var configure=new Gtk.Button.with_label("Configure"); configure.valign=Gtk.Align.CENTER; configured.add_suffix(configure); group.add(configured);
            rows.append(group);
            var layouts=section("Shared Layout Components","layout");
            foreach(bool compact_demo in new bool[]{false,true}) {
                var demo_scroll=new Gtk.ScrolledWindow(); demo_scroll.hscrollbar_policy=Gtk.PolicyType.NEVER;
                demo_scroll.min_content_height=260; demo_scroll.max_content_height=360; demo_scroll.propagate_natural_height=true;
                var clamp=new Adw.Clamp();
                var content=new Gtk.Box(Gtk.Orientation.VERTICAL,16); content.add_css_class("majoris-page-content");
                if(compact_demo) content.add_css_class("majoris-compact");
                content.append(new Gtk.Label(compact_demo?"Compact gutters: 16px":"Desktop gutters: 24px"));
                content.append(layout_card("Header and body",true,false));
                content.append(layout_card("Header, body and footer",true,true));
                content.append(layout_card("Body only",false,false));
                var preference_card=new Gtk.Box(Gtk.Orientation.VERTICAL,0); preference_card.add_css_class("card");
                var preference_body=new Gtk.Box(Gtk.Orientation.VERTICAL,8); preference_body.add_css_class("majoris-card-body");
                var preference_group=new Adw.PreferencesGroup();
                var preference=new Adw.ActionRow(); preference.title="Preferences in a card"; preference.subtitle="Inset group retains its own list boundary";
                preference.add_suffix(icon_button("go-next-symbolic","Open preferences")); preference_group.add(preference);
                preference_body.append(preference_group); preference_card.append(preference_body); content.append(preference_card);
                clamp.child=content; demo_scroll.child=clamp; layouts.append(demo_scroll);
            }
            var nav=section("Navigation","navigation"); var ns=new Gtk.Stack(); ns.add_titled(new Gtk.Label("List content"),"list","List"); ns.add_titled(new Gtk.Label("Grid content"),"grid","Grid"); ns.add_titled(new Gtk.Label("Columns content"),"columns","Columns"); var switcher=new Gtk.StackSwitcher(); switcher.stack=ns; switcher.halign=Gtk.Align.START; nav.append(switcher); probes.insert("view_switcher",switcher); nav.append(ns);
            // Native segmented corner gallery: no replacement selection logic.
            for(int count=2;count<=4;count++) {
                for(int selected_index=0;selected_index<count;selected_index++) {
                    var segment_group=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);
                    segment_group.add_css_class("majoris-segmented"); segment_group.halign=Gtk.Align.START;
                    Gtk.ToggleButton? first=null;
                    for(int index=0;index<count;index++) {
                        var segment=new Gtk.ToggleButton.with_label("Page %d".printf(index+1));
                        if(first==null)first=segment;else segment.group=first;
                        segment.active=index==selected_index;
                        if(count==4 && index==2 && selected_index!=2)segment.sensitive=false;
                        segment_group.append(segment);
                    }
                    nav.append(segment_group);
                }
            }
            var view_stack=new Adw.ViewStack();
            foreach(var page_title in new string[]{"General","Metadata","Permissions","Open With"}) {
                var page=view_stack.add_titled(new Gtk.Label(page_title),page_title,page_title);
                page.icon_name="document-properties-symbolic";
            }
            var view_switch=new Adw.ViewSwitcher(); view_switch.policy=Adw.ViewSwitcherPolicy.WIDE;
            view_switch.stack=view_stack; view_switch.halign=Gtk.Align.START;nav.append(view_switch);nav.append(view_stack);
            var preferences_demo=new Gtk.Button.with_label("File Properties — native PreferencesDialog");
            preferences_demo.clicked.connect(()=>{
                var dialog=new Adw.PreferencesDialog();dialog.title="File Properties";
                foreach(var page_title in new string[]{"General","Metadata","Permissions","Open With"}) {
                    var page=new Adw.PreferencesPage();page.title=page_title;page.icon_name="document-properties-symbolic";
                    var segment_group=new Adw.PreferencesGroup();segment_group.title=page_title;
                    var setting=new Adw.ActionRow();setting.title="Native file properties";
                    segment_group.add(setting);page.add(segment_group);dialog.add(page);
                }
                dialog.present(owner);
            });
            nav.append(preferences_demo);
            var notebook=new Gtk.Notebook(); notebook.append_page(new Gtk.Label("Native GTK tab"),new Gtk.Label("Tab one")); notebook.append_page(new Gtk.Label("Second tab"),new Gtk.Label("Tab two")); nav.append(notebook); probes.insert("notebook",notebook);
            var data_card=section("Lists, Tables & Selection","data");
            var data_model=new GLib.ListStore(typeof(DataRecord));data_model.append(new DataRecord(0,"Documents"));data_model.append(new DataRecord(1,"Majoris Design.md"));data_model.append(new DataRecord(2,"Wallpaper.png"));
            var data_selection=new Gtk.SingleSelection(data_model); data_selection.selected=1;
            var data=new Gtk.ColumnView(data_selection); data.add_css_class("majoris-data-view"); data.add_css_class("majoris-data-boxed"); data.overflow=Gtk.Overflow.HIDDEN;
            string[] headings={"Name","Type","Date modified"};
            data.show_column_separators=true; data.show_row_separators=true;
            for(int i=0;i<headings.length;i++) {
                int column_index=i;
                var cell_factory=new Gtk.SignalListItemFactory();
                cell_factory.setup.connect((item)=>{((Gtk.ListItem)item).child=new DataCell("column",column_index==1?2:(column_index==2?1:0));});
                cell_factory.bind.connect((item)=>((DataCell)((Gtk.ListItem)item).child).bind_record((DataRecord)((Gtk.ListItem)item).item));
                cell_factory.unbind.connect((item)=>((DataCell)((Gtk.ListItem)item).child).unbind_record());
                var column=new Gtk.ColumnViewColumn(headings[i],cell_factory); column.expand=false;data.append_column(column);
            }
            for(uint c=0;c<3;c++){var column=(Gtk.ColumnViewColumn)data.columns.get_item(c);column.resizable=true;column.expand=c==0;column.fixed_width=c==0?192:160;}
            data_card.append(data);
            var feedback=section("Popover & Menu","menus"); r=row(); feedback.append(r); var file_menu=menu_button(); r.append(file_menu); var plain_model=new Menu(); plain_model.append("New Folder…","win.folder"); plain_model.append("Duplicate","win.duplicate"); plain_model.append("Preferences","win.preferences"); var plain_menu=new Gtk.MenuButton(); plain_menu.label="Menu without shortcuts"; plain_menu.menu_model=plain_model; r.append(plain_menu); var menu_dropdown=new Gtk.DropDown.from_strings({"Automatic","Ask every time","Never","Only on this device"}); r.append(menu_dropdown);
            var context_area=new Gtk.Label("Right-click for File actions"); context_area.hexpand=true; feedback.append(context_area); var context_button=menu_button(); context_button.halign=Gtk.Align.END; feedback.append(context_button); var context_click=new Gtk.GestureClick(); context_click.button=3; context_click.pressed.connect(()=>context_button.popup()); context_area.add_controller(context_click);
            var pop=new Gtk.MenuButton(); pop.label="Plain popover"; var p=new Gtk.Popover(); var pc=new Gtk.Box(Gtk.Orientation.VERTICAL,8); pc.append(new Gtk.Label("Native popover contents")); var destructive=new Gtk.Button.with_label("Move to Trash"); destructive.add_css_class("majoris-menu-danger"); pc.append(destructive); p.child=pc; pop.popover=p; r.append(pop);
            var toast=new Gtk.Button.with_label("Show toast"); toast.clicked.connect(()=>show_toast()); r.append(toast);
            var dialog=new Gtk.Button.with_label("Open alert dialog"); dialog.clicked.connect(()=>{show_dialog();}); r.append(dialog);
            var feedbackpage=section("Banner & Toast","feedback"); var banner=new Adw.Banner("A system update is ready to install."); banner.button_label="Install"; banner.revealed=true; feedbackpage.append(banner); var tb=new Gtk.Button.with_label("Show toast with Undo"); tb.clicked.connect(()=>show_toast()); feedbackpage.append(tb);
            if(filter=="overview") for(int i=0;i<12;i++) append(new Gtk.Label("Overlay scrollbar test row %d".printf(i+1)));
        }
    }
}
