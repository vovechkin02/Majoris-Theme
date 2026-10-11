# GNOME Shell

The original theme covers panel buttons, menus, quick settings/sliders, calendar, notifications, dialogs, search, overview, workspaces, dash labels and tooltips. No reference artwork is reused.

`tools/validate-shell.py` parses declaration grammar and checks key selectors against installed Debian `gnome-shell-theme.gresource` light CSS (gnome-shell-common 48.7). This is static validation, not proof of St property support or runtime visual correctness.

Tier 2 requires a real Majoris GNOME Shell/Mutter session or VM, with User Themes or distribution integration. Check calendar/notification states, keyboard focus, quick toggles/sliders, overview/display scaling, window corners/shadows and popup clipping. Ordinary WSLg is not that environment. No Shell extension or GDM theme is implemented here.

Light and dark are provided simultaneously. The generated dark stylesheet is also installed as the Shell-only `Majoris-Dark` User Themes entrypoint. `scripts/select-shell-theme.sh --light|--dark|--auto` implements explicit selection or a reversible foreground monitor through the User Themes schema. Auto observes GNOME `color-scheme`; the ISO/session must supervise the monitor or supply equivalent integration. These runtime selections require an enabled User Themes extension and have not been validated under WSL. Test Light → Dark → Light in the real VM, including panel/clock, menus, Quick Settings, calendar, notifications, dialogs, search/overview, workspaces, dash labels/tooltips and scaling. See [dark theme architecture](dark-theme.md).


## Complete variant colour ownership

Generation uses explicit Shell semantic surfaces. Light panel/popups stay
#FFFFFF with #1C1C1F labels/icons. Dark panel is #202023, elevated popup/Quick
Settings surfaces rgba(40,40,44,.98), and search/secondary controls #28282C with
#F4F4F5 text. Panel clock/status descendants and popup, toggle, slider, system,
power, calendar, message and dialog descendants explicitly reset StLabel/StIcon
foregrounds in each stylesheet. Selected menu/toggle descendants are #FFFFFF
on #6366F1; disabled descendants use #8A8A92 light / #7F7F88 dark. Icon buttons
retain 4px corners and the existing neutral default/hover/active surfaces.

`tools/validate-shell.py` checks exact selector properties as well as grammar and
installed selectors. Tests simulate both Light → Dark → Light and Dark → Light →
Dark source replacements and reject stale colour ownership. This is source
coverage, not a live St rendering or extension-switching claim.

Majoris-Theme supplies these assets, DING transparency and reusable GTK bridges.
The distro/desktop project owns automatic global bridge attachment, the session
LD_PRELOAD dispatcher, Shell extension activation and installed-session variant
switching, panel layout/branding, wallpaper and Mutter lifecycle. The ISO builder
can copy `theme/Majoris/` verbatim; it should activate these assets through its
session machinery rather than patch CSS. The desktop extension and dispatcher
remain outside this repository. Follow [the exact VM scenarios](theme-state-vm-checklist.md).
