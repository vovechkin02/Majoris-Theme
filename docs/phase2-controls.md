# Phase 2 — native GTK control foundation

Phase 2 standardises `Gtk.Calendar`, `Gtk.LinkButton`, `Gtk.EditableLabel`,
`Gtk.Paned`, `Gtk.FlowBox`, `Gtk.Expander` and `Gtk.SearchBar`. Applications use
these native widgets; Majoris supplies their appearance. No replacement control
classes, custom renderers, date logic, resizing logic or key-dispatch framework
were added. The primary baseline is GTK 4.18 / libadwaita 1.7 on Debian 13.

## Shared design and source architecture

Ordinary interactive corners are 4px, structural tiles/surfaces 8px, and internal
boundaries square. Focus uses 2px semantic Indigo. Icons are 16px. Flat icon
buttons are 32px; spacing follows 4/8/16px. Existing 128ms colour/shadow transitions
remain stationary. GTK owns revealing, dragging and disclosure animations.

The light/dark HTML references define the Phase 2 roles and examples. Extracted
JSON remains generated. `gtk4-phase2.css.in` and `gtk3-phase2.css.in` are appended
by the normal light/dark generator after broad defaults, so LinkButton and Calendar
navigation override ordinary button elevation without touching ordinary buttons.
`generate_phase2.py` derives native 10.5pt/9pt text from canonical 14px/12px roles
at 96 DPI, allowing the new explicit typography to follow GTK text DPI. Font family
comes from the existing Plus Jakarta Sans configuration, with native fallback.
EditableLabel and arbitrary FlowBox contents inherit their parent text roles.

| Role | Light | Dark |
| --- | --- | --- |
| Surface | #FFFFFF | #202023 |
| Raised/background | #F2F2F4 / #F7F7F8 | #28282C / #18181B |
| Hover / pressed | #ECECEF / #E2E2E6 | #303035 / #38383D |
| Primary / secondary text | #1C1C1F / #626269 | #F4F4F5 / #A9A9B0 |
| Soft divider | #E5E5E9 | #313136 |
| Focus | #6366F1 | #818CF8 |

Selection reuses existing palette and data-view semantic selection paint rather
than redefining primitive colours. Disabled and backdrop states remain legible.

## Calendar

GTK4 exposes `calendar.view > header` with native button, month stack and year
label children, then `grid > label` nodes with `day-name`, `week-number`,
`day-number`, `other-month` and `today` classes. Selection is `:selected` and
marking is `:checked`; these were checked on realised GTK 4.18 widgets.

The root uses a normal surface without border or shadow. It is square by default;
`majoris-calendar-surface` optionally gives the independent root an 8px structural
radius. Header labels use 14px/600, day labels 14px/500, weekdays 12px/600 and week
numbers 12px/400. Native flat navigation buttons allocate 32×32px with 16px icons.
Days have 32px minima and 4px corners; locale, heading widths and font metrics may
increase cells. No locale ordering or minimum/natural-size calculation is replaced.

Today has an inset Indigo marker; selected days have a strong persistent Indigo
fill with white text. Today plus selection adds a white inset marker. Marked dates
use double underlining without inheriting an unrelated checked fill. Other-month
dates use secondary text. Focus, hover, pressed, disabled and backdrop are scoped
to the native nodes. Month/year navigation, date marking, keyboard selection,
scrolling, RTL and week numbers remain GTK functionality.

```vala
var calendar = new Gtk.Calendar();
calendar.show_week_numbers = true;
calendar.mark_day(12);
calendar.day_selected.connect(() => {
    var chosen = calendar.get_date();
});
```

The factory pins its displayed month/selection to 15 October 2026 and marks 12.
GTK's today marker intentionally uses the execution environment's real clock;
tests separately select today and a different date in that month. Thus fixture
selection is reproducible without falsifying GTK's date logic. `phase2-calendar`
and `phase2-calendar-popover` show embedded and native-popover composition.

GTK3 uses its legacy Calendar CSS classes/gadgets rather than GTK4 label nodes.
Its day-cell internals are not individual GtkWidgets, so GTK3 captures and root
measurements supplement primary GTK4 cell measurements.

## LinkButton

Native `button.link` is automatic; no application class is necessary. Default,
hover, active, visited, disabled and backdrop rules explicitly clear inherited
raised backgrounds, borders, shadows, ordinary height and horizontal padding.
The direct label remains underlined and uses 14px/500. Hover/pressed/visited use
existing Indigo steps; focus adds a 2px outline without changing layout. The
visited pseudo-class is supported and exercised through `visited` on this baseline.

```vala
var link = new Gtk.LinkButton.with_label("https://example.org", "Documentation");
// For a controlled test, handle activation and return true to avoid launching a URI.
link.activate_link.connect(() => { return true; });
```

This is still a native LinkButton: its URI, accessible link role, activation signal,
visited state and context/copy menu are not replaced. Tests intercept activation,
so no website opens. An ordinary button alongside it confirms the narrower inline
allocation. GTK3 receives the same native `.link` styling. The factory Links section
includes inline explanatory text, unvisited, visited and disabled links; native
state captures additionally cover hover, press, keyboard focus and backdrop.

