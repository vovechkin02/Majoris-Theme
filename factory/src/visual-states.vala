namespace MajorisThemeFactory {
    /* Real toolkit state flags, never appearance CSS. Event behavior remains
     * interactive; the labels distinguish held diagnostic flags from input. */
    public class VisualStates : Gtk.Box {
        public VisualStates(Gtk.Window owner,string group="all") {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:16);
            margin_start=24; margin_end=24; margin_top=24; margin_bottom=24;
            var note=new Gtk.Label("Native GTK state flags are held for CSS diagnostics. Use pointer/Tab to verify real input; deactivate the window for real backdrop."); note.wrap=true; append(note);
            string[] kinds={"Normal button","Primary button","Destructive button","Flat button","Icon button","Window control","Entry","Dropdown","Checkbox","Radio","Switch","Tab","View switch","Menu row"};
            for(int k=0;k<kinds.length;k++) {
                if(group=="buttons" && k>2)continue;
                if(group=="controls" && (k<3 || k>5))continue;
                if(group=="inputs" && (k<6 || k>7))continue;
                if(group=="selection" && (k<8 || k>10))continue;
                if(group=="navigation" && k<11)continue;
                var card=new Gtk.Box(Gtk.Orientation.VERTICAL,8); card.add_css_class("card");
                var heading=new Gtk.Label(kinds[k]); heading.xalign=0; heading.margin_top=12; heading.margin_start=12; card.append(heading);
                var grid=new Gtk.Grid(); grid.column_spacing=12; grid.row_spacing=10; grid.margin_start=12; grid.margin_end=12; grid.margin_bottom=12;
                string[] names={"Default","Hover","Pressed","Focus","Disabled","Selected","Backdrop"};
                Gtk.StateFlags[] flags={Gtk.StateFlags.NORMAL,Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE,Gtk.StateFlags.FOCUSED|Gtk.StateFlags.FOCUS_VISIBLE,Gtk.StateFlags.INSENSITIVE,Gtk.StateFlags.CHECKED|Gtk.StateFlags.SELECTED,Gtk.StateFlags.BACKDROP};
                for(int i=0;i<names.length;i++) {
                    var cell=new Gtk.Box(Gtk.Orientation.VERTICAL,6); cell.append(new Gtk.Label(names[i]));
                    Gtk.Widget widget;
                    if(k==5) { var controls=new Gtk.WindowControls(Gtk.PackType.END); controls.decoration_layout=":minimize,maximize,close"; widget=controls; }
                    else if(k==6) { var e=new Gtk.Entry(); e.text="Majoris"; widget=e; }
                    else if(k==7) widget=new Gtk.DropDown.from_strings({"Dropdown","Automatic"});
                    else if(k==8 || k==9) { var c=new Gtk.CheckButton.with_label(k==8?"Check":"Radio"); if(k==9){var mate=new Gtk.CheckButton();c.group=mate;} widget=c; }
                    else if(k==10) widget=new Gtk.Switch();
                    else if(k==11) { var notebook=new Gtk.Notebook(); notebook.append_page(new Gtk.Label("Content"),new Gtk.Label("General")); notebook.append_page(new Gtk.Label("Details"),new Gtk.Label("Details")); widget=notebook; }
                    else if(k==12) { var vs=new Adw.ViewStack(); var lp=vs.add_titled(new Gtk.Label("List"),"list","List"); lp.icon_name="view-list-symbolic"; var gp=vs.add_titled(new Gtk.Label("Grid"),"grid","Grid"); gp.icon_name="view-grid-symbolic"; var sw=new Adw.ViewSwitcher(); sw.policy=Adw.ViewSwitcherPolicy.WIDE; sw.stack=vs; widget=sw; }
                    else { var b=k==4?icon_button("document-save-symbolic","Save"):new Gtk.Button.with_label(k==13?"Move to Trash":"Apply"); if(k==1)b.add_css_class("suggested-action");if(k==2)b.add_css_class("destructive-action");if(k==3)b.add_css_class("flat");if(k==13)b.add_css_class("majoris-menu-danger");widget=b; }
                    widget.halign=Gtk.Align.START; widget.valign=Gtk.Align.CENTER; cell.append(widget); grid.attach(cell,i%4,i/4,1,1);
                    if(i==4)widget.sensitive=false;
                    if(i==5) { if(widget is Gtk.CheckButton)((Gtk.CheckButton)widget).active=true; if(widget is Gtk.Switch)((Gtk.Switch)widget).active=true; }
                    hold_state(widget,flags[i]);
                }
                card.append(grid);append(card);
            }
        }
        void hold_state(Gtk.Widget widget,Gtk.StateFlags state) {
            Timeout.add(350,()=>{ apply_state(widget,state);return Source.REMOVE; });
        }
        void apply_state(Gtk.Widget widget,Gtk.StateFlags state) {
            widget.set_state_flags(state,false);
            if(widget is Gtk.WindowControls || widget is Gtk.Notebook || widget is Adw.ViewSwitcher || widget is Gtk.DropDown) {
                for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling()) apply_state(c,state);
            }
        }
    }
}
