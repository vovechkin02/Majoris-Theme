# Sidebar finalisation — 26 October 2026

The shared navigation system, canonical references and native factory have been
updated. This pass changes sidebar presentation/composition only; it does not
redesign headerbars, window controls, menus, tabs, editors, buttons, GDM or Shell.
The Shell template has no equivalent owned sidebar component and was not changed.

## Before and after

| Property / rule | Before | After |
|---|---|---|
| Factory/reference preferred width | 212px | 224px, app-owned recommendation |
| Outer top/bottom inset | 12px | 16px |
| Outer horizontal inset | 8px | 8px, unchanged |
| Painted navigation minimum | 34px | 32px |
| Bottom row gap | 2px | 4px |
| Repeating pitch | Approximately 36px | 36px at the standard font |
| Row horizontal inset / radius | 8px / 4px | Unchanged |
| Divider | 1px, potentially repeated in compositions | 1px, explicit native-owner opt-out |
| Normal label | Native 14px/500; reference base 13px | Consistent 14px/500 |
| Selected label | Native 14px/600 | 14px/600, baseline stable |
| Section heading | Reference 11px/700, no reusable native treatment | 12px/600, 8px horizontal inset, 16px/8px group margins |
| Supporting description | No shared sidebar role | 12px/400 secondary text |
| Badge/count | No shared sidebar role | 12px/600, compact 4px corners, trailing allocation |
| Leading icon / gap | Inconsistent or absent in fixtures | 16×16px / 8px |
| Split fixture labels | Plain, centred Labels | Start-aligned icon/label Box in native rows |
| Selected indicator | 2px, 9px top/bottom inset | 2px, 8px top/bottom inset |
| Standard visible stripe | 16px | 16px, grows with enlarged rows |
| Child indentation | App-specific / absent demo | Opt-in 16px beyond parent content |
| Sidebar surfaces | Light #F2F2F4, dark #1D1D20 | Unchanged |
| Selected surface/text/stripe | Existing indigo roles | Unchanged base light/dark roles |
| Default row | Toolkit-dependent residual styling | Explicit transparent, borderless, shadowless |
| Hover / pressed | Incomplete shared specification | Existing neutral hover / pressed roles |
| Selected + hover | No dedicated strengthening | Light p100; dark indigo alpha .22; stripe retained |
| Selected + pressed | No dedicated strengthening | Light p200; dark indigo alpha .28; stripe retained |
| Keyboard focus | Incomplete shared specification | Inset 2px p500 / semantic dark focus |
| Disabled | Toolkit fallback only | Tertiary text, no hover/pressed surface or stripe |
| Backdrop | No explicit shared row treatment | Reduced text emphasis, persistent selection/stripe |
| RTL | Left-only indicator | Mirrored indicator, divider and child inset |
| Motion | Existing control fades | 128ms stationary colour/focus fades; no geometry animation |
| Narrow demonstration | Desktop Box layout only | Native split-view collapse/reveal and selection restoration |

The shared source is `design/templates/gtk-sidebar.css.in`. Geometry and surface
roles derive from the revised canonical HTML/token cascades; the small
`generate_sidebar.py` module selects a supported fixed-inset construction for
each toolkit. All generated GTK3/GTK4 light/dark CSS is synchronized. Original
window glyph assets and primitive colour identities remain unchanged.

## Native demonstrations

The existing factory now has a **Sidebar Design** page with plain/icon examples
and a launch control. The standalone native fixture (`--page=sidebar`) combines
section/list headers, symbolic rows, badges, a disabled row, a long ellipsised
name, GtkExpander children, native scrolling and NavigationSplitView adaptation.
The original split-headerbar fixture now uses proper start-aligned SidebarRows.

Final divider inspection verified one theme-owned `@border_soft` line in the
NavigationSplitView fixture. The native-divider opt-out is reserved for containers
whose native separation is actually visible; applying it here removed the line.

Capture modes under `artifacts/sidebar-finalisation/`:

