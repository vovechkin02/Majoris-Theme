# GTK4/libadwaita

GTK theme settings alone are insufficient for libadwaita. Development installation symlinks gtk.css, gtk-dark.css **and colors.css** into the normal user override directory; relative imports resolve beside the symlink path. Existing files are journaled and backed up. No application appearance stylesheet masks theme failures.

The gallery uses Trixie's libadwaita 1.7 widgets including AlertDialog, SwitchRow and SpinRow. Deprecated but available ColorButton and FontButton intentionally exercise native legacy controls. CSS parsing and simple/dense border-box geometry are tested.
Native spinner vectors live in gtk-4.0/assets and are linked alongside user CSS. Re-running the installer adds new asset/font links while preserving existing backups. The real-node mappings include dialog.alert/floating-sheet and banner/revealer/widget; stock toolkit image backgrounds, preference subtitle opacity and nested menu-button styling require explicit cascade resets.
