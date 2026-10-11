# Theme-state GNOME VM regression checklist

Use the target Majoris GNOME/Mutter session with its normal DING extension,
installed light/dark assets, supplied Plus Jakarta Sans, desktop extension and
OS-owned automatic process attachment. Record GNOME/GTK/DING versions, renderer,
scale, screenshots and PASS/FAIL for each scenario. WSL source/GTK paint tests
cannot certify this session lifecycle.

| Scheme | Focus | Required desktop result |
|---|---|---|
| Light | Desktop focused | Wallpaper visible; GTK desktop window transparent; Home/Trash visible |
| Light | Another application focused | Same; no opaque backdrop rectangle |
| Dark | Desktop focused | Wallpaper visible; GTK desktop window transparent; Home/Trash visible |
| Dark | Another application focused | Same; no opaque backdrop rectangle |

In each scheme open and reopen panel menus, Quick Settings, calendar,
notifications, modal dialogs and search. Check readable panel/clock/tray icons;
Quick Settings labels, icons, slider, power controls and arrow buttons; disabled
controls; checked toggles with white text/icons on #6366F1. In dark mode confirm
panel #202023, transients rgba(40,40,44,.98), search/controls #28282C and text
#F4F4F5. In light mode confirm white panel/popups with #1C1C1F foregrounds,
#F2F2F4 controls and #8A8A92 disabled foregrounds. Dark disabled foreground is
#7F7F88. Also check hover/pressed states and contrast under fractional scaling.

Run both sequences without logout, leaving some surfaces open and reopening
others after each transition:

1. Light → Dark → Light.
2. Dark → Light → Dark.

Reject stale white text on light surfaces, dark text on dark surfaces, old white
or dark popup surfaces, old disabled colours, lost wallpaper or hidden Home/Trash.
Repeat desktop focus changes after every transition. Check GTK3 applications and
GTK4/libadwaita applications launched before/after switching, including GJS/GI
processes that load a toolkit later; the OS owns their automatic attachment.

Retain the established checks for 48px simple/dense/split headers, 32x32 titlebar
plates, 16x16 minimize/maximize/restore/close glyphs, Mutter shadows/corners,
inactive/maximized/restored/fullscreen/tiled windows, Wayland, 100%/200% and
125%/150% scaling, portals, Settings, and GDM. Theme assets/bridges are provided
here; session dispatcher, desktop extension/activation, wallpaper selection and
full GNOME lifecycle belong to the distro/desktop project.
