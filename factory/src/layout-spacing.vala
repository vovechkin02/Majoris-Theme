namespace MajorisThemeFactory {
    public class LayoutSpacingPage : Gtk.Box {
        Gtk.Label report;
        public LayoutSpacingPage() {
            Object(orientation:Gtk.Orientation.VERTICAL,spacing:0);
            add_css_class("majoris-dialog-content");
            report=new Gtk.Label("Native spacing: inspect allocations after mapping");report.wrap=true;append(report);
            var inspect=new Gtk.Button.with_label("Measure visible sibling gaps");append(inspect);
            inspect.clicked.connect(()=>{var text=new StringBuilder();inspect_box(this,text);report.label=text.str;});
            var page=new Adw.PreferencesPage();append(page);
            var tags=new Adw.PreferencesGroup();tags.title="Tags assignment — inherited non-row spacing";page.add(tags);
            tags.add(new Gtk.SearchEntry());var list=new Gtk.ListBox();list.add_css_class("boxed-list");
            var row=new Adw.ActionRow();row.title="Documents";list.append(row);row=new Adw.ActionRow();row.title="Work";list.append(row);tags.add(list);
            var editor=layout("majoris-field");editor.append(new Gtk.Entry());editor.append(new Gtk.Label("Tag name validation"));editor.visible=false;tags.add(editor);
            var actions=layout("majoris-action-group",Gtk.Orientation.HORIZONTAL);var toggle=new Gtk.Button.with_label("New Tag");toggle.clicked.connect(()=>editor.visible=!editor.visible);actions.append(toggle);actions.append(new Gtk.Button.with_label("Manage Tags"));tags.add(actions);
            string[] styles={"majoris-control-stack","majoris-action-group","majoris-section-stack","majoris-major-stack","majoris-connected-group"};
            foreach(var style in styles) {var group=new Adw.PreferencesGroup();group.title=style;page.add(group);var b=layout(style,style=="majoris-control-stack"?Gtk.Orientation.VERTICAL:Gtk.Orientation.HORIZONTAL);b.append(new Gtk.Button.with_label("First"));b.append(new Gtk.Button.with_label("Second"));group.add(b);}
            var form=new Adw.PreferencesGroup();form.title="Form, search and results";page.add(form);var fields=layout("majoris-form-layout");
            var pair=layout("majoris-field");pair.append(new Gtk.Label("Associated label"));pair.append(new Gtk.Entry());fields.append(pair);fields.append(new Gtk.PasswordEntry());fields.append(new Gtk.DropDown.from_strings({"First","Second"}));fields.append(new Gtk.SpinButton.with_range(0,100,1));fields.append(new Gtk.CheckButton.with_label("Enable option"));fields.append(new Gtk.Switch());fields.append(new Gtk.Scale.with_range(Gtk.Orientation.HORIZONTAL,0,100,1));fields.append(new Gtk.TextView());form.add(fields);
            var progress=new Adw.PreferencesGroup();progress.title="Progress and separate footer";page.add(progress);
            var footer=layout("majoris-footer-layout");var content=layout("majoris-progress-content");content.append(new Gtk.Label("Copying files"));var detail=layout("majoris-progress-detail");var bar=new Gtk.ProgressBar();bar.fraction=0.6;detail.append(bar);detail.append(new Gtk.Label("6 of 10 files"));content.append(detail);footer.append(content);var buttons=layout("majoris-action-footer",Gtk.Orientation.HORIZONTAL);buttons.append(new Gtk.Button.with_label("Cancel"));buttons.append(new Gtk.Button.with_label("Pause"));footer.append(buttons);progress.add(footer);
            var popup=new Gtk.MenuButton();popup.label="Ordinary popover";var pop=new Gtk.Popover();var popcontent=layout("majoris-control-stack");popcontent.append(new Gtk.SearchEntry());popcontent.append(new Gtk.Button.with_label("Results"));pop.child=popcontent;popup.popover=pop;progress.add(popup);
            var expander=new Gtk.Expander("Expander content");var ec=layout("majoris-control-stack");ec.append(new Gtk.Entry());ec.append(new Gtk.Button.with_label("Apply"));expander.child=ec;progress.add(expander);
            var flow=new Gtk.FlowBox();flow.selection_mode=Gtk.SelectionMode.NONE;flow.tooltip_text="Neutral native FlowBox: item gaps use row-spacing and column-spacing properties";flow.append(new Gtk.Button.with_label("Neutral"));flow.append(new Gtk.Button.with_label("FlowBox"));progress.add(flow);
            var toolbar=new Gtk.Box(Gtk.Orientation.HORIZONTAL,4);toolbar.add_css_class("toolbar");toolbar.append(new Gtk.Button.with_label("Toolbar"));toolbar.append(new Gtk.Button.with_label("Regression"));progress.add(toolbar);
        }
        static Gtk.Box layout(string cls,Gtk.Orientation orientation=Gtk.Orientation.VERTICAL) {var b=new Gtk.Box(orientation,0);b.add_css_class(cls);return b;}
        static void inspect_box(Gtk.Widget widget,StringBuilder text) {
            var b=widget as Gtk.Box;
            if(b!=null) {Gtk.Widget? previous=null;for(var c=b.get_first_child();c!=null;c=c.get_next_sibling()) {if(!c.visible)continue;if(previous!=null) {Graphene.Rect a=Graphene.Rect(),z=Graphene.Rect();if(previous.compute_bounds(b,out a)&&c.compute_bounds(b,out z))text.append_printf("%s: %.0fpx\n",b.get_css_name(),b.orientation==Gtk.Orientation.VERTICAL?z.get_y()-a.get_y()-a.get_height():Math.fabs(z.get_x()-a.get_x())-(z.get_x()>a.get_x()?a.get_width():z.get_width()));}previous=c;}}
            for(var c=widget.get_first_child();c!=null;c=c.get_next_sibling())inspect_box(c,text);
        }
    }
}


