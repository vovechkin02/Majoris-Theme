# Majoris dark theme

The supplied dark factory is a true counterpart to the light design. Both reference HTML files are preserved verbatim. The dark file contains the original root block and a later `/* MAJORIS DARK THEME */` block. `tools/design.py` merges both root blocks and all component declarations in source order. `design/tokens-dark.json` includes the effective CSS rules, root palette, semantic component colours, shadows, typography and shared geometry. Generation and verification use that extraction; they do not mistake the initial light block for the dark palette.

## Palette and surfaces

Dark surfaces are cool neutral near-blacks, rather than a blue-black palette.

| Semantic role | Colour |
|---|---|
| Window background | `#18181B` |
| Card / view surface | `#202023` |
| Elevated controls | `#28282C` |
| Hover / active | `#303035` / `#38383D` |
| Border / soft divider | `#3B3B40` / `#313136` |
| Main / secondary / tertiary text | `#F4F4F5` / `#A9A9B0` / `#7F7F88` |
| Primary default / hover / pressed | `#6366F1` / `#7377F3` / `#4F46E5` |
| Focus | `#818CF8` |
| Danger default / hover / pressed | `#DC3C4D` / `#E34B5B` / `#B92F3E` |
| Success | `#22A06B` |

Headerbars use `rgba(32,32,35,.94)` and the soft divider. Sidebar surface is `#1D1D20`. Sidebar selection uses translucent indigo and `#C7D2FE` text with an `#818CF8` indicator; table selection uses the same translucent fill with `#E0E7FF` text. These are distinct semantic treatments. Inputs use the elevated surface, an `#A5B4FC` caret, and `rgba(99,102,241,.42)` selection.

Generic focus uses a 2px `rgba(129,140,248,.34)` halo; primary focus uses `.38` and window controls `.36`. Flat buttons remain flat outside focus. Destructive hover and pressed states have explicit colours. Toggle/view-switch surfaces use `#242428`, selected children `#35353A`; check/radio use `#26262A` with `#4A4A50` borders and white selected glyphs. Switches use a `#303035` off track, `#DADAE0` off thumb, indigo on track and white on thumb.

Elevation follows the reference's deeper black shadows and subtle white inset highlights. Control normal/hover/active, card, popover and window shadows are separate tokens. Boxed preference lists have no card shadow. Expander details use `#26262A`; the native nested list receives an inset 1px separator to preserve the shared allocation. Banner uses `#24253D` / `#3C3F78` / `#C7D2FE`. Toast uses `#0F0F12`, white text, a subtle white border and an `#A5B4FC` action. Dialog uses the surface with an elevated footer and stronger elevation.

The tooltip deliberately inverts the dark UI: `#F4F4F5` background with `#18181B` text. This applies to the actual GTK tooltip and its label. Native GTK tooltips do not expose the HTML's left-pointing arrow; popup placement remains toolkit owned. Scrollbar tracks stay quiet and transparent; thumbs use `#686872`, 6px width and 4px radius. The dark spinner is a separate 20px vector, with a 2px `#34365D` ring and `#818CF8` arc. Tests capture actual realized GtkSpinner windows in both toolkits and check both rendered stroke colours.

## Geometry and generation

Shared templates retain 4px control / 8px structural radii, a 48px header including its divider, 32px window controls and unchanged exact 16px SVG glyphs. Motion stays stationary at 128ms for controls and 256ms for surfaces. The dark generator renders the shared templates with the effective dark values and appends dark semantic overrides. Generated output contains repeated geometry for standalone native entrypoints, but there is one authored source for those allocations. The existing light CSS is not restructured.

`gtk-dark.css` imports the light and dark colour definitions, not `gtk.css`: this lets a user-local `gtk.css` symlink select the standalone dark file without recursive imports. GTK3 also imports its native Adwaita base. Both variants are packaged simultaneously, including both spinner assets. Geometry equality compares the entire realized factory widget tree and reports, including hidden banners, simple/dense/split headers, fonts and control sizes.

## Native switching on Debian Trixie

GTK3 loads named theme `Majoris`; `GTK_THEME=Majoris:dark` explicitly selects its dark entrypoint. Its native `gtk-application-prefer-dark-theme` setting also selects that entrypoint. The generic GTK3 auto bridge observes GNOME `color-scheme` and updates that native setting. It selects the Majoris named theme only in the launched process. The auto wrapper clears `GTK_THEME`, because a fixed environment variant overrides automatic selection.

GTK4 4.18/libadwaita 1.7 does not select the user `gtk-dark.css` merely because StyleManager changes to dark. The reusable GTK4 bridge loads the appropriate installed theme entrypoint at user priority + 1 and watches native `Adw.StyleManager::dark`. It contains no palette, geometry or widget drawing. The factory links it; arbitrary GTK4/libadwaita processes can use `scripts/with-majoris-gtk4.sh PROGRAM`. A packaged install supplies `majoris-gtk4`; GTK3 has `majoris-gtk3 --light|--dark|--auto PROGRAM`. Do not preload the GTK4 bridge into a GTK3 process.

