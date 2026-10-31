namespace MajorisThemeFactory {
    public class SwitchPage : Gtk.Box {
        public SwitchPage () {
            Object(orientation: Gtk.Orientation.VERTICAL, spacing: 16, margin_top: 24, margin_bottom: 24, margin_start: 24, margin_end: 24);
            append(new Gtk.Label("Switches — native 4px track and thumb"));
            var comparison=new Gtk.Box(Gtk.Orientation.HORIZONTAL,12);
            comparison.append(new Gtk.Button.with_label("Button"));
            comparison.append(new Gtk.CheckButton.with_label("Checkbox"));
            foreach(bool active in new bool[]{false,true}) {var sw=new Gtk.Switch();sw.active=active;sw.valign=Gtk.Align.CENTER;comparison.append(sw);}
            var segments=new Gtk.Box(Gtk.Orientation.HORIZONTAL,0);segments.add_css_class("majoris-segmented");
            var first=new Gtk.ToggleButton.with_label("List");var second=new Gtk.ToggleButton.with_label("Grid");second.group=first;first.active=true;segments.append(first);segments.append(second);comparison.append(segments);append(comparison);
            var group=new Adw.PreferencesGroup();
            var row=new Adw.SwitchRow();row.title="Native SwitchRow";row.active=true;group.add(row);
            var disabled=new Adw.SwitchRow();disabled.title="Disabled checked row";disabled.active=true;disabled.sensitive=false;group.add(disabled);
            var suffix=new Adw.ActionRow();suffix.title="ActionRow switch suffix";var sw=new Gtk.Switch();sw.valign=Gtk.Align.CENTER;suffix.add_suffix(sw);suffix.activatable_widget=sw;group.add(suffix);append(group);
            var rtl=new Gtk.Switch();rtl.set_direction(Gtk.TextDirection.RTL);rtl.halign=Gtk.Align.START;append(new Gtk.Label("RTL native switch"));append(rtl);
            var open=new Gtk.Button.with_label("Open switch preferences dialog");
            open.clicked.connect(()=>{var dialog=new Adw.PreferencesDialog();dialog.title="Switch preferences";var page=new Adw.PreferencesPage();var preferences=new Adw.PreferencesGroup();foreach(bool active in new bool[]{false,true}){var item=new Adw.SwitchRow();item.title=active?"Checked":"Unchecked";item.active=active;preferences.add(item);}page.add(preferences);dialog.add(page);dialog.present(this);});append(open);
            append(new Gtk.Label("Tab to a switch; Space toggles it. Appearance follows the factory menu."));
        }
    }
}

