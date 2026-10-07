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

CSS minima are content sizes. A 30px minimum plus two 1px borders produces a 32px button. AdwHeaderBar also has native windowhandle padding; normalize it to avoid double padding. The HTML uses border-box sizing: 32px children plus 15px vertical padding and a 1px divider allocate 48px. GTK padding is 7px above and 8px below to reserve that divider within the 48px target. Dense dropdown rows have zero header-local padding to prevent stretching. Inner pane boundaries stay square; only the outer window rounds.

The factory uses native widgets and layout margins without an application CSS provider. All tested appearance comes from the theme/user override. The Visual States page holds real GTK state flags for diagnostics, labels them clearly, and still supports pointer/keyboard interaction. Reusable classes majoris-segmented, majoris-data-view, majoris-sidebar, majoris-card-header and majoris-menu-danger express component semantics rather than application identity. GTK3 translates unsupported 650 weight to 600 and paints a label-owned 2px tab underline because its gradients do not support calc().
