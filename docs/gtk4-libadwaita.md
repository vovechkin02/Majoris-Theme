# GTK4/libadwaita

GTK theme settings alone are insufficient for libadwaita. Development installation symlinks gtk.css, gtk-dark.css **and colors.css** into the normal user override directory; relative imports resolve beside the symlink path. Existing files are journaled and backed up. No application appearance stylesheet masks theme failures.

The gallery uses Trixie's libadwaita 1.7 widgets including AlertDialog, SwitchRow and SpinRow. Deprecated but available ColorButton and FontButton intentionally exercise native legacy controls. CSS parsing and simple/dense border-box geometry are tested.
