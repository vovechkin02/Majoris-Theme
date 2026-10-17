from css_contract import ROOT
code='\n'.join(p.read_text() for p in (ROOT/'factory/src').glob('*.vala'))
for native in ['Adw.TabView','Adw.TabBar','GtkSource.View','GtkSource.Buffer','GtkSource.SearchContext','Gtk.Spinner','Gtk.LevelBar','Gtk.CheckButton','Gtk.Switch','Gtk.DropDown','Gtk.PasswordEntry','Adw.ActionRow','Adw.SwitchRow','Adw.ComboRow','Adw.EntryRow','Adw.PasswordEntryRow','Adw.SpinRow','Adw.ExpanderRow','Gtk.ColumnView','Gtk.SingleSelection','Gtk.Notebook','Gtk.StackSwitcher','Adw.ViewSwitcher','Adw.StatusPage','Adw.ToastOverlay','Adw.Toast','Adw.AlertDialog','Adw.Banner','Gtk.Popover','Gtk.PopoverMenu','Adw.ToolbarView','Adw.HeaderBar','Gtk.WindowControls']:
    assert native in code,'Native demonstration dropped: '+native
assert 'Gtk.LevelBarMode.DISCRETE' in code and 'level.value=6' in code
for feature in ['Visual States','SplitFixture','HeaderFixture','navigation-sidebar','majoris-menu-danger','majoris-segmented','show_dialog','show_toast']:assert feature in code,feature
assert 'Gtk.CssProvider' not in code,'Factory must not supply its own appearance CSS'
print('Native factory categories, discrete level, state laboratory and stress fixtures present')
