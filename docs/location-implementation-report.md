# Location bar implementation and verification

Implemented on 23 October 2026.

## Changes

- `design/templates/gtk4-location.css.in` supplies the seven opt-in location
  classes, standard 4px geometry (updated 29 October 2026), semantic colours, flat 14px/500 breadcrumbs with 14px/600 current emphasis, full-width
  editing and optional high contrast. Both existing generators include it;
  `theme/Majoris/gtk-4.0/gtk.css` and `gtk-dark.css` are regenerated.
- `factory/src/location-bar.vala` implements the simulated path/history component
  and Files-style fixture. The enclosing pill handles unused-space clicks while
  ignoring button descendants. A separate 48px labelled native button provides
  keyboard access to editing. Ctrl+L / Alt+D select the path; Enter validates
  absolute sample paths, Escape/focus loss/outside clicks cancel. Long paths
  scroll to the current folder and labels ellipsize. Navigation is non-destructive.
- Factory build, application dispatch and Headerbars launcher expose
  `--page=location` and `--page=location-editing`. Native Adw.TabBar reuses
  `majoris-document-tabs`. Back/Forward/Up/Home remain standard icon buttons.
- `tests/test-location-contract.py`, `tests/location-native.vala` and Meson cover
  palettes, geometry, selector isolation and actual component/input behaviour.
  `tools/capture-visual.py` adds reproducible location and 480px narrow captures,
  including scrolled diagnostic states.
- `design/gtk-mapping.md`, `docs/gtk4-libadwaita.md`, `docs/dark-theme.md` and
  `docs/testing.md` document styling, application responsibilities and verification.

No reference HTML, official palette, font, common control rules, document-tab
rules, window-control SVGs, GTK3, Shell or GDM sources were changed. The existing
dark import structure and StyleManager bridge remain intact. There is no new
appearance Gtk.CssProvider in the native factory.

## Verification

Linux dependencies were available through WSL (GTK 4.18.6, libadwaita 1.7.6,
Vala 0.56.18). Windows Python lacked tinycss2, so generation and native testing
used the existing Linux dependencies.

- `python3 tools/generate-theme.py`: passed.
- `python3 tools/generate-theme.py --check`: passed.
- `./scripts/test.sh`: 47 tests passed, zero failures/skips/timeouts.
- Native location test: real X11 Ctrl+L, Alt+D, Enter, Escape, full-path selection,
  invalid input rejection, outside click cancellation, breadcrumb pointer click
  without entering editing, empty-space click, history, Up/Home, truncated forward
  history, long-path scrolling, narrow layout, 32×32 toolbar allocations and
  Light → Dark → Light foreground checks passed.
- Both `./scripts/run-factory.sh --light --page=location` and `--dark` launched
  under Xvfb and exited through the existing tree-report mechanism.
- Existing colour, geometry, exact window-control assets, document/editor,
  GTK3 and variant-switching regressions passed. Generated GTK3/Shell outputs
  and window assets have no changes.

Saved local evidence (artifacts are intentionally gitignored):

- `artifacts/location-suite.log`
- `artifacts/location-launch-light.log`, `location-launch-dark.log`
- `artifacts/location-capture-light.log`, `location-capture-dark.log`
- `artifacts/screenshots/light/location.png`, `location-editing.png`,
  `location-narrow.png`, plus corresponding `*-states.png` diagnostic views.
- Matching files in `artifacts/screenshots/dark/`.

Native captures were visually inspected for both appearances, editing, narrow
layout and high contrast. Held flags demonstrate CSS states; they are not proof
of physical pointer hover/press or screen-reader behaviour. Xvfb captures use the
existing native capture workflow without an application appearance provider.

## Remaining application and desktop work

Majoris Files must instantiate the component structure and implement real
filesystem validation, navigation, history, tab-specific paths and keyboard/click
handling. Theme CSS cannot inject that behaviour. The factory accepts simulated
absolute paths and does not test whether real directories exist.

GNOME/Mutter, Wayland, fractional scaling, real portal/desktop appearance changes,
physical keyboard traversal across a complete Files app and screen-reader
acceptance remain unverified. Native Light → Dark → Light checks exercise the
existing application StyleManager bridge, not an actual desktop settings change.


The current 29 October visual contract and universal Toolbar integration are
specified in [Location Bar standardisation](location-bar-standardisation.md).
The original behaviour report above remains historical verification evidence;
current fields share normal Entry surfaces, borders and elevation.
