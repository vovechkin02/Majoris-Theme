namespace MajorisThemeFactory {
    public class DataRecord : Object {
        public uint identity {get;set;}
        public string name {get;set;}
        public string kind {get;set;}
        public int64 modified {get;set;}
        public int64 bytesize {get;set;}
        public string icon {get;set;}
        public string thumbnail {get;set;default="";}
        public DataRecord(uint id,string title) {
            identity=id;name=title;kind=title.contains(".")?"Document":"Folder";if(title.has_suffix(".png"))kind="Image";if(title.has_suffix(".pdf"))kind="PDF document";
            modified=20261026-id%24;bytesize=(id+1)*1024;icon=kind=="Folder"?"folder-symbolic":(kind=="Image"?"image-x-generic-symbolic":"text-x-generic-symbolic");
            if(id==4){thumbnail="missing.svg";kind="Plain text document with an exceptionally long descriptive content type";}if(id==5){kind="Unknown";icon="text-x-generic-symbolic";}
            if(id==2)thumbnail="landscape.svg";if(id==6)thumbnail="portrait.svg";if(id==7)thumbnail="square.svg";
        }
    }
    public class DataCell : Gtk.Box {
        public Gtk.Label label;
        public Gtk.Image icon;
        public Gtk.Box artwork;
        public Gtk.Picture picture;
        Gtk.AspectFrame? thumbnail_frame;
        public DataRecord? record;
        public string family;
        public int column;
        ulong thumbnail_handler=0;
        public DataCell(string mode,int col=0,bool compact=false) {
            Object(orientation:mode=="grid"?Gtk.Orientation.VERTICAL:Gtk.Orientation.HORIZONTAL,spacing:8);
            family=mode;column=col;add_css_class("majoris-data-cell");
            label=new Gtk.Label("");label.xalign=mode=="grid"?0.5f:0;label.valign=Gtk.Align.CENTER;label.hexpand=mode!="grid";label.ellipsize=Pango.EllipsizeMode.END;
            icon=new Gtk.Image();icon.valign=Gtk.Align.CENTER;icon.halign=Gtk.Align.CENTER;
            artwork=new Gtk.Box(Gtk.Orientation.VERTICAL,0);artwork.add_css_class("majoris-data-artwork");artwork.halign=Gtk.Align.CENTER;artwork.valign=Gtk.Align.CENTER;
            picture=new Gtk.Picture();picture.content_fit=Gtk.ContentFit.CONTAIN;picture.can_shrink=true;picture.add_css_class("majoris-data-thumbnail");picture.overflow=Gtk.Overflow.HIDDEN;
            if(mode=="grid") {
                add_css_class("majoris-data-tile");halign=Gtk.Align.CENTER;valign=Gtk.Align.START;
                var overlay=new Gtk.Overlay();overlay.hexpand=true;overlay.vexpand=true;overlay.child=icon;thumbnail_frame=new Gtk.AspectFrame(0.5f,0.5f,1.0f,false);thumbnail_frame.add_css_class("majoris-data-artwork-frame");thumbnail_frame.child=picture;overlay.add_overlay(thumbnail_frame);picture.halign=Gtk.Align.FILL;picture.valign=Gtk.Align.FILL;
                artwork.append(overlay);artwork.vexpand=false;append(artwork);label.justify=Gtk.Justification.CENTER;label.yalign=0;label.wrap=true;label.wrap_mode=Pango.WrapMode.WORD_CHAR;label.lines=2;label.max_width_chars=1;append(label);
            } else {if(col==0)append(icon);append(label);if(col>0)label.add_css_class("majoris-data-metadata");}
            if(family=="grid")label.notify["attributes"].connect(()=>reserve_caption());
            configure(compact);
        }
        void reserve_caption(){if(family!="grid")return;var metrics=label.create_pango_layout("Agjpqy\nAgjpqy");metrics.set_attributes(label.attributes);Pango.Rectangle ink,logical;metrics.get_pixel_extents(out ink,out logical);if(label.height_request!=logical.height)label.height_request=logical.height;}
        public void configure(bool compact) {reserve_caption();label.xalign=family=="grid"?0.5f:(get_direction()==Gtk.TextDirection.RTL?1:0);icon.pixel_size=family=="grid"?(compact?32:64):16;if(family=="grid")label.width_request=compact?80:112;}
        public void bind_record(DataRecord value) {
            unbind_record();record=value;tooltip_text=value.name;
            if(column==0)label.label=value.name;else if(column==1)label.label="%04lld-%02lld-%02lld".printf(value.modified/10000,(value.modified/100)%100,value.modified%100);else if(column==2)label.label=value.kind;else label.label="%lld KB".printf(value.bytesize/1024);
            string accessible_text=value.name;if(column>0)accessible_text=value.name+", "+label.label;label.update_property(Gtk.AccessibleProperty.LABEL,accessible_text,-1);
            icon.icon_name=value.icon;update_artwork();
            if(family=="grid")thumbnail_handler=value.notify["thumbnail"].connect(()=>update_artwork());
        }
        void update_artwork() {
            picture.paintable=null;picture.visible=false;icon.visible=true;
            if(family!="grid")return;
            if(record==null || record.thumbnail=="")return;
            var asset_root=Environment.get_variable("MAJORIS_DATA_ASSET_ROOT")??Path.build_filename(Environment.get_current_dir(),"factory","data","thumbnails");
            if(!FileUtils.test(asset_root,FileTest.IS_DIR))foreach(var directory in Environment.get_system_data_dirs()){
                var candidate=Path.build_filename(directory,"majoris-theme","thumbnails");if(FileUtils.test(candidate,FileTest.IS_DIR)){asset_root=candidate;break;}
            }
            try {var texture=Gdk.Texture.from_filename(Path.build_filename(asset_root,record.thumbnail));if(thumbnail_frame!=null)thumbnail_frame.ratio=(float)texture.get_width()/texture.get_height();picture.paintable=texture;picture.visible=true;icon.visible=false;}catch(Error e){/* Missing thumbnail keeps the aligned fallback icon. */}
        }
        public void unbind_record() {
            if(record!=null && thumbnail_handler!=0)record.disconnect(thumbnail_handler);
            thumbnail_handler=0;record=null;tooltip_text=null;label.label="";label.reset_property(Gtk.AccessibleProperty.LABEL);picture.paintable=null;picture.visible=false;icon.clear();
        }
    }
    public class DataViewsPage : Gtk.Box {
        public DataViewsPage(Gtk.Application app) {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:16);add_css_class("majoris-page-content");
            var title=new Gtk.Label("Data Views");title.add_css_class("title-1");title.xalign=0;append(title);
            var launch=new Gtk.Button.with_label("Open native Grid, List and Details");launch.halign=Gtk.Align.START;launch.clicked.connect(()=>new DataViewsFixture(app).present());append(launch);
            var stress=new Gtk.Button.with_label("Open 1,200-item virtualization fixture");stress.halign=Gtk.Align.START;stress.clicked.connect(()=>new DataViewsFixture(app,"data-grid-stress").present());append(stress);
        }
    }
    public class DataViewsFixture : Adw.ApplicationWindow {
        public GLib.ListStore store;
        public Gtk.SortListModel sorted;
        public Gtk.SelectionModel selection;
        public Gtk.ListView list;
        public Gtk.GridView grid;
        public Gtk.ColumnView column;
        public Gtk.Stack stack;
        public Gtk.ToggleButton compact_button;
        public Gtk.ToggleButton multi_button;
        Gtk.ToggleButton[] mode_buttons;
        Gtk.ColumnViewColumn[] columns;
        Gtk.Label status;
        bool compact=false;
        public uint setups=0;
        public uint binds=0;
        public uint unbinds=0;
        uint activated=0;
        bool preserving=false;
        string mode_name="grid";
        public DataViewsFixture(Gtk.Application app,string mode="data-grid") {
            Object(application:app,title:"Majoris Data Views",default_width:1000,default_height:720);
            if(mode.contains("rtl"))Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL);
            compact=mode.contains("compact");
            store=new GLib.ListStore(typeof(DataRecord));
            string[] names={"Documents","Downloads","Photos","Majoris Design.md","Majoris-Theme-Implementation-Notes.txt","A Very Long Filename That Exceeds The Available View Width.txt","Wallpaper.png","Project Requirements.pdf","Favorites","Files","Folders","Find","Format","Properties","gjpqy","ABCDEFGHIJKLMNOPQRSTUVWXYZ"};
            int count=mode.contains("stress")?1200:64;
            for(int i=0;i<count;i++)store.append(new DataRecord((uint)i,i<names.length?names[i]:"File %04d.txt".printf(i)));
            sorted=new Gtk.SortListModel(store,null);selection=new Gtk.SingleSelection(sorted);
            grid=new Gtk.GridView(null,item_factory("grid"));grid.add_css_class("majoris-data-grid");grid.min_columns=1;grid.max_columns=12;
            list=new Gtk.ListView(null,item_factory("list"));list.add_css_class("majoris-data-list");
            column=new Gtk.ColumnView(null);column.add_css_class("majoris-data-column");column.add_css_class("majoris-data-view");column.show_row_separators=true;column.show_column_separators=false;
            string[] titles={"Name","Date modified","Type","Size"};int[] widths={192,160,128,96};
            for(int i=0;i<4;i++) {
                int index=i;var c=new Gtk.ColumnViewColumn(titles[i],item_factory("column",i));c.fixed_width=widths[i];c.expand=i==0;c.resizable=true;
                c.sorter=new Gtk.CustomSorter((a,b)=>{var x=(DataRecord)a;var y=(DataRecord)b;if(index==0)return strcmp(x.name,y.name);if(index==2)return strcmp(x.kind,y.kind);int64 delta=index==1?x.modified-y.modified:x.bytesize-y.bytesize;return delta<0?-1:(delta>0?1:0);});
                column.append_column(c);columns+=c;
            }
            // Subscribe before SortListModel so selected identities are captured
            // before reordered items are published. Restore through native selection.
            column.sorter.changed.connect(()=>preserve_sort_selection());sorted.sorter=column.sorter;
            stack=new Gtk.Stack();stack.hhomogeneous=false;stack.vhomogeneous=false;stack.vexpand=true;
            Gtk.Widget[] views={grid,list,column};string[] modes={"grid","list","column"};
            for(int i=0;i<3;i++){var scroller=new Gtk.ScrolledWindow();scroller.hscrollbar_policy=i==2?Gtk.PolicyType.AUTOMATIC:Gtk.PolicyType.NEVER;scroller.child=views[i];stack.add_named(scroller,modes[i]);}
            var root=new Gtk.Box(Gtk.Orientation.VERTICAL,0);var controls=new ControlFlow();controls.margin_top=12;controls.margin_bottom=12;controls.margin_start=16;controls.margin_end=16;
            var segmented=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);segmented.add_css_class("majoris-segmented");Gtk.ToggleButton? leader=null;
            for(int i=0;i<3;i++){string target=modes[i];var button=new Gtk.ToggleButton.with_label(i==0?"Grid":(i==1?"List":"Details"));if(leader==null)leader=button;else button.group=leader;button.toggled.connect(()=>{if(button.active){activate_view(target);}});segmented.append(button);mode_buttons+=button;}
            controls.append(segmented);
            compact_button=new Gtk.ToggleButton.with_label("Compact");compact_button.active=compact;compact_button.toggled.connect(()=>{compact=compact_button.active;apply_density();});controls.append(compact_button);
            multi_button=new Gtk.ToggleButton.with_label("Multiple selection");multi_button.toggled.connect(()=>change_selection(multi_button.active));controls.append(multi_button);
            var direction=new Gtk.Button.with_label("Reverse sort");bool descending=false;direction.clicked.connect(()=>{descending=!descending;column.sort_by_column(columns[0],descending?Gtk.SortType.DESCENDING:Gtk.SortType.ASCENDING);});controls.append(direction);
            status=new Gtk.Label("Native selection, sorting, resizing and recycled item factories");status.xalign=0;status.margin_start=16;status.margin_bottom=8;root.append(controls);root.append(status);root.append(stack);
            var toolbar=new Adw.ToolbarView();var header=new Adw.HeaderBar();header.title_widget=new Gtk.Label("Data Views");header.pack_end(menu_button());toolbar.add_top_bar(header);toolbar.content=root;content=toolbar;
            install_menu_actions(this);((SimpleAction)lookup_action("open")).set_enabled(false);((SimpleAction)lookup_action("preview")).set_enabled(false);
            grid.activate.connect((pos)=>activate_item(pos));list.activate.connect((pos)=>activate_item(pos));column.activate.connect((pos)=>activate_item(pos));
            mode_name=mode.contains("column")?"column":(mode.contains("list")?"list":"grid");mode_buttons[mode_name=="grid"?0:(mode_name=="list"?1:2)].active=true;stack.visible_child_name=mode_name;
            apply_density();selection.select_item(1,true);
            if(mode.contains("multi")){multi_button.active=true;selection.select_item(1,false);selection.select_item(2,false);}
            if(mode.contains("disabled-sort"))columns[3].sorter=null;
            if(mode.contains("disabled" ) && !mode.contains("disabled-sort")){grid.sensitive=false;list.sensitive=false;column.sensitive=false;}
            if(mode.contains("sorted"))column.sort_by_column(columns[0],Gtk.SortType.ASCENDING);
            if(mode.contains("resized")){columns[0].expand=false;columns[0].fixed_width=260;}
            if(mode.contains("narrow"))set_default_size(390,720);
            if(mode.contains("rtl"))set_direction_recursive(this,Gtk.TextDirection.RTL);
            if(mode.contains("backdrop"))Timeout.add(1000,()=>{var target=new Adw.ApplicationWindow(app);target.title="Data backdrop target";target.default_width=220;target.default_height=100;target.content=new Gtk.Label("Inactive-window selection");target.present();return Source.REMOVE;});
            if(mode.contains("focus") || mode.contains("states"))Timeout.add(900,()=>{var view=mode_name=="grid"?(Gtk.Widget)grid:(mode_name=="list"?(Gtk.Widget)list:column);var items=find_nodes(view,mode_name=="grid"?"child":"row");if(items.length>2){items[2].grab_focus();items[2].set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);if(mode.contains("states")){items[0].set_state_flags(Gtk.StateFlags.PRELIGHT,false);items[1].set_state_flags(Gtk.StateFlags.PRELIGHT,false);}}return Source.REMOVE;});
            var diagnostic=Environment.get_variable("MAJORIS_DATA_STATE");
            if(diagnostic!=null && diagnostic!="backdrop")Timeout.add(900,()=>{
                var view=mode_name=="grid"?(Gtk.Widget)grid:(mode_name=="list"?(Gtk.Widget)list:column);
                var nodes=find_nodes(view,mode_name=="grid"?"child":"row");
                if(nodes.length<3)return Source.CONTINUE;
                var target=nodes[diagnostic.contains("selected")?1:0];
                if(diagnostic.contains("hover"))target.set_state_flags(Gtk.StateFlags.PRELIGHT,false);
                if(diagnostic.contains("pressed"))target.set_state_flags(Gtk.StateFlags.ACTIVE,false);
                if(diagnostic.contains("focus")){target.grab_focus();target.set_state_flags(Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,false);selection.select_item(1,true);}
                if(diagnostic=="disabled")target.sensitive=false;
                return Source.REMOVE;
            });
            if(mode.contains("large"))Timeout.add(800,()=>{enlarge(stack);return Source.REMOVE;});
            // A single application timer simulates completed thumbnail delivery.
            Timeout.add(1200,()=>{((DataRecord)store.get_item(3)).thumbnail="landscape.svg";return Source.REMOVE;});
            var report=Environment.get_variable("MAJORIS_DATA_REPORT");if(report!=null)Timeout.add(200,()=>{write_report(report);return Source.CONTINUE;});
        }
        Gtk.SignalListItemFactory item_factory(string family,int col=0) {
            var f=new Gtk.SignalListItemFactory();
            f.setup.connect((obj)=>{setups++;((Gtk.ListItem)obj).child=new DataCell(family,col,compact);});
            f.bind.connect((obj)=>{binds++;var item=(Gtk.ListItem)obj;((DataCell)item.child).configure(compact);((DataCell)item.child).bind_record((DataRecord)item.item);});
            f.unbind.connect((obj)=>{unbinds++;((DataCell)((Gtk.ListItem)obj).child).unbind_record();});return f;
        }
        void activate_view(string target){mode_name=target;grid.model=mode_name=="grid"?selection:null;list.model=mode_name=="list"?selection:null;column.model=mode_name=="column"?selection:null;stack.visible_child_name=mode_name;}
        void activate_item(uint pos){activated++;status.label="Activated: "+((DataRecord)sorted.get_item(pos)).name;}
        DataRecord[] selected_records(){DataRecord[] values={};for(uint i=0;i<sorted.get_n_items();i++)if(selection.is_selected(i))values+=(DataRecord)sorted.get_item(i);return values;}
        void restore_records(DataRecord[] values){selection.unselect_all();for(uint i=0;i<sorted.get_n_items();i++)foreach(var record in values)if(sorted.get_item(i)==record)selection.select_item(i,false);}
        void preserve_sort_selection(){if(preserving)return;preserving=true;var values=selected_records();Idle.add(()=>{restore_records(values);preserving=false;return Source.REMOVE;});}
        void change_selection(bool multi){var values=selected_records();selection=multi?(Gtk.SelectionModel)new Gtk.MultiSelection(sorted):(Gtk.SelectionModel)new Gtk.SingleSelection(sorted);activate_view(mode_name);restore_records(values);}
        void apply_density(){foreach(var view in new Gtk.Widget[]{grid,list,column}){if(compact)view.add_css_class("majoris-density-compact");else view.remove_css_class("majoris-density-compact");configure_cells(view);}}
        void configure_cells(Gtk.Widget w){if(w is DataCell)((DataCell)w).configure(compact);for(var c=w.get_first_child();c!=null;c=c.get_next_sibling())configure_cells(c);}
        void set_direction_recursive(Gtk.Widget w,Gtk.TextDirection d){w.set_direction(d);if(w is Gtk.Label){var parent=w.get_parent() as DataCell;((Gtk.Label)w).xalign=parent!=null && parent.family=="grid"?0.5f:(d==Gtk.TextDirection.RTL?1:0);}for(var c=w.get_first_child();c!=null;c=c.get_next_sibling())set_direction_recursive(c,d);}
        void enlarge(Gtk.Widget w){if(w is Gtk.Label){var a=new Pango.AttrList();a.insert(Pango.attr_scale_new(1.5));((Gtk.Label)w).attributes=a;}for(var c=w.get_first_child();c!=null;c=c.get_next_sibling())enlarge(c);}
        string css_name(Gtk.Widget w){string name;w.get("css-name",out name);return name;}
        Gtk.Widget[] find_nodes(Gtk.Widget w,string name){Gtk.Widget[] items={};if(css_name(w)==name)items+=w;for(var c=w.get_first_child();c!=null;c=c.get_next_sibling())foreach(var item in find_nodes(c,name))items+=item;return items;}
        string bounds(Gtk.Widget w){Graphene.Rect r;w.compute_bounds(this,out r);return "[%g,%g,%g,%g]".printf(r.origin.x,r.origin.y,r.size.width,r.size.height);}
        string quote(string s){return "\""+s.replace("\\","\\\\").replace("\"","\\\"").replace("\n","\\n")+"\"";}
        void cells_report(Gtk.Widget w,StringBuilder json,ref bool first){
            var cell=w as DataCell;
            if(cell!=null && cell.record!=null && cell.get_mapped()){
                if(!first)json.append(",");first=false;var font=cell.label.get_pango_context().get_font_description();Pango.Rectangle ink,logical;cell.label.get_layout().get_pixel_extents(out ink,out logical);
                var owner=cell.get_parent();if(css_name(owner)=="cell")owner=owner.get_parent();
                json.append("{\"id\":%u,\"name\":%s,\"text\":%s,\"tooltip\":%s,\"family\":%s,\"column\":%d,\"bounds\":%s,\"owner\":%s,\"label\":%s,\"icon\":%s,\"artwork\":%s,\"picture\":%s,\"thumbnail\":%s,\"font\":%s,\"size\":%g,\"weight\":%d,\"ink\":[%d,%d,%d,%d],\"logical\":[%d,%d,%d,%d],\"baseline\":%d,\"ellipsized\":%s,\"lines\":%d,\"selected\":%s,\"flags\":%u,\"role\":%s}".printf(cell.record.identity,quote(cell.record.name),quote(cell.label.label),quote(cell.tooltip_text??""),quote(cell.family),cell.column,bounds(cell),bounds(owner),bounds(cell.label),bounds(cell.icon),bounds(cell.artwork),bounds(cell.picture),quote(cell.record.thumbnail),quote(font.to_string()),(double)font.get_size()/Pango.SCALE,(int)font.get_weight(),ink.x,ink.y,ink.width,ink.height,logical.x,logical.y,logical.width,logical.height,cell.label.get_layout().get_baseline()/Pango.SCALE,cell.label.get_layout().is_ellipsized().to_string(),cell.label.get_layout().get_line_count(),selection.is_selected(find_position(cell.record)).to_string(),(uint)owner.get_state_flags(),quote(((Gtk.Accessible)owner).get_accessible_role().to_string())));
            }
            for(var c=w.get_first_child();c!=null;c=c.get_next_sibling())cells_report(c,json,ref first);
        }
        uint find_position(DataRecord r){for(uint i=0;i<sorted.get_n_items();i++)if(sorted.get_item(i)==r)return i;return uint.MAX;}
        void write_report(string path){
            var json=new StringBuilder("{");json.append("\"active\":%s,\"window_bounds\":%s,\"mode\":%s,\"compact\":%s,\"multi\":%s,\"count\":%u,\"setups\":%u,\"binds\":%u,\"unbinds\":%u,\"activated\":%u,\"view\":%s,\"controls\":[".printf(is_active.to_string(),bounds(this),quote(mode_name),compact.to_string(),multi_button.active.to_string(),sorted.get_n_items(),setups,binds,unbinds,activated,bounds(stack)));
            foreach(var b in mode_buttons){if(b!=mode_buttons[0])json.append(",");json.append(bounds(b));}json.append(","+bounds(compact_button)+","+bounds(multi_button)+"],\"selected\":[");bool first=true;
            foreach(var r in selected_records()){if(!first)json.append(",");first=false;json.append(r.identity.to_string());}json.append("],\"order\":[");for(uint i=0;i<uint.min(16,sorted.get_n_items());i++){if(i>0)json.append(",");json.append(((DataRecord)sorted.get_item(i)).identity.to_string());}json.append("],\"widths\":[");for(int i=0;i<4;i++){if(i>0)json.append(",");json.append(columns[i].fixed_width.to_string());}json.append("],\"headers\":[");first=true;
            var header=find_nodes(column,"header");if(header.length>0)for(var c=header[0].get_first_child();c!=null;c=c.get_next_sibling()){if(!first)json.append(",");first=false;json.append(bounds(c));}
            json.append("],\"header_bounds\":%s,\"header_fonts\":[".printf(header.length>0?bounds(header[0]):"null"));
            first=true;if(header.length>0)foreach(var h in find_nodes(header[0],"label")){if(!first)json.append(",");first=false;var font=h.get_pango_context().get_font_description();json.append("[%g,%d]".printf((double)font.get_size()/Pango.SCALE,(int)font.get_weight()));}
            json.append("],\"header_foregrounds\":[");first=true;if(header.length>0)foreach(var label in find_nodes(header[0],"label")){if(!first)json.append(",");first=false;var colour=label.get_style_context().get_color();json.append("[%g,%g,%g,%g]".printf(colour.red,colour.green,colour.blue,colour.alpha));}
            json.append("],\"indicators\":[");first=true;foreach(var indicator in find_nodes(column,"sort-indicator")){if(!first)json.append(",");first=false;json.append("{\"bounds\":%s,\"classes\":%s}".printf(bounds(indicator),quote(string.joinv(" ",indicator.get_css_classes()))));}
            json.append("],\"cells\":[");first=true;cells_report(stack.visible_child,json,ref first);json.append("]}");try{FileUtils.set_contents(path,json.str);}catch(Error e){warning("%s",e.message);}
        }
    }
}