| Mode / PNG stem | Demonstrates |
|---|---|
| `sidebar-basic` | Plain text rows |
| `sidebar` | Icons, selected navigation, sections, badges, expanded children and long labels |
| `sidebar-states`, `sidebar-focus` | Selected hover, pressed, unselected keyboard focus and disabled navigation |
| `sidebar-selected-pressed` | Persistent indicator during selected press |
| `sidebar-scroll` | Overflow with selected lower row and overlay scrolling |
| `sidebar-narrow`, `sidebar-narrow-content` | 390px native sidebar/content pages and reveal controls |
| `sidebar-rtl` | Mirrored layout and leading indicator |
| `sidebar-large` | Actual enlarged Pango text with naturally taller rows |
| `sidebar-backdrop` | Genuine inactive main window; a small native focus target is also shown |
| `split` | Corrected split-fixture alignment |

Both schemes have full native screenshots, plus representative `light-2x` and
`dark-2x` captures. They are unmodified full-frame X11 screenshots, not HTML
substitutes. Before images from the existing repository capture directory were
preserved in `before/light` and `before/dark`; compare their split/overview panes
with the new views. The updated HTML authorities are also rendered separately
through the existing renderer; they are supplementary design comparisons.

## Validation

Baseline: all 66 pre-existing Meson tests passed before edits. Final suite: all
72 tests passed, with no failures or skips, using exact Plus Jakarta Sans on
Debian Trixie / GTK 4.18.6 / libadwaita 1.7.6. No packages were modified. The final full run used `GIO_USE_VFS=local` and
`--num-processes 4` to isolate file I/O and avoid Xvfb startup contention. An
earlier run concurrent with screenshot capture sampled pre-layout geometry in
the unchanged window-edge test; it passed unchanged in the bounded run.

New tests verify the CSS contract and real native GTK3/GTK4 allocations at both
100% and 200%, including actual GtkStackSidebar wrapper/list ownership. They
measure 32px painted rows, 36px pitch, 16px icons, 8px gaps, 14px Medium/SemiBold,
12px/600 headings and badges, fitting Pango ink, stable selection baselines,
ellipsis, native row states and exact rendered 2px stripes with 8px caps in
both directions. Enlarged text grows rows to 36px and retains fixed caps.

The input test uses real X11 pointer/keyboard events against the Vala fixture:
pointer selection, disabled-row rejection, Down/Return navigation, Tab traversal,
Return disclosure activation, wheel and Home keyboard scrolling, 390px reveal /
navigation and selection persistence after returning to desktop. Home scrolls
the focused row into view; it need not reveal an earlier offscreen group header.

Real interaction exposed two composition issues that were corrected without
altering shared menu behavior: the gallery's placeholder Open/Preview accelerators
intercepted native Return/Space, so those unused actions are disabled only in the
sidebar fixture; native split-view focus restoration could reselect an earlier
row, so the application's chosen row is preserved around breakpoint transitions.
No custom disclosure keyboard controller, animation engine or appearance provider
was added. Native selection, accessibility roles and GtkExpander activation remain.

Evidence is in `suite.log`, `captures.log`, `captures-2x.log`, `html.log`, and
`geometry/` JSON/PNG reports inside `artifacts/sidebar-finalisation/`. Existing
headerbar/window glyph, colour, parser, menu, editor, location, installer and
variant-geometry tests remain enabled and pass. Parsed non-sidebar selector
declarations are identical to the Git baseline in all four GTK entrypoints
(`geometry/unrelated-css-comparison.json`); sidebar widths can intentionally
shift the main content area by 12px. Fontconfig resolves actual Medium and
SemiBold faces (`geometry/font-faces.txt`). The canonical token verification
and deterministic generation checks pass; no unrelated test was weakened.

## Remaining session acceptance

Xvfb/Openbox tests establish native X11 behavior and logical geometry at integer
scales, not Wayland/Mutter or fractional-scaling acceptance. Validate real GNOME
text-scaling settings, fractional scales, system appearance/portal changes,
screen-reader announcements, high-contrast preferences and real application
integration in the Majoris VM. Enlarged-text tests use native Pango attributes:
legacy Xft DPI alone does not enlarge the approved absolute CSS pixel sizes in
this test environment. This limitation is explicit rather than reported as an
OS accessibility-settings pass.

See [integration and ownership](sidebar-design.md) for reusable classes and Vala
composition. Applications choose width, structure, badge values, navigation and
adaptation; installing the theme does not build sidebars for third-party apps.