## EditableLabel

The realised hierarchy is `editablelabel > stack > label/text`, with an additional
native context popover. Display is transparent, borderless and unpadded, with no
forced height or font role. Display-mode keyboard focus has a 2px external Indigo
outline, without introducing a permanent input box. `majoris-editable-discoverable` opts into subtle hover
feedback. Editing styles the native `text` node, not an imaginary GtkEntry.

A 4px radius and inset border/focus paint provide the textbox appearance without
adding border or padding to layout. Selected text/caret and native text actions
remain GTK's. The display and editing render nodes retain the same text baseline;
normal row and compact tile parent allocations are measured across transitions.

```vala
var name = new Gtk.EditableLabel("Quarterly report.txt");
name.add_css_class("majoris-editable-discoverable"); // optional hover affordance
name.notify["editing"].connect(() => { /* observe native editing */ });
```

The gallery shows a body label, compact file tile, list row and document-title
layout. Enter, Escape, commit, cancellation, selection, Unicode, punctuation,
long/multiline source strings and RTL are exercised without custom key handlers.
The text editor is GTK's single-line `Gtk.Text`; this does not turn EditableLabel
into a multiline editor. Real IME/preedit composition and platform input-method
integration require an interactive desktop session; CSS preserves the native text
node and selection machinery. There is no GTK3 replacement/backport.

## Paned

`paned > separator` is the only separator hierarchy targeted. Horizontal Paned
gets an 8px horizontal gutter containing a centred 1px vertical line; vertical
Paned gets an 8px vertical gutter with a centred 1px horizontal line. `.wide`
retains a larger 16px gutter. Borders, padding, shadows and internal radius are
zero. Hover increases emphasis, drag uses semantic Indigo, and actual keyboard
focus adds a 2px inset indication without reallocating either pane.

GTK4 can propagate `focus-visible` to ancestors. The new Calendar, Paned and Expander focus
rules additionally require actual `:focus`, so a focused child field does not
highlight its parent handle/header. Native pointer dragging and F8/arrow-key
resizing remain GTK operations; no position formula is implemented by the theme.

```vala
var split = new Gtk.Paned(Gtk.Orientation.HORIZONTAL);
split.start_child = new Gtk.Entry();
split.end_child = new Gtk.Label("Content");
split.wide_handle = false;
```

Both toolkits get their native separator rules. Tests measure the 8/16px gutter
separately from the rendered 1px paint, including a pixel-alpha coverage check.
Native pointer coordinates account for physical display scale. The gallery adds
vertical/nested and wide/RTL examples. Generic GtkSeparator styling is unchanged.

## FlowBox and FlowBoxChild

Neutral FlowBox remains a layout container with transparent, borderless children;
it receives no tile dimensions, artwork or layout spacing policy. This preserves
ControlFlow and other selection-disabled layout uses. Selectable tiles must opt in:

```vala
var tiles = new Gtk.FlowBox();
tiles.add_css_class("majoris-flow-tiles");
tiles.selection_mode = Gtk.SelectionMode.MULTIPLE;
tiles.row_spacing = 8;
tiles.column_spacing = 8;
tiles.insert(new Gtk.Label("Favorites"), -1);
```

Opted-in `flowboxchild` nodes receive 8px content-tile corners and 8px padding,
neutral hover/press, native `:selected` semantic paint, disabled/backdrop treatment
and a 2px focus outline. `majoris-flow-compact` selects 4px corners for compact items.
No fixed width/height, forced caption font, artwork or global label rule is added.
The `rubberband` CSS subnode uses translucent Indigo with a 1px border. Native
selection classes are never emulated with an application `.selected` state.

None/single/browse/multiple modes and wrapping are exercised in both toolkits.
GTK4 also exercises Shift-arrow range selection and a real pointer rubberband
sequence; the latter creates a native CSS node rather than a public GtkWidget.
The harness yields between pointer events so GTK observes both drag endpoints.
GTK3 compatibility runs verify native multi-selection and keyboard selection;
they do not claim the GTK4-specific rubberband diagnostics.

