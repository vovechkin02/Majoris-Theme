# Switch standardisation

Native switch tracks and thumbs use 4px corners. Track CSS remains 34×16px minimum content, 2px padding and a 1px border, yielding a measured 40×22px allocation. Structural preferences groups stay 8px; no toggle-button, segmented, checkbox or radio rules changed.

Open `./scripts/run-factory.sh --page=switches --light` (or `--dark`). The Switches page includes native Gtk.Switch, RTL, Adw.SwitchRow, disabled rows, ActionRow suffixes, PreferencesDialog and a comparison with buttons, checkboxes and segmented controls. Tab/Space use native GTK focus and activation; row suffixes use activatable_widget. Appearance follows the existing factory menu and theme bridge.

The shared template supplies neutral hover/press, persistent Indigo checked hover/press, stationary 128ms colour/border/shadow/opacity transitions and subdued backdrop shadows. GTK4 uses :focus-visible; GTK3 keeps :focus because it lacks GTK4 keyboard-visible CSS semantics. GTK3 therefore may show focus after a pointer activation; accessible keyboard focus is preserved.

Disabled opacity is sourced from the HTML `.switch.is-disabled` token (0.58). GTK4 clears libadwaita's inherited `filter: Opacity(var(--disabled-opacity))` specifically on switches. Native render-node tests confirm one opacity node, including switches in disabled Adw.SwitchRow, rather than compounded opacity. Thumb opacity remains 1. Checked dark thumbs retain the existing white token; neutral dark thumbs retain their existing surface token.

## Geometry evidence

GTK4 4.18.6 divides the 34px content width in half, allocating the native slider 17×16px, rather than the approximate 16×16px specification. The existing 14px minimum plus borders remains untouched. Slider content-coordinate bounds span x=0 or x=17, y=0; the widget contributes 3px border/padding insets. Changing native allocation to force 16px would alter existing geometry. Tests assert the measured 17×16px size, stable 40×22px track, containment, borders/padding and 4px rendered radii. GTK3's internal slider CSS node is not exposed as a GtkWidget; GTK3 tests measure the outer allocation and native input, while stylesheet contracts assert thumb radius/minimums.

## Reproduction and artifacts

Run the normal extract/generate/verify tools, build, then:

```sh
meson test -C build --num-processes 2 --print-errorlogs 'native switches*'
```

Twelve cases cover GTK3/GTK4, light/dark, 100%/200% and enlarged fonts. Tests drive real pointer presses/clicks, Tab and Space, disable/re-enable and RTL; GTK4 additionally renders libadwaita rows and PreferencesDialog. Render-node assertions check real 4px radii, a 2px focus ring, thumb containment and non-compounded disabled opacity. CSS parser and radius-contract tests cover both toolkits and palettes.

Unedited native screenshots, GTK4 render nodes and switch-dimensions.json reports are under `artifacts/switch-standardisation/gtk{3,4}/{light,dark}/scale-{1,2}/`, with additional `scale-1-large-font` directories. Each has checked, unchecked, hovered, pressed, focused, disabled and RTL captures; GTK4 adds rows/dialog. `before-radius-8px.png` reconstructs only the former track radius with a temporary native CSS provider; `unchecked.png` shows the final radius at identical dimensions. Captures are generated, ignored artifacts, retained locally rather than added to theme installation.

WSL/Xvfb establishes native toolkit rendering and input, not GNOME/Mutter compositor, fractional scaling or assistive-technology end-to-end acceptance. Those session checks remain part of the existing VM workflow.

## Validation result

Debian WSL build and token verification/generator consistency pass. The complete Meson run passed 118/120 initially; its two geometry failures were caused by eagerly constructing the new hidden page. Lazy page creation fixed that cause, and both existing geometry tests then passed. All twelve switch matrix cases pass; after adding row/dialog Space activation, all six GTK4 cases pass again. Both GTK CSS parsers and radius contracts pass. `git diff --check` passes. No existing test was removed or weakened.
