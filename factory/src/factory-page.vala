namespace MajorisThemeFactory {
    public class ControlFlow : Gtk.Box {
        Gtk.FlowBox flow;
        public ControlFlow () {
            Object (orientation: Gtk.Orientation.VERTICAL);
            flow=new Gtk.FlowBox(); flow.selection_mode=Gtk.SelectionMode.NONE; flow.column_spacing=8; flow.row_spacing=8; flow.max_children_per_line=6;
            base.append(flow);
        }
        public new void append (Gtk.Widget widget) {
            widget.halign=Gtk.Align.START; widget.valign=Gtk.Align.CENTER;
            flow.append(widget);
        }
    }
    public class FactoryPage : Gtk.Box {
        public Adw.ToastOverlay? toast_overlay;
        Gtk.Window owner;
        Gtk.Grid gallery;
        int section_count = 0;
        Gtk.Box section (string title) {
            var card = new Gtk.Box (Gtk.Orientation.VERTICAL, 12); card.add_css_class ("card");
            var inner = new Gtk.Box (Gtk.Orientation.VERTICAL,12); inner.margin_top=16; inner.margin_bottom=16; inner.margin_start=16; inner.margin_end=16;
            var label = new Gtk.Label(title); label.xalign=0; label.add_css_class("heading"); inner.append(label); card.append(inner);
            card.hexpand=true; card.valign=Gtk.Align.START;
            if(section_count<4) gallery.attach(card,section_count%2,section_count/2,1,1);
            else gallery.attach(card,0,section_count-2,2,1);
            section_count++; return inner;
        }
        ControlFlow row () { return new ControlFlow(); }
        public FactoryPage (Gtk.Window window) {
            Object (orientation: Gtk.Orientation.VERTICAL, spacing: 16);
            owner=window; margin_start=24; margin_end=24; margin_top=24; margin_bottom=24;
            var title=new Gtk.Label("Majoris native widget gallery"); title.xalign=0; title.add_css_class("title-1"); append(title);
            append(new Gtk.Label("Hover and hold buttons to test real states; Tab moves keyboard focus. No simulated CSS states."));
            gallery=new Gtk.Grid(); gallery.column_spacing=16; gallery.row_spacing=16; gallery.column_homogeneous=true; append(gallery);
            var buttons=section("Buttons and interaction states"); var r=row(); buttons.append(r);
            string[] labels={"Default","Suggested","Destructive","Flat","Disabled"};
            string[] classes={"","suggested-action","destructive-action","flat",""};
            for(int i=0;i<labels.length;i++){var b=new Gtk.Button.with_label(labels[i]); if(classes[i]!="")b.add_css_class(classes[i]); b.sensitive=i!=4; r.append(b);}
            r.append(icon_button("document-save-symbolic","Save — real GTK tooltip"));
            var split=new Adw.SplitButton(); split.label="Split button"; var sm=new Menu(); sm.append("New window","win.new"); split.menu_model=sm; r=row(); r.append(split); buttons.append(r);
            var selection=section("Selection"); r=row(); selection.append(r);
            var check=new Gtk.CheckButton.with_label("Checkbox"); r.append(check);
            var checked=new Gtk.CheckButton.with_label("Checked"); checked.active=true; r.append(checked);
            var mixed=new Gtk.CheckButton.with_label("Indeterminate"); mixed.inconsistent=true; r.append(mixed);
            var radio=new Gtk.CheckButton.with_label("Radio A"); var radio2=new Gtk.CheckButton.with_label("Radio B"); radio2.group=radio; radio.active=true; r.append(radio); r.append(radio2);
            var sw=new Gtk.Switch(); sw.valign=Gtk.Align.CENTER; sw.active=true; r.append(sw);
            var inputs=section("Inputs"); r=row(); inputs.append(r);
            var entry=new Gtk.Entry(); entry.placeholder_text="Text entry"; r.append(entry);
            var search=new Gtk.SearchEntry(); r.append(search);
            var password=new Gtk.PasswordEntry(); password.show_peek_icon=true; r.append(password);
            r=row(); inputs.append(r); r.append(new Gtk.DropDown.from_strings({"Majoris","GTK","libadwaita"})); r.append(new Gtk.SpinButton.with_range(0,100,1)); r.append(new Gtk.ColorButton()); r.append(new Gtk.FontButton());
            var ranges=section("Range and progress"); var scale=new Gtk.Scale.with_range(Gtk.Orientation.HORIZONTAL,0,100,1); scale.set_value(62); ranges.append(scale);
            var progress=new Gtk.ProgressBar(); progress.fraction=0.68; ranges.append(progress);
            var level=new Gtk.LevelBar(); level.value=0.7; ranges.append(level); var spinner=new Gtk.Spinner(); spinner.start(); ranges.append(spinner);
            var rows=section("Adwaita rows"); var list=new Gtk.ListBox(); list.add_css_class("boxed-list"); list.selection_mode=Gtk.SelectionMode.NONE; rows.append(list);
            var action=new Adw.ActionRow(); action.title="Action row"; action.subtitle="Native subtitle and suffix"; action.add_suffix(icon_button("go-next-symbolic","Open")); list.append(action);
            var switchrow=new Adw.SwitchRow(); switchrow.title="Switch row"; switchrow.active=true; list.append(switchrow);
            var combo=new Adw.ComboRow(); combo.title="Combo row"; combo.model=new Gtk.StringList({"Standard","Compact"}); list.append(combo);
            var er=new Adw.EntryRow(); er.title="Entry row"; list.append(er);
            var pr=new Adw.PasswordEntryRow(); pr.title="Password row"; list.append(pr);
            var sr=new Adw.SpinRow.with_range(0,100,1); sr.title="Spin row"; list.append(sr);
            var exp=new Adw.ExpanderRow(); exp.title="Expander row"; var nested=new Adw.ActionRow(); nested.title="Expanded detail"; exp.add_row(nested); list.append(exp);
            var nav=section("Navigation and data"); var ns=new Adw.ViewStack(); ns.add_titled(new Gtk.Label("Overview content"),"overview","Overview"); ns.add_titled(new Gtk.Label("Details content"),"details","Details"); var switcher=new Adw.ViewSwitcher(); switcher.stack=ns; nav.append(switcher); nav.append(ns);
            var notebook=new Gtk.Notebook(); notebook.append_page(new Gtk.Label("Native GTK tab"),new Gtk.Label("Tab one")); notebook.append_page(new Gtk.Label("Second tab"),new Gtk.Label("Tab two")); nav.append(notebook);
            var data=new Gtk.ListBox(); data.add_css_class("boxed-list"); for(int i=0;i<8;i++){var label=new Gtk.Label("Document %02d                 Modified today                 24 KB".printf(i+1)); label.xalign=0; data.append(label);} nav.append(data); data.select_row(data.get_row_at_index(1));
            var feedback=section("Menus, popovers and feedback"); r=row(); feedback.append(r); r.append(menu_button());
            var pop=new Gtk.MenuButton(); pop.label="Plain popover"; var p=new Gtk.Popover(); var pc=new Gtk.Box(Gtk.Orientation.VERTICAL,8); pc.append(new Gtk.Label("Native popover contents")); var destructive=new Gtk.Button.with_label("Destructive item"); destructive.add_css_class("destructive-action"); pc.append(destructive); p.child=pc; pop.popover=p; r.append(pop);
            var toast=new Gtk.Button.with_label("Show toast"); toast.clicked.connect(()=>toast_overlay.add_toast(new Adw.Toast("Majoris notification"))); r.append(toast);
            var dialog=new Gtk.Button.with_label("Open alert dialog"); dialog.clicked.connect(()=>{var d=new Adw.AlertDialog("Save changes?","Native Majoris dialog surface and response buttons."); d.add_response("cancel","Cancel"); d.add_response("save","Save"); d.set_response_appearance("save",Adw.ResponseAppearance.SUGGESTED); d.present(owner);}); r.append(dialog);
            var banner=new Adw.Banner("Majoris update available"); banner.button_label="Details"; banner.revealed=true; feedback.append(banner);
            for(int i=0;i<12;i++) append(new Gtk.Label("Overlay scrollbar test row %d".printf(i+1)));
        }
    }
}
