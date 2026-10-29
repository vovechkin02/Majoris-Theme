# Location Bar standardisation — 29 October 2026

## Result and canonical ownership

The Location Bar is a specialised composite textbox. Its outer field now shares
the standard Majoris Entry radius, border, surface, control shadow and editing
focus; the internal breadcrumbs and entry remain transparent flat controls.

| Property | Previous | Standardised |
|---|---|---|
| Outer / crumb / entry radius | 9 / 7 / 7px | 4 / 4 / 4px |
| Normal crumb | inherited size / 400 | 14px / 500 |
| Current folder | 700 | 14px / 600 |
| Editable path | inherited typography | 14px / 500 |
| Light field | secondary grey | Entry #FFFFFF |
| Dark field | secondary control surface | Existing Entry #28282C |
| Outer border | soft border | Standard 1px @border |
| Outer elevation | none | Existing control shadow |
| Editing focus | separate outline | Standard Entry border and focus shadow |
| Complete normal height | 32px | 32px |

`design/templates/gtk4-location.css.in` reuses `control_radius`, Entry background,
Entry focus border/shadow, existing control shadow and motion definitions.
There is no second field palette or location-specific shadow token. Both HTML
references now demonstrate the composite next to SearchEntry, current/hovered
crumbs, editing focus, long paths and a narrow universal Toolbar. Extracted
`tokens.json` / `tokens-dark.json` include these canonical component rules;
light/dark GTK4 entrypoints are regenerated through the existing workflow.

The light shadow remains `0 1px 2px rgba(20,20,25,.10)`; dark uses the existing
black control shadow plus restrained white inset highlight. Focus remains light
#6366F1 with .24 halo, dark #818CF8 with .34 halo. The transparent inner entry
paints no second shadow, border or focus ring. Breadcrumb keyboard focus uses
native :focus-visible and does not put the outer field into editing mode.

## Native geometry and font measurements

`factory/src/location-bar.vala` now composes a real `Majoris.Ui.Toolbar`, native
LocationBar and Gtk.SearchEntry, using `append_widget(location)` and
`append_control(search)`. Neither internal crumbs nor the inner entry receive
Toolbar control classes. There are no extra application-owned field margins.
The reusable Toolbar source and geometry are unchanged.

Both themes at GDK scale 1 and 2 measure:

| Measurement | Logical pixels |
|---|---:|
| Complete Toolbar | 40 |
| Toolbar vertical / horizontal padding | 4 / 8 |
| Location Bar and SearchEntry | 32 |
| Field top / bottom inset in Toolbar | 4 / 4 |
| Location outer border | 1 on all sides |
| Location internal padding | 2 on all sides |
| Crumb button / internal entry allocation | 26 |
| Crumb button content / label allocation | 24 |
| Label logical line height | 18 |
| Pango layout baseline | approximately 14.5322 |
| Outer native border corner radii | 4 on all corners |

The height equation is 24px child content + two 1px transparent child borders +
4px outer vertical padding + two 1px outer borders = 32px. No vertical translations,
negative margins or fixed baseline offsets are used. Native vertical alignment
centres content. Typography resolves to Plus Jakarta Sans Medium 14px for normal
crumbs and editable paths, and Semi-Bold 14px for the current folder.

All requested strings are measured in current and ancestor positions, testing
both weights. Logical/ink rectangles and actual label layout offsets are checked
against label allocations and the enclosing field's vertical content region.
Representative 100% metrics: uppercase alphabet at weight 500 has ink
(0,3,237,13), logical (0,0,240,18); `gjpqy` at weight 600 has ink (0,4,40,14),
logical (0,0,40,18), fitting its 24px label. Labels and separators share the same
vertical centre. No uppercase/descender clipping was reproduced.

A 2× Pango accessibility-text diagnostic grows LocationBar to 44px, SearchEntry
to 38px and Toolbar to 52px in both themes. These are natural content-driven
allocations, not a forced 32px height. The controls remain vertically centred.
This native attribute test is distinct from real desktop text-scaling acceptance.

Native GSK render-tree reports verify actual 4px outer border outlines, 1px border
widths, matching LocationBar/SearchEntry shadow parameters, and 4px hovered crumb
clips. Focus shadows match when each field receives real input focus. A transparent
inner entry has no visible rounded border to measure in a render node: its 4px
radius is protected by the source contract, while native allocation and render
assertions verify integration and absence of duplicate border/shadow paint.
Gtk.Label metrics come from its actual Pango layout. Gtk.Text does not expose its
internal layout in this GTK4 API, so its report explicitly labels contextual
Pango measurements rather than claiming to inspect its private cursor layout.

