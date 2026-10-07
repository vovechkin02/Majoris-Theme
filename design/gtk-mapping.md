# Native mapping

| HTML concept | GTK3 | GTK4/libadwaita |
|---|---|---|
| Window radius/shadow | decoration | window.background / csd / solid-csd |
| Headerbar | headerbar | AdwHeaderBar → windowhandle → center box |
| Window controls | button.titlebutton | windowcontrols → button → image |
| Popover surface | popover.background | popover → contents |
| Menu row | menuitem | modelbutton / button.model |
| Cards/preferences | list/row, .card | .card / .boxed-list / Adw rows |
| Sidebar | .sidebar | .navigation-sidebar |
| Quiet scrollbar | scrollbar → slider | scrollbar → range → trough/slider |

CSS minima are content sizes. A 30px minimum plus two 1px borders produces a 32px button. AdwHeaderBar also has native windowhandle padding; normalize it to avoid double padding. Its 32px children plus 16px outer padding and a 1px separator allocate 49px. Dense dropdown rows have zero header-local padding to prevent stretching. Inner pane boundaries stay square; only the outer window rounds.

The factory uses native widgets and layout margins without an application CSS provider. All tested appearance comes from the theme/user override. Hover and press are interactive states; no diagnostic CSS fakes them.
