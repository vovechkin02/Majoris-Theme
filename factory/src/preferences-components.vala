namespace MajorisThemeFactory {
    public class PreferencesComponents : Adw.PreferencesPage {
        Adw.ActionRow information(string title,string value,bool property=false) {
            var row=new Adw.ActionRow();row.title=title;row.subtitle=value;row.subtitle_selectable=true;row.subtitle_lines=0;
            if(property)row.add_css_class("property");return row;
        }
        void rtl_direction(Gtk.Widget widget) {
            widget.set_direction(Gtk.TextDirection.RTL);
            for(var child=widget.get_first_child();child!=null;child=child.get_next_sibling())rtl_direction(child);
        }
        public PreferencesComponents() {
            var info=new Adw.PreferencesGroup();info.title="Information";info.description="Read-only file information. Select values or use Copy without activating the row.";
            string[] names={"Type","Size","Location","Modified"};string[] values={"Plain text document","19 bytes","Home / Documents","31 Oct 2026"};
            for(int i=0;i<names.length;i++) {
                var row=information(names[i],values[i],true);
                if(i==2){var copy=new Gtk.Button.from_icon_name("edit-copy-symbolic");copy.tooltip_text="Copy location";copy.valign=Gtk.Align.CENTER;string value=values[i];copy.clicked.connect(()=>copy.get_clipboard().set_text(value));row.add_suffix(copy);}
                info.add(row);
            }
            add(info);
            var open_with=new Adw.PreferencesGroup();open_with.title="Open With";
            var application=information("Notepad","Default application");application.icon_name="text-editor-symbolic";
            var change=new Gtk.Button.with_label("Change…");change.valign=Gtk.Align.CENTER;change.clicked.connect(()=>{application.subtitle=application.subtitle=="Default application"?"Application chooser activated":"Default application";});application.add_suffix(change);application.activatable_widget=change;open_with.add(application);add(open_with);
            var organisation=new Adw.PreferencesGroup();organisation.title="Organisation";var favorite=new Adw.SwitchRow();favorite.title="Favorite";organisation.add(favorite);add(organisation);
            var general=new Adw.PreferencesGroup();general.title="General settings";general.description="Native rows keep their own editing and activation behaviour.";
            var add_button=new Gtk.Button.from_icon_name("list-add-symbolic");add_button.tooltip_text="Add information";add_button.valign=Gtk.Align.CENTER;add_button.clicked.connect(()=>general.add(information("Added information","This row is passive")));general.header_suffix=add_button;
            general.add(information("Standard ActionRow","Supporting description"));
            var switchrow=new Adw.SwitchRow();switchrow.title="Automatic updates";switchrow.subtitle="Native switch activation";general.add(switchrow);
            var combo=new Adw.ComboRow();combo.title="View";combo.model=new Gtk.StringList({"Standard","Compact"});general.add(combo);
            var spin=new Adw.SpinRow.with_range(0,100,1);spin.title="Refresh interval";general.add(spin);
            var entry=new Adw.EntryRow();entry.title="Display name";general.add(entry);
            var password=new Adw.PasswordEntryRow();password.title="Password";general.add(password);
            var expander=new Adw.ExpanderRow();expander.title="Advanced";expander.subtitle="Native expansion";expander.add_row(information("Nested information","No duplicated container border"));general.add(expander);
            var buttonrow=new Adw.ButtonRow();buttonrow.title="Reset preferences";buttonrow.activated.connect(()=>{switchrow.active=false;combo.selected=0;spin.value=0;entry.text="";});general.add(buttonrow);
            var suggested=new Adw.ButtonRow();suggested.title="Apply preferences";suggested.add_css_class("suggested-action");general.add(suggested);
            var destructive=new Adw.ButtonRow();destructive.title="Remove configuration";destructive.add_css_class("destructive-action");general.add(destructive);add(general);
            var semantics=new Adw.PreferencesGroup();semantics.title="Informational and interactive";
            semantics.add(information("Passive information","Hover does not imply an action"));
            var actionable=information("Interactive action","Tab and Enter activate the suffix");var action=new Gtk.Button.with_label("Activate");action.valign=Gtk.Align.CENTER;action.clicked.connect(()=>actionable.subtitle="Native action activated");actionable.add_suffix(action);actionable.activatable_widget=action;semantics.add(actionable);
            var disabled=information("Disabled information","Native disabled state");disabled.sensitive=false;semantics.add(disabled);add(semantics);
            var suffixes=new Adw.PreferencesGroup();suffixes.title="Prefix and suffix controls";
            Gtk.Widget[] controls={new Gtk.Switch(),new Gtk.Button.with_label("Action"),new Gtk.Button.from_icon_name("edit-copy-symbolic"),new Gtk.DropDown.from_strings({"Default","Alternative"}),new Gtk.SpinButton.with_range(0,100,1),new Gtk.Label("Value"),new Gtk.Image.from_icon_name("go-next-symbolic"),new Gtk.ProgressBar()};
            foreach(var control in controls){var row=new Adw.ActionRow();row.title="Native suffix";row.icon_name="document-properties-symbolic";control.valign=Gtk.Align.CENTER;row.add_suffix(control);suffixes.add(row);}add(suffixes);
            var long_content=new Adw.PreferencesGroup();long_content.title="Long content and selectable subtitles";long_content.description="Resize the window or increase system text size; rows grow naturally.";
            foreach(var text in new string[]{"1.0 KiB (1028 bytes)","1 files, 0 folders","Home / Documents / Folder1","/etc/bluetooth/input.conf","Tue 03 Jun 2025 06:48:11 PM UTC","ABCDEFGHIJKLMNOPQRSTUVWXYZ","gjpqy","A multiline subtitle\nwith a second line\nand a third line"})long_content.add(information("Text rendering sample",text));add(long_content);
            var rtl=new Adw.PreferencesGroup();rtl.title="RTL layout";rtl.set_direction(Gtk.TextDirection.RTL);var rtlrow=information("RTL information","Home / Documents / Folder1");rtlrow.icon_name="document-properties-symbolic";rtl.add(rtlrow);rtl_direction(rtl);add(rtl);
        }
    }
}