The factory accepts `--light`, `--dark`, `--system`; its existing menu contains Appearance → Light / Dark / System. Each selects FORCE_LIGHT, FORCE_DARK or DEFAULT. The same realized widgets switch live. Majoris applications should choose DEFAULT and consume the theme instead of hardcoding dark backgrounds, text or titlebars. Explicit application preferences take precedence over system appearance.

Development installation accepts `--variant=light|dark|auto`. Light/dark select a fixed GTK4 user CSS entrypoint; auto links a neutral, comment-only `integration/gtk4-auto.css` and both palettes/assets. It imports neither variant: the factory or GTK4 wrapper must attach the live bridge to supply the active scheme. The journal preserves original files across mode changes and refuses to overwrite later user edits. Installation changes no global GNOME appearance preference.

System tests use an isolated in-memory GSettings backend, exercise prefer-dark/default repeatedly, and restore the original value in `finally`. No persistent WSL preference is changed. Portal/session delivery still requires the actual GNOME environment.

## GNOME Shell

`Majoris/gnome-shell/gnome-shell.css` is the light entrypoint and `gnome-shell-dark.css` its dark counterpart. The Shell-only `Majoris-Dark` alias packages the dark stylesheet under the conventional `gnome-shell.css` name. `scripts/select-shell-theme.sh --light|--dark` selects these names through an enabled User Themes extension. `--auto` watches GNOME colour scheme and restores the preceding Shell theme when the monitor exits. It is a foreground session helper, not an installed background service. The ISO/session can supervise it or perform equivalent native integration. The helper checks for the User Themes schema and has not been run in WSL.

Both Shell files pass grammar and installed Trixie selector checks. Panel, menus, Quick Settings, calendar, notifications, modal dialogs, search/overview, workspaces, dash labels and tooltips have dark styles. St rendering, extension switching, Mutter, fractional scaling and GDM require a real Majoris GNOME VM. Automatic GTK application switching does not certify automatic Shell switching.

## Evidence and native constraints

Artifacts are kept in `artifacts/baseline-light/`, `screenshots/light/`, `screenshots/dark/`, `screenshots/html/`, `screenshots/html-dark/`, `integration/light/` and `integration/dark/`. Reference rendering injects the exact installed normal/italic Plus Jakarta Sans into a temporary copy; the authoritative source is untouched and screenshots are uncropped. The visual report separates LIGHT, DARK, SHARED GEOMETRY, TOOLKIT CONSTRAINTS and VM-ONLY VALIDATION. PASS means the exposed theme treatment was reviewed; it does not assert a native GTK layout is a pixel clone of an HTML simulation.

Native constraints include libadwaita's centered banner message, adaptive toast width, alert-dialog response structure, preference row internals, view-switcher content policy, popover anchoring/arrow, tooltip placement/no HTML arrow and overlay scrollbar behavior. Clock's application-specific SVG strokes remain fixed `#2e3436` in its existing resources; the dark capture exposes their weak contrast. This application asset limitation is recorded as NATIVE TOOLKIT CONSTRAINT (fixed SVG paint cannot be changed by theme text colours). No Clock code or resources were modified.

Settings starts under the WSL GNOME marker but presents no visible surface; a blank capture is rejected and recorded as GNOME SESSION VALIDATION REQUIRED. Files and the existing Clock build have actual captures. The theme should be validated in the target VM before desktop acceptance.


## Theme-state backport ownership

The theme owns GTK3/GTK4 light and dark CSS, the DING `desktopwindow` normal and
backdrop transparency exception, both reusable GTK bridges, Shell light/dark
assets and variant regressions. The OS/session owns global process attachment,
any session LD_PRELOAD dispatcher, extension activation, wallpaper selection and
the full GNOME/Mutter lifecycle. No session dispatcher or desktop extension is
shipped by this repository.

Shell now has explicit descendant colours and separate panel, transient, search,
control, disabled and selected semantic values. The dark panel is #202023;
transients are rgba(40,40,44,.98); search/controls are #28282C. Checked children
stay #FFFFFF in both variants. This avoids a former broad foreground substitution
that also matched `background-color` and made dark surfaces white. See
[the VM regression checklist](theme-state-vm-checklist.md).


## GTK4 location bar

The opt-in location field uses the same semantic tokens in both generated
entrypoints: Entry surface #FFFFFF / #28282C, border #D8D8DD / #3B3B40,
primary text #1C1C1F / #F4F4F5 and focus #6366F1 / #818CF8. Hover and pressed
states use the existing theme tokens. High contrast uses the primary text border without a separate palette. Surrounding dark toolbar controls retain #28282C, #3B3B40
borders and existing shadows. No global control rules or stylesheet imports change.

The source is `design/templates/gtk4-location.css.in`, included after existing
GTK4 overrides by both generators. The factory uses the existing StyleManager
bridge; no separate appearance provider or cached per-widget colours.
[Application integration](gtk4-libadwaita.md#gtk4-location-bar).
