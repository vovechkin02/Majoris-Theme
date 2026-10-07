# GTK3

Select `GTK_THEME=Majoris` after development installation. GTK3 loads the user-local theme and uses decoration, titlebutton, menu and menuitem nodes. It has a separate stylesheet and native GTK3 CssProvider test. The icon overlay is selected by the desktop icon-theme setting; the factory sets it within its process.

GTK3 imports the installed toolkit's Adwaita resource as its native baseline, then applies Majoris colors and selectors. This supplies native check/radio rendering and uncommon widgets without copying third-party CSS into the repository. GTK4/libadwaita already supplies its own native baseline.