GTK4 node behavior was cross-checked against the versioned
[GTK 4.18.6 FlowBox implementation](https://raw.githubusercontent.com/GNOME/gtk/4.18.6/gtk/gtkflowbox.c).

## Expander

GTK4 uses `expander-widget > box > title > expander/label`, while GTK3 uses
`expander > title > arrow/label`. The generic header has a 32px minimum, 4px corners,
14px/500 text, a 16px native disclosure indicator and 8px gap where CSS supports it.
Only its header receives hover, pressed and focus paint. Expanded content remains
naturally sized without automatic border, padding or cards. Native disclosure
state, direction, keyboard activation and content accessibility remain intact.

```vala
var expander = new Gtk.Expander("Advanced options");
expander.child = new Gtk.Entry();
```

All new rules explicitly exclude `majoris-sidebar-group`. The existing sidebar
spacing, typography and indentation remain authoritative. Adw.ExpanderRow exposes
a different row hierarchy and does not match these rules. The gallery includes
collapsed/expanded, long, disabled, nested/form and sidebar comparison instances.
Tests measure header independently of expanded content and toggle with Space.
GTK3's older indicator/gap machinery retains native layout where its CSS lacks
GTK4 border-spacing support.

## SearchBar

GTK4 uses `searchbar > revealer > box > child/button.close`. The root is transparent
with no outer padding or independent card. Insets of 4px vertical/8px horizontal
belong to the revealed inner box, with an 8px child gap. The existing SearchEntry
contract is unchanged. The close button gets flat neutral 32×32px/16px icon styling,
4px corners and 2px focus; it never receives destructive window-close red.

```vala
var bar = new Gtk.SearchBar();
var entry = new Gtk.SearchEntry();
bar.child = entry;
bar.connect_entry(entry);
bar.show_close_button = true;
bar.set_key_capture_widget(window);
// Bind a toggle to search-mode-enabled or set it from application actions.
```

Native capture/reveal/focus and Escape dismissal work without custom key handlers.
There is no universal outer height. GTK4 hidden allocation is zero; revealed height
is determined by content. GTK3 uses its native SearchBar/Revealer and may report a
1px allocated hidden widget due to its native allocation clamp, with no added theme
padding or border. This documented toolkit tolerance is not imposed on GTK4.

## Factory, tests and evidence

Open **Phase 2 Controls** in the factory sidebar or use `--page=phase2`.
Individual modes are `phase2-calendar`, `phase2-calendar-popover`, `phase2-links`,
`phase2-editable-label`, `phase2-editing`, `phase2-paned`, `phase2-flowbox`,
`phase2-expander` and `phase2-searchbar`. Widgets remain interactive. The fixture
intercepts links using an invalid-domain URI and does not launch external pages.
All appearance comes from theme templates, without factory CSS providers.

`test-phase2-contract.py` verifies real selectors, extracted roles, geometry,
registration and scoped isolation. `test-phase2-native.py` drives actual widgets,
not mocks, across GTK4 Cairo/GL/default renderers, 1×/2×, both palettes and enlarged
text, plus GTK3 1×/2× in both palettes. Existing regression tests remain enabled.

Diagnostics contain allocations, native computed borders/padding, minimum/natural
sizes, calendar cell/header dimensions, inline display/editing baselines, parent
row/tile sizes, splitter paint/hit widths, Expander header sizes, search hidden/
revealed measurements, Pango logical/ink extents and resolved fonts. GTK4 also
records serialized native render nodes and rendered glyph pixels; pixel upper/lower
bounds are compared with native ink positions using a 2px raster/hinting tolerance.
These checks supplement genuine window screenshots rather than treating Pango fit
alone as proof. CJK/Arabic retain native fallback; render nodes expose actual glyph
font runs. Font-bearing roles follow text DPI; enlarged inherited label content is
also stressed with native Pango scaling attributes.

See [native screenshots, geometry and test logs](../artifacts/phase2-controls/README.md).
Before/final screenshots show the same compiled native fixture against original
and final theme CSS. HTML disclosure and splitters illustrate appearance; browser
layout/interaction is not substituted for GTK validation.

## Build and known limits

```sh
python3 tools/extract-design-tokens.py --tokens-only
python3 tools/generate-theme.py
python3 tools/generate-theme.py --check
meson compile -C build
meson test -C build --print-errorlogs
python3 tools/capture-phase2.py
python3 tools/report-phase2.py
```

`--tokens-only` is an optional extraction mode added to preserve the local icon
artwork already present in this checkout. The default extractor's existing icon
regeneration behavior is unchanged. Full verification still checks icons and is
not relaxed: at baseline the four edited window-control SVGs differed from the
canonical HTML and had non-16px viewBoxes. The existing `design-tokens` and
`theme-tree` checks therefore report those pre-existing differences. Phase 2 does
not overwrite or silently approve that artwork. Source/token generation consistency
and Phase 2 tests are reported separately from those failures.

GTK4 4.18 exposes deprecated allocation/style getters used here for complete-box
measurements. They are diagnostic APIs, not replacements for native rendering.
The default renderer report records the actual implementation chosen by GTK;
GL under Xvfb is not proof of a hardware GPU or Wayland compositor result.
Headless native tests cannot establish screen-reader output, actual IME/preedit
behavior, real session preference forwarding, hardware/desktop GPU differences or
fractional compositor scaling. Those remain desktop checks. Normal native widget
roles, focus, key handling, context menus and text machinery are retained.
## Executed results

The final focused run passed **21/21** (one Phase 2 contract, 18 native profiles
and two CSS parsers). A further three representative native focus-diagnostic runs
passed. The complete regression suite passed **150/152**; its only failures were
`design-tokens` and `theme-tree` against the pre-existing local icon edits described
above. No tests were disabled or marked expected-failure. Existing toolbar, sidebar,
location, data-view, menu, segmented, switch and preference tests passed.
