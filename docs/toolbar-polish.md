# Universal Toolbar — final polish

The existing `Majoris.Ui.Toolbar` / `ToolbarGroup` API remains the single installed
GTK4 component. No navigation, command or editor widget types were introduced.

## Causes and corrections

| Source cause | Correction |
| --- | --- |
| Canonical toolbar padding was 16px horizontally | Both HTML references/tokens and four generated GTK stylesheets now use 8px |
| Root CSS gap 8px differed from grouped controls; native spacing could add to CSS spacing | Public root/groups use native spacing 4, CSS spacing zero; visible logical boundaries add only 4px, or 12px in optional major mode |
| Generic focus styles and GTK's sticky keyboard-visible window flag survived some pointer interactions | Scoped 2px `:focus-visible` outline; passive action gestures reset GTK's own window focus-visible flag on pointer press, without claiming events or replacing keyboard navigation |
| Global button opacity plus libadwaita's native disabled filter and image dimming compounded | Toolbar-only opacity .58 with native filters/child dimming cleared; global disabled opacity remains unchanged |
| Flat controls inherited primary 600 weight | Flat normal 14px/500, checked 14px/600; primary 600 and menu 500 remain; Pango reserves both toggle/segment weights |
| Native top-bar wrapper added a band below Files tabs | Application-parent composition reproduced and corrected in the factory; exact Files integration below |

Child-model and visibility observation updates group boundaries and separator
coalescing after append, insertion, removal, reordering and hiding. Empty groups
hide; removed groups lose managed margin classes. RTL reverses the boundary margin.
Icon/label action boxes use one native 8px gap. Icon artwork and 16px allocations
are unchanged. Unmarked application composites, breadcrumb internals, search
padding, menu rows, document tabs, headerbars and statusbars retain their rules.

## Native measurements

The public-component probe uses the installed-library build dependency, real GTK
allocations, Pango layouts and actual X11 pointer/keyboard events. Both palettes
run at GDK_SCALE 1 and 2; reported coordinates are logical pixels.

| Measurement | Result |
| --- | --- |
| Standard / compact complete strip | 40 / 40 |
| Standard / compact control | 32 / 28 |
| Standard / compact top/bottom allocation | 4 / 6 |
| Left and right outer inset | 8 / 8 |
| Direct controls / group members | 4 / 4 |
| Logical / optional major boundary | 8 / 16 |
| Segmented container / inner segment | 32 / 24 |
| Two adjacent toolbar rows | 80 |
| Correctly composed document tabs plus two rows | 120 |
| Keyboard outline / shared divider | 2 / 1, without allocation changes |

Pixel tests distinguish pointer focus from keyboard focus on raised, flat and
selected segmented actions, and verify one divider pixel inside its owner's row.
Disabled raised, flat, icon-only, icon/label, menu, segment and compact samples are
measured against their actual surfaces rather than assuming the segmented surface
is white. Their effective glyph opacity is approximately .58.

Pango evidence records size, weight, resolved font face, label allocation, logical
and ink bounds, layout offsets and baseline. The named samples include New Folder,
Back, Forward, Refresh, Sort, Favorites, Files, Format, Undo, Redo and Properties.
Normal layouts resolve Plus Jakarta Sans Medium/Semi-Bold at 14px; logical text
height is 18px and layout baseline 14px. Ink plus layout offset stays within the
label. Selected flat/segment allocations remain stable, including 24px runtime segment
fonts, restoration to 14px, renamed labels and segments inserted after mapping.
Application-provided minimum label widths are retained. Existing native tests also
exercise 40px accessibility text and verify that the strip grows naturally, menus
retain their typography, and 480px windows scroll to keyboard focus.

## Majoris-Files application integration

The sibling checkout was inspected **read-only**. In `src/views/browser.vala:143`
its browser already uses vertical spacing 0; navigation and command rows are
appended in scrollers at lines 329 and 415. Their heights are not the extra band.

