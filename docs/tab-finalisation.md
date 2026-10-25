# Tab system finalisation

Document tabs remain native `Adw.TabView`/`Adw.TabBar` widgets, styled only when the
bar has `majoris-document-tabs`. Notebook navigation and segmented view switchers
retain distinct native designs. SourceView palettes, document/terminal fonts,
menus, shortcut keycaps, headerbars and window-control artwork are unchanged.

| Component | Previous | Final |
| --- | --- | --- |
| Complete document strip | 38px | **40px** |
| Strip/tabbox content minimum | 37px | 39px plus 1px divider |
| Individual tab content minimum | 37px | 35px plus 2px vertical padding each side |
| Document horizontal padding | 10px | 8px |
| Normal / selected title | 12px/400, selected 700 | **14px/500**, selected **600** |
| Inactive title | inherited selected weight | 14px/500 |
| Selected underline | 2px, 10px inset | 2px, **8px** inset, inside the allocation |
| Close control | 22px allocation | **24px** allocation |
| Close content / padding / border | 20px / 0 / 1px | 16px / 3px / 1px = 24px |
| Close symbolic image | 16px artwork in a larger image widget | **16×16px image allocation**, unchanged SVG |
| Inter-tab separator | 1px, 8px vertical margins | retained |
| Notebook | existing 36px / 12px padding | retained; 14px/500 and selected 600 verified |
| Segmented outer / child radius | 6px / 4px | **8px / 4px** |
| Segmented padding / child height | 2px / 28px | retained, typography 14px/500/600 |

The tab, bar and tabbox do not each request 40px. Their distinct derived minima
produce a measured total of 40px while allowing larger native text to grow. No
fixed heights, text translations, negative vertical margins or clip suppression
were introduced. Native libadwaita title negotiation, ellipsisation, pinned pages,
reorder, page transfer and overflow remain in use. Native attention can introduce
its own indicator/underline; that is distinct from selected-tab styling.

## Source and validation

`design/editor-tokens.json` owns derived document geometry and typography.
`gtk4-editor.css.in` applies it to the opt-in component. `gtk-common.css.in` and
`gtk-dark.css.in` refine notebook typography/focus and segmented outer radius.
Both canonical widget-factory HTML references demonstrate the same numbers and
reuse the unchanged Majoris close SVG. GTK3/GTK4 light/dark CSS is regenerated;
GTK3 does not receive Adw document-tab rules.

The native editor factory now demonstrates Files (pinned), Favorites, Documents,
notes.md, main.vala and Project Requirements.md, with attention/unsaved state. Its
overflow mode adds the remaining diagnostic names and long filenames. Native
GtkNotebook and switcher comparisons remain in the factory navigation page.

Tests inspect real label, tab, button and image allocations, font descriptions,
Pango ink/logical bounds, ascent/descent, layout origins and baselines. Glyph ink
is checked against the label and each ancestor up to the TabBar. Switching weight
must preserve baseline and strip height. The close button/image allocations must
be 24px/16px. GTK3 and GTK4 notebook labels are measured directly, including GTK3's
separate notebook tab-label API, and their baselines must agree within 1 logical
pixel. Text-only StackSwitcher children measure 28px.

Pin/reorder/close, native overflow and TabView page transfer are exercised. The
inactive screenshot uses a second real native window to establish deactivation.
Openbox did not forward GTK BACKDROP state, so the test records that limitation
and holds native BACKDROP flags for the Medium typography assertion.
`backdrop-state.json` distinguishes real deactivation from this held-state test. Held hover/focus states are labelled review
fixtures, not custom appearance CSS.

```bash
python3 tools/extract-design-tokens.py
python3 tools/generate-theme.py
python3 tools/verify-design-tokens.py
python3 tools/generate-theme.py --check
meson compile -C build
meson test -C build --print-errorlogs
MAJORIS_CAPTURE_PAGES=editor,editor-focus,editor-states,editor-overflow,navigation scripts/capture-visual-regressions.sh --both
MAJORIS_CAPTURE_PAGES=editor,editor-focus,editor-states,editor-overflow,navigation MAJORIS_CAPTURE_SCALE=2 scripts/capture-visual-regressions.sh --both
```

Native screenshots and measurements are under `artifacts/tab-finalisation/`.
The ten-case tab matrix covers both toolkits, both palettes and 100%/200% device
scale, plus two 125% text-enlargement cases. Xvfb's `GDK_DPI_SCALE` alone did not
enlarge the fixed-pixel CSS font; those two cases explicitly apply an equivalent
17.5px native Pango size and assert that glyph height increases. A separate 40px
Pango-text case verifies that the strip grows. These are text-layout tests, not a
claim of fractional compositor validation or GNOME preference forwarding.

## Original clipping: confirmed evidence versus hypotheses

`tools/diagnose-tab-clipping.py` was run with the original generated light/dark
styles from the starting Git revision, isolated under `baseline-theme/`. It
measured a 38px native strip and **zero vertically clipped labels**, including
Favorites, Files, Find, Format, ascenders, descenders and punctuation. Its before
screenshots and measurements are retained alongside existing prior editor captures.

The original application's clipped capital F was **not reproduced**. The old
37px content minimum, zero vertical padding and 12px/400 typography were confirmed
implementation differences, but cannot honestly be labelled the proven cause of
that screenshot. In the revised native tree, 35px title allocations accommodate
18px logical text height at default size; the tab is 39px and the complete bar is
40px. Medium/SemiBold share a stable baseline. Parent-allocation checks protect
against a different clipping layer rather than checking CSS text alone.

No affected Files/Notepad/Terminal application source or inspectable screenshot
file was attached. This repository contains the theme and native integration
fixtures, not those applications, so no application-level fix is claimed.

## Application integration and remaining session checks

Use the documented component on the real application tab widget:

```vala
var documents = new Adw.TabView();
var tabs = new Adw.TabBar();
tabs.view = documents;
tabs.add_css_class("majoris-document-tabs");
tabs.expand_tabs = false;
```

Keep pinning, dirty state, close confirmation, `create-window`/drag-detach and
page-transfer handlers in the application. The factory verifies the native page
transfer primitive; actual cross-window drag/drop needs a desktop session. Apply
the class only to Adw.TabBar, not GtkNotebook, a location bar or a custom Files tab
widget. GtkNotebook uses the navigation contract; an unrelated custom tab widget
needs an explicit application integration after inspection. Terminal/VTE and
SourceView document typography must remain application-owned.

For the affected application, run it with GTK Inspector enabled (`GTK_DEBUG=interactive`),
select Favorites and identify its actual widget class and provider cascade. Check
the class attachment, effective font, label/tab/ancestor allocations, baselines,
Pango ink and any application CSS/provider priority. Compare 100%/200%, both weights,
and enlarged text. Verify Fontconfig Medium/SemiBold discovery. Export that tree
and allocation evidence before attributing the defect to the theme.

True 125%/fractional Wayland scaling, GNOME accessibility-preference forwarding,
real pointer detach/reorder, screen-reader behaviour and Mutter composition still
require the repository's GNOME VM workflow. Existing compiler deprecations and WSL
GVFS/portal warnings are retained; failures are not suppressed.

Final validation: **66 Meson tests passed**, with generation reproducibility, GTK
CSS parsers, existing menu/headerbar regressions, the native ten-case tab matrix
and palette geometry comparison. The compiled factory capture workflow completed
for all five requested pages in both variants at both device scales. Screenshot
links are indexed in `artifacts/tab-finalisation/README.md`.
