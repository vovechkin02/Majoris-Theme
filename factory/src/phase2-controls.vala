namespace MajorisThemeFactory {
    public class Phase2Page : Gtk.Box {
        public Gtk.Calendar calendar;
        public Gtk.LinkButton link;
        public Gtk.EditableLabel editable;
        public Gtk.Paned split;
        public Gtk.FlowBox tiles;
        public Gtk.Expander expander;
        public Gtk.SearchBar searchbar;
        public Gtk.SearchEntry search;
        public Gtk.Label result;
        public Phase2Page(string mode="phase2") {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:16,margin_start:16,margin_end:16,margin_top:16,margin_bottom:16);
            result=new Gtk.Label("Native controls — changes report here");result.wrap=true;append(result);
            var dates=section("Calendar",mode,"calendar");
            calendar=new Gtk.Calendar();calendar.select_day(new DateTime.local(2026,10,15,12,0,0));calendar.mark_day(12);calendar.show_week_numbers=true;calendar.halign=Gtk.Align.START;
            calendar.day_selected.connect(()=>result.label="Selected "+calendar.get_date().format("%F"));dates.append(calendar);
            var popup_button=new Gtk.MenuButton();popup_button.label="Calendar in native popover";var popup=new Gtk.Popover();popup.child=new Gtk.Calendar();popup_button.popover=popup;dates.append(popup_button);
            var links=section("Links",mode,"links");var line=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);line.append(new Gtk.Button.with_label("Ordinary button"));
            link=safe_link("Open documentation");line.append(link);var visited=safe_link("Visited documentation");visited.visited=true;line.append(visited);var disabled=safe_link("Disabled link");disabled.sensitive=false;line.append(disabled);links.append(line);
            var inline_links=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4);inline_links.append(new Gtk.Label("Read the"));inline_links.append(safe_link("format guide"));inline_links.append(new Gtk.Label("before continuing."));links.append(inline_links);
            var edits=section("Inline editing",mode,"editable-label");editable=new Gtk.EditableLabel("Favorites Format gjpqy.txt");editable.add_css_class("majoris-editable-discoverable");editable.halign=Gtk.Align.START;edits.append(editable);
            var file_tile=new Gtk.Box(Gtk.Orientation.VERTICAL,4);file_tile.halign=Gtk.Align.START;file_tile.append(new Gtk.Image.from_icon_name("text-x-generic-symbolic"));file_tile.append(new Gtk.EditableLabel("Compact file — 日本語.txt"));edits.append(file_tile);
            var row=new Gtk.Box(Gtk.Orientation.HORIZONTAL,8);row.append(new Gtk.Label("List row:"));row.append(new Gtk.EditableLabel("Long filename with spaces, punctuation & accents é.txt"));edits.append(row);
            var title=new Gtk.EditableLabel("Document title — مرحبا");title.add_css_class("heading");edits.append(title);
            var splits=section("Splitters — drag or focus with F8",mode,"paned");split=new Gtk.Paned(Gtk.Orientation.HORIZONTAL);split.width_request=400;split.height_request=120;split.position=180;
            split.start_child=new Gtk.Label("Resizable start pane");var vertical=new Gtk.Paned(Gtk.Orientation.VERTICAL);vertical.start_child=new Gtk.Label("Upper pane");vertical.end_child=new Gtk.Entry();vertical.position=55;split.end_child=vertical;splits.append(split);
            var wide=new Gtk.Paned(Gtk.Orientation.HORIZONTAL);wide.wide_handle=true;wide.height_request=64;wide.start_child=new Gtk.Label("Wide hit target");wide.end_child=new Gtk.Label("RTL native layout");wide.set_direction(Gtk.TextDirection.RTL);splits.append(wide);
            var flows=section("Flow layouts",mode,"flowbox");var neutral=new Gtk.FlowBox();neutral.selection_mode=Gtk.SelectionMode.NONE;neutral.row_spacing=4;neutral.column_spacing=4;
            neutral.insert(new Gtk.Button.with_label("Neutral layout"),-1);neutral.insert(new Gtk.Switch(),-1);neutral.insert(new Gtk.Entry(),-1);flows.append(neutral);
            tiles=new Gtk.FlowBox();tiles.add_css_class("majoris-flow-tiles");tiles.selection_mode=Gtk.SelectionMode.MULTIPLE;tiles.row_spacing=8;tiles.column_spacing=8;tiles.max_children_per_line=6;tiles.min_children_per_line=1;
            foreach(var name in new string[]{"Favorites","Files","Format gjpqy","Pictures","日本語","مرحبا"})tiles.insert(new Gtk.Label(name),-1);
            tiles.selected_children_changed.connect(()=>result.label="Selected tiles: %u".printf(tiles.get_selected_children().length()));flows.append(tiles);tiles.select_child(tiles.get_child_at_index(1));
            var expanders=section("Expanders",mode,"expander");expander=new Gtk.Expander("General expander");var form=new Gtk.Box(Gtk.Orientation.VERTICAL,8);form.append(new Gtk.Entry());var nested=new Gtk.Expander("Nested native expander");nested.child=new Gtk.Label("Natural content height");form.append(nested);expander.child=form;expanders.append(expander);
            var expanded=new Gtk.Expander("Expanded with a long descriptive title — Format gjpqy");expanded.child=new Gtk.Label("Content has no automatic nested card");expanded.expanded=true;expanders.append(expanded);
            var unavailable=new Gtk.Expander("Disabled expander");unavailable.sensitive=false;expanders.append(unavailable);
            var sidebar=new Gtk.Box(Gtk.Orientation.VERTICAL,0);sidebar.add_css_class("majoris-sidebar");var specialised=new Gtk.Expander("Sidebar comparison");specialised.add_css_class("majoris-sidebar-group");specialised.child=new Gtk.Label("Existing sidebar indentation remains authoritative");sidebar.append(specialised);expanders.append(sidebar);
            var search_section=section("Search container",mode,"searchbar");var reveal=new Gtk.ToggleButton.with_label("Search");search_section.append(reveal);
            searchbar=new Gtk.SearchBar();searchbar.show_close_button=true;search=new Gtk.SearchEntry();search.placeholder_text="Favorites Files Format gjpqy";searchbar.child=search;searchbar.connect_entry(search);
            reveal.bind_property("active",searchbar,"search-mode-enabled",BindingFlags.BIDIRECTIONAL);search.search_changed.connect(()=>result.label="Search: "+search.text);search_section.append(searchbar);
            map.connect(connect_search_capture);unmap.connect(disconnect_search_capture);
            result.label="Interact with the controls below.";
            if(mode=="phase2-calendar-popover"){dates.visible=true;Timeout.add(400,()=>{popup_button.popup();return Source.REMOVE;});}
            if(mode=="phase2-searchbar")reveal.active=true;
            if(mode=="phase2-editing"){edits.visible=true;Timeout.add(400,()=>{editable.start_editing();return Source.REMOVE;});}
            if(mode=="phase2-states")Timeout.add(400,()=>{link.set_state_flags(Gtk.StateFlags.PRELIGHT,false);editable.start_editing();expander.expanded=true;searchbar.search_mode_enabled=true;return Source.REMOVE;});
        }
        void connect_search_capture(){searchbar.set_key_capture_widget(get_root() as Gtk.Widget);}
        void disconnect_search_capture(){searchbar.set_key_capture_widget(null);}
        Gtk.LinkButton safe_link(string label) {var item=new Gtk.LinkButton.with_label("https://example.invalid/majoris",label);item.valign=Gtk.Align.CENTER;item.activate_link.connect(()=>{result.label="URI activation handled safely by the fixture";item.visited=true;return true;});return item;}
        Gtk.Box section(string title,string mode,string id) {var box=new Gtk.Box(Gtk.Orientation.VERTICAL,8);var heading=new Gtk.Label(title);heading.add_css_class("heading");heading.xalign=0;box.append(heading);append(box);if(mode!="phase2" && mode!="phase2-states" && mode!="phase2-"+id)box.visible=false;return box;}
    }
    public class Phase2Fixture : Adw.ApplicationWindow {
        public Phase2Fixture(Gtk.Application app,string mode) {
            Object(application:app,title:"Majoris Phase 2 Controls",default_width:900,default_height:760);
            var chrome=new Adw.ToolbarView();chrome.add_top_bar(new Adw.HeaderBar());var scroll=new Gtk.ScrolledWindow();var page=new Phase2Page(mode);scroll.child=page;chrome.content=scroll;content=chrome;
        }
    }
}

