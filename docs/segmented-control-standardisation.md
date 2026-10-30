# Segmented control corner standardisation

The canonical HTML references now define 4px segmented group corners using
`--r-control` and 2px grouped segment corners. Standalone `.toggle` buttons keep
their 4px radius. Token extraction feeds both variants and both GTK templates;
the toolbar compatibility alias shares the same canonical segment token.

Only radii changed in production CSS. Standard padding remains 2px; toolbar
padding remains 3px and its complete native allocation remains 32px. Colors,
font weights, shadows, transitions, focus rules and native selection are retained.
Dialogs, cards, menus and popovers retain their structural radii.

## Native examples

The factory Navigation gallery includes two-, three- and four-button native
exclusive groups, first/middle/last selections, a disabled segment, Gtk.StackSwitcher,
Adw.ViewSwitcher and a File Properties button opening a real PreferencesDialog.
The existing native Visual States and Toolbars pages retain keyboard focus and
icon-only toolbar examples.

## Reproduce validation

Run on the repository's supported Linux GTK/libadwaita environment:

```sh
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
meson setup build --reconfigure
meson compile -C build
meson test -C build --print-errorlogs
python3 tools/validate-segmented.py
```

The segmented runner produces local evidence under
`artifacts/segmented-control-standardisation/` (ignored by Git like the existing
native evidence). It captures light/dark at 1x, 2x and 125% text, with screenshots,
GSK render node dumps, allocated geometry, focus flags and the realized preferences
hierarchy. `comparison/before.png` reconstructs the previous 8px/4px radii on the
same native widgets using a temporary test provider; `after.png` uses the generated
theme. Their measured allocations are identical, and their native pixels differ.
This comparison is a controlled reconstruction, not an archived application build.

The native test verifies 4px outer and 2px selected corners in GTK render nodes,
including selected hover, press, disabled and focus states. It tests real X11
pointer/keyboard input, native page switching, exclusive selection, unchanged
heights and padding. The radius contract covers both variants/toolkits, ordinary
4px buttons, 8px cards, and 500/600 segment weights.

## Toolkit details

On libadwaita 1.7.6 / GTK 4.18.6, PreferencesDialog generates both header and bottom
Adw.ViewSwitcher controls; each uses `viewswitcher > button` nodes. The shared
selectors reach both, including ViewSwitcherBar's internal switcher. The native
hierarchy JSON records this rather than assuming the dialog's title control.
No dialog or headerbar geometry rules were added.

GTK3 retains its toolkit-specific native focus behavior (`:focus` rather than
GTK4 `:focus-visible`). Its public StyleContext cannot retrieve corner radius
properties; the GTK3 realized-widget test renders its rounded background through
GTK/Cairo, while parsed source contracts enforce the exact 4px/2px values. GTK4
provides stronger native render-node radius evidence. Normal accessibility-driven
text growth is allowed; no widget sizes are forced by the new corner rules.

## Validation results (2026-10-30)

Generation and `generate-theme.py --check` pass. The factory compiles with the
installed GTK 4.18.6 / libadwaita 1.7.6 stack. Both GTK CSS parsers, radius and
toolbar contracts, and the GTK3 realized-widget test pass. All six native segmented
profiles pass, including native GSK corner assertions and pointer selection at
both scales. Screenshots were visually inspected in light and dark modes.

The initial 102-test regression run passed 99 tests; the window-edge capture and
both data-view focus tests failed under concurrent execution. All three passed
when rerun serially. The revised GTK3 fixture also passes after attaching its
stack content to the realized widget tree. No production changes were made to
those unrelated components.
