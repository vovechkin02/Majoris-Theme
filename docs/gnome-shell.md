# GNOME Shell

The original theme covers panel buttons, menus, quick settings/sliders, calendar, notifications, dialogs, search, overview, workspaces, dash labels and tooltips. No reference artwork is reused.

`tools/validate-shell.py` parses declaration grammar and checks key selectors against installed Debian `gnome-shell-theme.gresource` light CSS (gnome-shell-common 48.7). This is static validation, not proof of St property support or runtime visual correctness.

Tier 2 requires a real Majoris GNOME Shell/Mutter session or VM, with User Themes or distribution integration. Check calendar/notification states, keyboard focus, quick toggles/sliders, overview/display scaling, window corners/shadows and popup clipping. Ordinary WSLg is not that environment. No Shell extension or GDM theme is implemented here.

Light and dark are provided simultaneously. The generated dark stylesheet is also installed as the Shell-only `Majoris-Dark` User Themes entrypoint. `scripts/select-shell-theme.sh --light|--dark|--auto` implements explicit selection or a reversible foreground monitor through the User Themes schema. Auto observes GNOME `color-scheme`; the ISO/session must supervise the monitor or supply equivalent integration. These runtime selections require an enabled User Themes extension and have not been validated under WSL. Test Light → Dark → Light in the real VM, including panel/clock, menus, Quick Settings, calendar, notifications, dialogs, search/overview, workspaces, dash labels/tooltips and scaling. See [dark theme architecture](dark-theme.md).