The remaining cause is `src/window/window.vala:165–166`: the document TabBar is
added as another `Adw.ToolbarView` top bar while TabView is its content. On the
tested libadwaita 1.7.6, the native `.top-bar .collapse-spacing` wrapper adds 3px
below that group. The faithful `toolbars-files-parent` fixture measures tabs 40,
navigation at y=43 and commands at y=83 relative to the tab strip. The two toolbars
still total 80; the extra 3 belongs to the application parent.

Replace those two Files composition lines with:

```vala
var document_content = new Gtk.Box(Gtk.Orientation.VERTICAL, 0);
document_content.append(tabbar);
document_content.append(tabs);
tabs.vexpand = true;
toolbar.content = document_content;
```

Keep the headerbar in `toolbar.add_top_bar(header)` and the existing
`tabbar.view = tabs`. The corrected `toolbars-stacked` fixture uses this exact
hierarchy and measures navigation y=40 and commands y=80. Do not add a separator,
external margins, negative offsets, or a global rule stripping ToolbarView/tab
padding. The TabBar owns its existing bottom divider; the navigation strip owns
one inset bottom divider between the two toolbars. A final command divider is
optional at the content boundary. **No Majoris-Files file was modified.** Files
must also load/rebuild against the updated Theme CSS and UI library.

## Compatibility and generation

Legacy navigation/command aliases keep 8px insets. CSS-only GTK4 legacy boxes use
native spacing 0 and CSS spacing 4, including groups; native GTK3 uses spacing 4.
Both have logical 8/16px boundaries. Native groups inside legacy rows are also
measured: an internal marker prevents a duplicated inner gap. The installed GTK4
component always uses
native spacing 4 with CSS spacing zero. Do not add both gaps. Legacy editor
geometry stays 40/28 with toolbar-only medium/selected typography and disabled
filter corrections; statusbar rules are unchanged. View-switcher remains an alias.
GTK3 retains native accessible `:focus`, omits GTK4 pointer-only rules and maps the
icon filter reset to its supported icon-effect property.

Canonical source is the light/dark HTML cascade, extracted tokens, and CSS
templates. Generated output is not maintained by hand. Verification commands:

```sh
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson compile -C build
GIO_USE_VFS=local meson test -C build --num-processes 4 --print-errorlogs
```

## Evidence and validation

The complete regression suite passes **100/100**. The focused toolbar/API/staged
consumer matrix also passes **13/13**, including the exact parent composition.
Tests cover GTK3 3.24.49, GTK4 4.18.6 and libadwaita 1.7.6. The staged consumer
compiles/runs using the installed header/VAPI/pkg-config outputs without
libadwaita or factory dependencies. Existing callback, menu, keyboard and widget
finalization checks pass. No tests were removed or failures suppressed.

- [Full regression log](../artifacts/toolbar-polish/regression-final.log)
- [Focused matrix log](../artifacts/toolbar-polish/toolbar-tests-final.log)
- [Public component geometry/Pango/input at 1×](../artifacts/toolbar-polish/geometry/public-1x.json)
- [Public component geometry/Pango/input at 2×](../artifacts/toolbar-polish/geometry/public-2x.json)
- [Factory geometry, including parent reproduction and correction](../artifacts/toolbar-polish/light/factory-measurements.json)
- [Scope verification](../artifacts/toolbar-polish/scope-verification.json)
- [Native evidence index](../artifacts/toolbar-polish/README.md)

The evidence index pairs native before/after windows to show the 16px → 8px
inset change. Screenshots are unaltered native X11 captures. Canonical HTML is also rendered
with the locally installed exact font; placeholder HTML glyph artwork is unchanged.
Xvfb verifies native widgets, not GNOME/Wayland compositor behaviour, fractional
scaling, screen-reader announcements or desktop preference forwarding. Those
remain session/VM checks. The pre-existing modified `Majoris-Theme.zip` is untouched.
