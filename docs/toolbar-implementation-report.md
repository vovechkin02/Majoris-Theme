# Universal Toolbar implementation and validation

The toolbar system now has one public GTK4 container, `Majoris.Ui.Toolbar`,
packaged as `majoris-ui-gtk4`. The same class is instantiated for file navigation,
file actions, formatting and playback. There are no purpose-specific public widget
types or surface tokens. Standard/compact density and per-item flat treatment are
independent options. All new styling remains opt-in.

## Changes

- `ui/toolbar.vala` implements the GTK4-only container, lightweight arbitrary-content
  groups, native append/prepend/insert/move/remove operations, separators and expanding
  spacers. Empty groups and redundant separators are managed through its API. Native
  callbacks, ownership, focus and menu handling remain GTK's responsibility.
- `ui/meson.build` installs the shared library, SONAME, C header, VAPI, GTK4 deps
  and pkg-config metadata. The factory consumes the dependency rather than compiling
  a second copy. The existing GTK3/GTK4 theme bridges remain separate.
- Canonical light/dark HTML now shows one neutral toolbar with different contents,
  densities and item treatments. Tokens and all four GTK3/GTK4 generated stylesheets
  were regenerated through the existing pipeline. `generate_toolbar.py` derives
  complete standard/compact dimensions; there is no parallel stylesheet generator.
- `gtk-toolbar.css.in` shares the segmented implementation with its deprecated
  view-switcher alias. Legacy navigation/command names alias the neutral strip.
  Existing editor CSS remains unchanged for applications still using that class.
- The factory uses the packaged component in all four examples, with native
  location/search, menus, icon and text segments, toggles, DropDown, Entry,
  progress, spinner and volume scale. Extra action inserts/removes Queue through
  the public API. Existing fixture modes remain usable.
- The specification documents API ownership, Vala/Meson consumption, native GTK3
  composition, compatibility and migration. The README points to the new contract.

## Native measurements

| Allocation | Standard | Compact |
| --- | --- | --- |
| Toolbar | 40px | 40px |
| Icon button | 32×32px | 28×28px |
| Text action / search | 32px | 28px |
| Icon artwork | 16px | 16px |
| Within-group / between-group gap | 4px / 8px | 4px / 8px |
| Outer horizontal padding | 16px | 16px |
| Top/bottom control clearance | 4px | 6px |
| Generic segmented container | 32px | 32px |

The compiled public-component factory additionally measures its formatting strip
at 40px with 28px buttons, mixed strip at 40px, selector at 32px, location shell at
32px and existing crumbs/editing entry at 26px. Normal and true 480px-wide fixtures
are checked. Geometry is identical across light/dark, GTK3/GTK4 and 1×/2× cases.
The nested location entry's 26px allocation is intentional compatibility geometry,
not the general toolbar field contract.

Pango tests cover action/menu labels, supporting labels and compact ascenders and
descenders, logical/ink extents, widths and baselines. Ordinary and compact flat
hover/pressed/focus/backdrop states retain allocations and text positions. Native
exclusive toggles and Space activation work; narrow focus reveals off-screen items.
Disabled controls and selected states are exercised. Popover labels retain native
14px/500 menu typography, demonstrating style isolation. Enlarged action text grows
its strip instead of being clipped. GTK reduced-motion settings remain disabled
through the native runs; no positional animation is added.

The mixed-controls measurement initially caught a 34px native scale causing a 42px
strip. An explicit opt-in toolbar scale class removes excess vertical scale padding;
ordinary scale styling is untouched. GTK4 reports content-relative child coordinates,
so inset checks combine realised geometry with native computed GTK padding. Native
lifetime testing clears window focus and popup parenting before releasing the root;
its weak finalization callback confirms that the component releases owned children.

## Validation

The full regression suite passed **98/98**. After adding further compact typography
and flat-state assertions, the focused toolbar/API/package matrix passed **11/11**.
No failures were suppressed or tests removed. Coverage includes the existing
headerbar, window, menus, tabs, editor, location, sidebar, data-view, SourceView,
Shell, colour, CSS-parser and generator checks.

The staged-package test installs to a temporary DESTDIR, verifies all development
outputs, uses pkg-config flags and the installed VAPI/header to compile a separate
Vala consumer, and runs it without Majoris CSS. The consumer tests empty construction,
append/prepend/insertion/reordering/removal, arbitrary widgets, groups, separator
cleanup, spacers, density/item modifiers, native exclusive selection, a real menu,
keyboard traversal, retained application callbacks and finalization. It links GTK4
and the public library, with no widget-factory or libadwaita dependency.

Commands:

```sh
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson compile -C build
meson test -C build --print-errorlogs
python3 tools/capture-universal-toolbar.py
python3 tools/report-universal-toolbar.py
```

Native captures cover all four examples, compact density, held interaction states,
dynamic insertion, location editing, menus and narrow windows in both palettes at
both display scales. GTK3 styling captures and standard/compact geometry, state and
text reports are consolidated in [the evidence index](../artifacts/universal-toolbar/README.md).
Screenshots are native Xvfb/X11 captures; no HTML or image composites replace them.

## Compatibility and limits

Only Majoris-Theme changed. Existing applications can keep their classes while
migrating. Navigation/command classes now use the neutral universal surface; legacy
editor controls retain 28px flat styling. New applications use one class with
optional density and item modifiers. Existing artwork and unrelated components
retain their source definitions. The already modified archive in the workspace was
not edited by this task.

The packaged core currently targets the repository's GTK4 4.18 baseline. GTK3 has
native composition/CSS compatibility, not a compiled wrapper. There is no GIR;
C headers and Vala metadata are supplied. Exact Majoris styling requires Majoris
CSS; without it the component uses ordinary GTK appearance. Applications own
adaptive layout, shortcuts, actions, labels and accessible names. Direct GtkBox
mutations bypassing helpers leave separator/group visibility with the caller.

Xvfb does not establish actual GNOME/Wayland compositor behaviour, fractional
scaling, screen-reader output or session-level accessibility/reduced-motion
preference forwarding. These remain desktop/VM checks. Native menu surface captures
accompany window views where root X11/ARGB screenshots omit popup pixels.