## Preserved interaction and targeted fixture fixes

Breadcrumbs retain native buttons, labelled empty-space editing, full-path
selection, Ctrl+L / Alt+D, Enter activation, Escape/outside cancellation and
simulated Back/Forward/Up/Home history. Paths with spaces and long paths are
entered through real X11 events in the tests. The normal fixture still performs
no filesystem operations. Application completion, suggestions, special locations,
mounted volumes and network navigation remain application-owned and were not
implemented or changed in another project.

Breadcrumb labels no longer use character-count minimum widths. A native
Gtk.Viewport with NATURAL horizontal policy preserves their natural measurements
and max-width ellipsis, with scrolling to the current end and logical RTL handling.
Separator artwork is unchanged; the existing chevron is mirrored for RTL.

The real factory's placeholder Open/Preview actions intercepted Return and Space
before text widgets could use them. They are disabled in this fixture only,
matching other native fixture practice. The actual application and global action
architecture are unchanged. This allows the test to verify Enter navigation and
folder names containing spaces using the real factory rather than only stubs.

Disabled crumbs explicitly suppress hover/press/focus paint; an insensitive outer
field applies a single opacity layer. Normal breadcrumb focus remains separate
from editing focus. Shadows and focus never participate in layout.

## Sources and regression tests

Changed source groups:

- Both HTML widget factories, extracted light/dark token files, the opt-in
  location template and generated GTK4 stylesheets.
- Native location fixture: real Toolbar/SearchEntry integration, natural scrolling,
  diagnostic report/snapshot methods and scoped placeholder action handling.
- `tests/test-location-contract.py`: replaces obsolete exceptions with standard
  radius/typography/field/focus checks without deleting coverage.
- `tests/test-location-standardisation.py` and Meson: native geometry, GSK render
  paints, Pango extents, keyboard/pointer input, long/narrow/RTL and large text.
- GTK mapping, GTK4 integration, dark-theme, testing and location documentation.

No common Entry/Button rules, Toolbar implementation or stylesheet, headerbar,
window controls, SVGs, document tabs, sidebar, data views, menus, GTK3 outputs,
Shell, login screen or Majoris Files source were changed. The pre-existing user
change to `Majoris-Theme.zip` was left untouched.

Commands used:

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson setup build --reconfigure
meson compile -C build
meson test -C build --num-processes 4 --print-errorlogs
```

The four targeted LocationBar contract/input/standardisation tests passed at both
100% and 200%. The full suite passed **102 tests**, with zero failures, skips or timeouts.
Results are saved in `artifacts/location-full-suite.log`. Canonical verification checks also confirm
unchanged exact window-control SVG geometry and official palette values.

## Native evidence

`artifacts/location-bar-standardisation/` contains actual GTK renders, not HTML
screenshots or redrawn controls:

- `light/` and `dark/`: default, LocationBar-versus-SearchEntry, Toolbar, hovered,
  pressed and keyboard-focused crumb, editing/focused editing, long-path, narrow,
  RTL and accessibility-text captures.
- `light-2x/` and `dark-2x/`: corresponding 200% captures.
- `geometry/location-bar.json`, `search-comparison.json`, `text-metrics.json`
  and matching `-2x` files contain allocations, border/padding insets, native
  flags, GSK border radii/shadow paints, fonts, ink/logical extents and baselines.
- `comparison/before.png` and `comparison/after.png`: close native Toolbar
  snapshots using identical current fixture composition, respectively with the
  committed original stylesheet and standardised stylesheet. These use GTK/GSK
  to render actual widgets directly, without retouching captured pixels.
- `comparison/light/location.png` also preserves the original fixture capture
  taken before modification; it has the original composition without SearchEntry.

Reproduce native checks with the Meson tests named `location standardisation
native 1x/2x`. Recreate the close comparison against the original Git HEAD with:

```bash
GDK_BACKEND=x11 ADW_DISABLE_PORTAL=1 dbus-run-session -- xvfb-run -a \
  python3 tests/test-location-standardisation.py --comparison
```

The comparison command depends on HEAD retaining the original stylesheet; after
committing this work, use the saved evidence or select the original revision
explicitly when reproducing the baseline. Artifacts are intentionally gitignored.

Remaining desktop checks: GNOME/Mutter/Wayland, fractional scaling, real system
accessibility font preferences and screen-reader acceptance. The available
WSL/X11 stack exercises the existing StyleManager theme bridge. No separate
appearance provider was introduced in the factory.
