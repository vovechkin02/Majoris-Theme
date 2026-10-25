namespace MajorisThemeFactory {
    // Integration fixture, not an editor application; no appearance provider.
    public class EditorFixture : Adw.ApplicationWindow {
        public Adw.TabView documents;
        public Adw.TabBar tabs;
        public Gtk.Box toolbar;
        public Gtk.Box status;
        GLib.List<GtkSource.Buffer> buffers = new GLib.List<GtkSource.Buffer>();
        GLib.List<GtkSource.SearchContext> searches = new GLib.List<GtkSource.SearchContext>();
        GtkSource.StyleSchemeManager schemes;
        public EditorFixture(Gtk.Application app, string mode="editor") {
            Object(application:app,title:"Majoris Editor Components",default_width:900,default_height:650);
            var chrome=new Adw.ToolbarView(); var header=new Adw.HeaderBar();
            header.pack_end(menu_button()); chrome.add_top_bar(header);
            var layout=new Gtk.Box(Gtk.Orientation.VERTICAL,0);
            documents=new Adw.TabView(); documents.vexpand=true;
            tabs=new Adw.TabBar(); tabs.view=documents; tabs.autohide=false; tabs.expand_tabs=false;
            tabs.add_css_class("majoris-document-tabs"); layout.append(tabs);
            schemes=GtkSource.StyleSchemeManager.get_default();
            // Prefer installed discovery. A development checkout uses the same generated assets.
            if(schemes.get_scheme("majoris-light")==null) {
                var root=Environment.get_variable("MAJORIS_THEME_ROOT");
                if(root!=null) schemes.append_search_path(Path.build_filename(root,"gtksourceview-5","styles"));
            }
            toolbar=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4); toolbar.add_css_class("majoris-editor-toolbar");
            string[] names={"Bold","Italic","Underline","Heading","Bulleted list","Numbered list","Link"};
            string[] icons={"format-text-bold-symbolic","format-text-italic-symbolic","format-text-underline-symbolic","format-text-rich-symbolic","view-list-symbolic","view-list-ordered-symbolic","insert-link-symbolic"};
            for(int i=0;i<names.length;i++) {
                if(i==3 || i==6) { var separator=new Gtk.Separator(Gtk.Orientation.VERTICAL); separator.valign=Gtk.Align.CENTER; toolbar.append(separator); }
                var button=new Gtk.ToggleButton(); button.icon_name=icons[i]; button.tooltip_text=names[i]; button.valign=Gtk.Align.CENTER;
                if(i==0)button.active=true;
                if(mode=="editor-states") {
                    if(i==1)button.set_state_flags(Gtk.StateFlags.PRELIGHT,false);
                    if(i==2)button.set_state_flags(Gtk.StateFlags.ACTIVE,false);
                    if(i==3)button.set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);
                    if(i==4)button.sensitive=false;
                }
                toolbar.append(button);
            }
            var extra=selector("More",{"Insert code block","Insert image","Insert table"}); extra.tooltip_text="Additional editing actions"; toolbar.append(extra);
            var toolbar_scroll=new Gtk.ScrolledWindow(); toolbar_scroll.hscrollbar_policy=Gtk.PolicyType.EXTERNAL; toolbar_scroll.vscrollbar_policy=Gtk.PolicyType.NEVER; toolbar_scroll.child=toolbar;
            layout.append(toolbar_scroll);
            string[] titles={"Files","Favorites","Documents","notes.md","main.vala","Project Requirements.md"};
            for(int i=0;i<titles.length;i++) add_document(titles[i],titles[i].has_suffix(".md")?"markdown":(titles[i].has_suffix(".vala")?"vala":"plain"));
            var modified=documents.get_nth_page(5); modified.needs_attention=true; modified.indicator_icon=new ThemedIcon("document-save-symbolic"); modified.indicator_tooltip="Unsaved changes — application-owned indicator";
            documents.set_page_pinned(documents.get_nth_page(0),true);
            if(mode=="editor-overflow") foreach(var title in new string[]{"Find","Format","Downloads","Preferences","New Folder","Majoris-Theme-Implementation-Notes.txt","A Very Long Document Filename That Exceeds Normal Tab Width.txt"})add_document(title,"plain");
            if(mode=="editor-overflow") for(int i=0;i<14;i++) add_document("Document %d with a long filename.vala".printf(i+1),"vala");
            documents.selected_page=documents.get_nth_page(1);
            layout.append(documents);
            status=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4); status.add_css_class("majoris-statusbar");
            var position=new Gtk.Label("Ln 4, Col 12"); position.hexpand=true; position.xalign=0; status.append(position);
            var language=selector("Vala",{"Plain Text","Markdown","Vala","Python"}); status.append(language);
            var encoding=selector("UTF-8",{"UTF-8","UTF-16"}); status.append(encoding);
            var separator=new Gtk.Separator(Gtk.Orientation.VERTICAL); separator.valign=Gtk.Align.CENTER; status.append(separator);
            var endings=selector("LF",{"LF","CRLF"}); status.append(endings);
            var zoom=selector("100%",{"80%","100%","125%","200%"}); status.append(zoom);
            layout.append(status);
            bool compact=false;
            add_tick_callback((widget,clock)=>{bool next=get_width()<650;if(next!=compact){compact=next;encoding.visible=!compact;separator.visible=!compact;endings.visible=!compact;zoom.visible=!compact;}return Source.CONTINUE;});
            var manager=Adw.StyleManager.get_default(); manager.notify["dark"].connect(update_schemes); update_schemes();
            // GtkNotebook remains a separate factory page and retains its own stylesheet.
            chrome.content=layout; content=chrome; install_menu_actions(this);
            var action=new SimpleAction("new",null); action.activate.connect(()=>add_document("Untitled.txt","c")); add_action(action);
            var width=Environment.get_variable("MAJORIS_CONTENT_WIDTH"); if(width!=null)set_default_size(int.parse(width),650);
            if(Environment.get_variable("MAJORIS_EDITOR_SWITCH_PROBE")=="1") run_switch_probe();
            if(mode=="editor-source") Timeout.add(500,()=>{
                var scrolled=documents.selected_page.child as Gtk.ScrolledWindow;
                if(scrolled!=null)scrolled.child.grab_focus();
                return Source.REMOVE;
            });
            if(mode=="editor-states") Timeout.add(500,()=>{int index=0;hold_tab_states(tabs,ref index);return Source.REMOVE;});
            if(mode=="editor-focus") Timeout.add(500,()=>{focus_tab(tabs);return Source.REMOVE;});
        }
        void run_switch_probe() {
            string[] modes={"light","dark","light"}; int index=0;
            get_application().activate_action("scheme",new Variant.string(modes[0]));
            Timeout.add(220,()=>{
                var ids=new StringBuilder("["); bool first=true;
                foreach(var buffer in buffers) {
                    if(!first)ids.append(",");first=false;
                    ids.append("\"%s\"".printf(buffer.style_scheme==null?"missing":buffer.style_scheme.id));
                }
                ids.append("]");
                stdout.printf("{\"mode\":\"%s\",\"schemes\":%s,\"tab_height\":%d,\"toolbar_height\":%d,\"status_height\":%d}\n",modes[index],ids.str,tabs.get_allocated_height(),toolbar.get_allocated_height(),status.get_allocated_height());
                index++;
                if(index==modes.length) {var application=get_application();close();application.quit();return Source.REMOVE;}
                get_application().activate_action("scheme",new Variant.string(modes[index]));
                return Source.CONTINUE;
            });
        }
        void hold_tab_states(Gtk.Widget widget,ref int index) {
            if(widget.get_css_name()=="tab") {
                Gtk.StateFlags[] states={Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,Gtk.StateFlags.BACKDROP};
                if(index<states.length)widget.set_state_flags(states[index],false);index++;
            }
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling())hold_tab_states(c,ref index);
        }
        bool focus_tab(Gtk.Widget widget) {
            if(widget.get_css_name()=="tab") {widget.grab_focus();widget.set_state_flags(Gtk.StateFlags.FOCUS_VISIBLE,false);return true;}
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling()) if(focus_tab(c))return true;
            return false;
        }
        Gtk.MenuButton selector(string label,string[] choices) {
            var button=new Gtk.MenuButton(); button.label=label; button.valign=Gtk.Align.CENTER;
            var popover=new Gtk.Popover(); var choices_box=new Gtk.Box(Gtk.Orientation.VERTICAL,4);
            foreach(var choice in choices) {var item=new Gtk.Button.with_label(choice);item.clicked.connect(()=>{button.label=choice;popover.popdown();});choices_box.append(item);}
            popover.child=choices_box;button.popover=popover;return button;
        }
        void add_document(string title,string language) {
            var buffer=new GtkSource.Buffer(null); buffer.language=language=="plain"?null:GtkSource.LanguageManager.get_default().get_language(language);
            buffer.text="// Majoris native source preview\npublic class Document : Object {\n    public string title = \"Welcome to Majoris\";\n    public int count = 42;\n    // Readable comments and subtle current-line highlighting.\n    public void save () {\n        print (\"Document saved\\n\");\n    }\n}\n";
            if(language=="markdown")buffer.text="# Majoris documents\n\nA **native** editor with [links](https://example.org).\n\n- Document tabs\n- Shared toolbar\n\n```vala\nvar title = \"Majoris\";\n```\n";
            if(language=="python")buffer.text="# Majoris Python preview\nclass Document:\n    def __init__(self):\n        self.title = \"Welcome to Majoris\"\n        self.count = 42\n\n    def save(self):\n        print(\"Document saved\")\n";
            if(language=="plain")buffer.text="Welcome to Majoris.\n\nNative document tabs preserve keyboard navigation, reordering and closing.\nThe application owns document state and save confirmation.\n";
            var source=new GtkSource.View.with_buffer(buffer); source.monospace=true;source.show_line_numbers=true;source.highlight_current_line=true;source.show_right_margin=true;source.right_margin_position=80;source.top_margin=12;source.bottom_margin=12;source.left_margin=12;source.right_margin=12;
            var scroll=new Gtk.ScrolledWindow();scroll.child=source;
            var page=documents.append(scroll);page.title=title;page.tooltip=title;page.icon=new ThemedIcon("text-x-generic-symbolic");
            var settings=new GtkSource.SearchSettings();settings.search_text="Document";settings.wrap_around=true;
            var search=new GtkSource.SearchContext(buffer,settings);search.highlight=true;searches.append(search);buffers.append(buffer);
            Gtk.TextIter start,end;buffer.get_iter_at_offset(out start,31);buffer.get_iter_at_offset(out end,39);buffer.select_range(start,end);
            var scheme=schemes.get_scheme(Adw.StyleManager.get_default().dark?"majoris-dark":"majoris-light");buffer.style_scheme=scheme;
        }
        void update_schemes() {
            var scheme=schemes.get_scheme(Adw.StyleManager.get_default().dark?"majoris-dark":"majoris-light");
            foreach(var buffer in buffers)buffer.style_scheme=scheme;
        }
    }
}
