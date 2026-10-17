# Majoris Theme — Complete Widget Showcase · Review notes

## Source authority and scope

The interactive HTML is a design-review artifact, not a native GTK4/libadwaita preview and does not modify theme or Notepad files. It is grounded in these supplied sources:

1. `majoris-gtk-libadwaita-widget-factory-v4-exact-window-icons(8).html`
2. `Majoris-Theme(20261016-225636).zip` — especially `design/tokens.json`, `design/tokens-dark.json`, `design/DESIGN.md`, `design/templates/gtk-common.css.in`, `design/templates/gtk4.css.in`, and `design/gtk-mapping.md`
3. The previously developed Notepad HTML mockups for the proposed 38px native document tab strip, 40px Markdown/editor toolbar, 34px statusbar and source-editor composition.

The mockup's first ten sections represent the established visual language; sections 11–13 explicitly show proposed changes. The composite window in section 1 includes both.

## Proposed changes to approve before Codex

| Theme component | Proposal | Ownership | Verification |
|---|---|---|---|
| Native document tabs | Opt-in `majoris-document-tabs` for `Adw.TabBar`/`Adw.TabView`. Target 38px strip, flat tabs, active 2px indigo underline, non-moving hover, tab width constrained to approximately 220px in the HTML prototype. | Theme styling; document title, dirty state, close/reorder handling from application | Native GTK visual-state tests for light/dark, active/hover/pressed/focus, overflow and modified tabs. Avoid assuming GtkNotebook CSS maps onto Adw.TabBar. |
| Editor toolbar | `majoris-editor-toolbar` opt-in class: 40px toolbar with 28px flat icon actions, quiet separator lines and 4px spacing. | Theme CSS plus application opt-in class | Native Markdown and plain text screen capture; no change to global GtkButton geometry or shared headerbar size. |
| Statusbar | `majoris-statusbar` opt-in class: 34px status area, 28px flat selectors for zoom, encoding, line endings, language. | Theme CSS plus application opt-in | Verify contrast, menu-button hit targets and viewport size in both schemes. |
| GtkSourceView | `Majoris Light` and `Majoris Dark` GtkSourceView XML schemes. The foreground syntax swatches in this preview are **proposed**, not existing token values. | Theme installs schemes; Notepad selects scheme by appearance setting. | Verify source, line number, current-line, caret, selection, syntax and search contrast in GtkSourceView, multiple languages. |

## Existing base values to retain

- Primary ramp: `#EEF2FF`, `#E0E7FF`, `#C7D2FE`, `#A5B4FC`, `#818CF8`, `#6366F1`, `#4F46E5`, `#4338CA`, `#3730A3`.
- Light: background `#F7F7F8`, surface `#FFFFFF`, secondary `#F2F2F4`, hover `#ECECEF`, pressed `#E2E2E6`, text `#1C1C1F`.
- Dark: background `#18181B`, surface `#202023`, secondary `#28282C`, hover `#303035`, pressed `#38383D`, text `#F4F4F5`.
- Radii: 4px controls, 8px windows, cards, popovers and dialogs.
- Window chrome: 48px headerbar, 32x32 window control allocation, exact supplied 16x16 minimize/maximize/restore/close glyphs, buttons on the right.
- Motions: 128ms control fade, 256ms surface. Avoid geometry-moving hover animations.
- GTK Notebook tabs are an existing *separate* component from the proposed native Adw.TabBar tabs.
- Preserve the independently defined dark semantic action, focus and selection roles rather than modifying the primitive indigo ramp.

## Implementation restrictions

- Edit source templates in `design/templates/`, not generated GTK CSS. Regenerate through the existing build scripts.
- Use opt-in semantic classes, avoiding global `tab`, `button`, `box` or `GtkSourceView` rules that could regress Clock, Settings, Files, Terminal or other apps.
- Headerbar geometry and window glyphs are approved base components and should not be altered for Notepad.
- This standalone HTML contains illustrative interactions. The final Vala/GTK app must retain native accessibility, focus handling, keyboard navigation, tab scrolling, drag-and-drop and all existing editing behaviour.
- Native visual/contrast testing remains necessary. Browser rendering is not proof that GTK CSS selectors or size allocations will match exactly.

## Showcase map

01 Composite live application · 02 Tokens & typography · 03 Window chrome & exact icons · 04 Buttons/action states · 05 Text/password/search/validation/chooser fields · 06 Checkbox/radio/switch/segmented selection · 07 Range/progress/loading/banners/toasts · 08 Sidebar/notebook/navigation/layout/scrollbars · 09 Preference rows/table/tree · 10 Menus/popovers/dialog/calendar/file chooser · 11 Proposed native document tabs · 12 Proposed toolbar/statusbar and split editor · 13 Proposed syntax schemes · 14 Icons and review checklist.

Standalone controls are visual approximations; this catalogue covers the theme's relevant common GTK4/libadwaita widget families and proposed controls, not every control class available across GTK's entire extensible ecosystem.
