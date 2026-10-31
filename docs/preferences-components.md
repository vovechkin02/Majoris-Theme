# Majoris Preferences Components Design Specification

This specification is authoritative for native preferences components. GTK4 uses libadwaita 1.7 (Debian 13); no replacement widgets or application state logic are supplied by the theme.

## Geometry and typography

| Component/property | Contract |
|---|---|
| Single-line ActionRow | 48px target complete allocation |
| Title/subtitle ActionRow | 56px target, natural text sizing |
| Row insets | 8px vertical, 16px both horizontal sides |
| Title / subtitle | Plus Jakarta Sans, 14px/500 and 12px/400 |
| Text gap | 4px once, on native title box border-spacing |
| Symbolic prefix / gap | 16px intrinsic image, 8px to text |
| Text-to-suffix gap | 16px; suffix width remains natural |
| Buttons / switches | Existing 32px button and 40×22px switch contracts |
| Internal rows / separator | Square shared boundaries; 1px bottom separator, omitted on last row |
| Boxed group | Surface token, subtle 1px border, 8px radius, no shadow |
| Group heading | 14px/600, primary text, application-supplied case |
| Group description | 12px/400, secondary text, natural wrapping |
| Heading-to-description / header-to-list | 4px / 8px |
| Between groups | 16px, owned by PreferencesPage's box, or application box spacing |
| Hover/press/focus transitions | Stationary 128ms; no animated allocations or baselines |

On the supplied Plus Jakarta Sans at normal DPI, a separated single-line row measures 48px and a separated two-line row 55px. The latter is 18px title + 16px subtitle + 4px gap + 16px padding + 1px separator, within 1px of the 56px target. Last rows omit the separator (47px/54px). Rows with buttons can naturally need 49px including the separator. These small native differences are retained instead of forcing label heights or clipping glyphs. Larger text, multiline content, thumbnails and larger suffix controls grow naturally.

GTK font declarations use point equivalents derived from the 14px/12px tokens: 10.5pt/9pt at 96 DPI. This preserves the approved normal typography while following GtkSettings text DPI. Enlarged DPI tests verify actual text and row growth, rather than merely changing a setting while retaining fixed pixel sizes. No unrelated typography changes.

## Native hierarchy and scope

The measured Adw 1.7 hierarchy is `row > box.header > box.title > label.title / label.subtitle`; groups expose `preferencesgroup > box > box.header > box.labels > label.heading` and an optional description label. Rules select labels explicitly. Title containers no longer receive label minimum-height resets. Ordinary ActionRow header minimum content height is 31px; the row adds its own 16px vertical padding and separator. Native title-box margins are removed specifically to avoid duplicating those insets; text line measurements remain natural.

Boxed rows inherit the same point-based primary font, so specialised entry text also follows enlarged text DPI. EntryRow/PasswordEntryRow retain their editable-area layout and native floating title behaviour. SpinRow keeps its native numeric control; native 10px button margins are removed because the row now supplies the vertical inset. ExpanderRow applies insets to its header and nested rows once, keeping a continuous surface and native expansion. ButtonRow keeps native action and suggested/destructive semantics. It is available in the repository's required libadwaita 1.7; no version dependency was raised.

The first/last exterior row corners follow the 7px inner edge of the 8px group with its 1px border. All shared boundaries remain square. GTK snapshots showed that the list background clips itself, but does not clip child row backgrounds; these exterior-only corner rules prevent hover colour bleeding over the group corners, including expander headers and nested last rows.

Header suffixes use existing controls, an 8px gap from labels, and natural heading-area sizing. Only symbolic images use the 16px icon contract; arbitrary prefix widgets and thumbnails retain their requested dimensions. Logical direction selectors move prefix/suffix gaps to the correct side for RTL. Controls should set `valign = Gtk.Align.CENTER` as part of normal native composition; CSS does not override arbitrary widget alignment properties.

## Semantics and states

Native `.activatable` identifies actionable rows. Hover uses the existing hover token; press uses active; keyboard focus is a 2px inset Indigo outline. Passive boxed rows stay transparent on hover/press, so the group surface shows through. Independently interactive suffix controls retain their own feedback. Passive selectable rows do not acquire the custom whole-row action outline. Disabled controls keep native disabled behaviour and selection is not simulated in CSS.

The former global `row:hover` rule is narrowed to `row.activatable:hover`, with pressed feedback. Sidebar rules remain explicitly scoped in gtk-sidebar.css.in; data lists, grids and column views retain their explicit gtk4-data.css.in hover selectors. Menu/dropdown lists keep their own rules. The existing full regression suite checks these components.

A `majoris-preference-info` class can explicitly suppress whole-row hover/press appearance when an application's widget semantics need that presentation. This class does not disable activation. Applications remain responsible for native activatability; CSS cannot infer arbitrary behaviour. A suffix button alone does not make an ActionRow activatable. There is no need to opt in passive rows merely to obtain typography.

## Read-only properties

Use native `.property` when the property name is a secondary caption and the subtitle is the primary value. It remains a stacked native property presentation; the theme does not replace it with a custom two-column layout. Property names use 12px secondary text; values use 14px primary text, regular weight. Ordinary ActionRow subtitles stay 12px/400. Selectable values, wrapping, ellipsisation and accessible full text remain libadwaita responsibilities. Applications that need side-by-side short values can instead add a native label suffix; CSS does not move subtitle widgets.

```vala
var group = new Adw.PreferencesGroup();
group.title = "Information";
group.description = "Read-only file properties";
var row = new Adw.ActionRow();
row.title = "Size";
row.subtitle = "19 bytes";
row.subtitle_selectable = true;
row.add_css_class("property"); // Optional native name/value hierarchy.
group.add(row);

var copy = new Gtk.Button.from_icon_name("edit-copy-symbolic");
copy.valign = Gtk.Align.CENTER;
copy.clicked.connect(() => copy.get_clipboard().set_text(row.subtitle));
row.add_suffix(copy); // The row remains informational.
```

A separate actionable row uses native activation:

```vala
var action = new Adw.ActionRow();
action.title = "Default application";
var change = new Gtk.Button.with_label("Change…");
change.valign = Gtk.Align.CENTER;
change.clicked.connect(() => { /* Application opens its chooser. */ });
action.add_suffix(change);
action.activatable_widget = change;
group.add(action);
```

Use PreferencesPage to compose groups; do not add another 16px margin to each group. For custom page boxes, set one 16px spacing at the parent. Missing descriptions and empty/hidden groups do not reserve a phantom header. Headings align with the outer group edge, not the 16px inset row title.

## Palettes and GTK3

All surfaces, borders, text, hover and active colours reuse Majoris tokens. Focus is #6366F1 in light and #818CF8 in dark. Both variants share geometry. Switches keep the previously finalised 4px track/thumb rules and disabled filter correction; embedded controls do not receive a new control design.

GTK3 has no libadwaita components. Shared boxed Gtk.ListBox rows receive equivalent 8px group corners, square internal rows, separators, insets and semantic activatable hover. GTK3 applications can use label.title and label.subtitle for equivalent typography and must provide their native text/control layout themselves. This is not a GTK3 preferences framework.

## Fixtures, validation and renderer investigation

Open the factory's Preferences Components page or run `./scripts/run-factory.sh --page=preference-components --light` / `--dark`. The lazy-built native page covers Files Properties, Copy, Open With, Organisation, every supported subclass, prefix/suffix controls, semantic states, descriptions, header suffixes, long/selectable values, multiline text and RTL.

`tests/test-preferences-native.py` measures real allocations, Pango logical/ink bounds, resolved font face/size/weight, label baseline and layout baseline, padding/margins, parent bounds, prefix/suffix gaps, heading alignment and actual PreferencesPage spacing. It tests native keyboard activation, independent Copy pointer input, SwitchRow, entry/password editing, numeric/selection properties, expansion and ButtonRow activation. Native render nodes validate group radius and focus. Normal and enlarged text, narrow widths, light/dark, scales 1/2, Cairo/GL/default renderer cases are registered in Meson.

Each test writes unedited full-window PNGs, native `.node` snapshots and JSON under `artifacts/actionrow-finalisation/<variant>/<renderer>-<scale>x[-large-font]/`. `before.png` reconstructs only the previous row insets/minimums/text gap through a temporary native provider; `after.png` removes it. This comparison is not a full historical theme reconstruction. The initial complete native hierarchy is also retained in the investigation artifacts.

The original native title box contributed 3px spacing in addition to the old 2px subtitle margin, giving a measured 5px text gap. The final title-box spacing is 4px with no extra subtitle margin.

The label-reset investigation reintroduces `min-height:0`, `padding:0` and `margin:0` independently and records the resulting native text metrics. Removing these broad resets is a scope/layout correction, not proof that they caused the reported glyph corruption. Reviewed Cairo and GL screenshots show complete sample glyphs in this WSL/Xvfb environment, with logical and ink bounds fitting their labels. Default renderer results identify the actual renderer. The WSL/Xvfb renderer does not reproduce the user's physical desktop GPU environment; GNOME/Wayland, the affected application, real graphics drivers and fractional scaling still require desktop reproduction. Do not mark the recurring desktop defect fixed from Pango bounds alone.

Regenerate with extract-design-tokens.py, generate-theme.py and verify-design-tokens.py. `generate-theme.py --check` must pass. Build and run `meson test -C build --print-errorlogs`; focused cases are `native preferences*` and `preferences component source contract`.

Generate the aggregate JSON and Cairo/GL metric/pixel comparison with `python3 tools/report-preferences.py` after native tests. This reads captures without modifying them.

A label allocation baseline of -1 in reports means GTK did not negotiate a shared baseline for that vertical box. Its Pango layout baseline and ink/logical positions are recorded independently; no hardcoded baseline is introduced. Ancestor content bounds/overflow policies and full render nodes provide clipping context.

Suggested ButtonRows retain an Indigo fill and white foreground through hover/press using the existing Majoris action tokens; destructive ButtonRows retain the danger text treatment. Neutral row hover does not replace those explicit actions.

## Validation result

The complete regression run passed 133/133 tests. After final exterior-corner, inherited-font and RTL refinements, all 33 affected-component checks passed. The subsequent ButtonRow treatment pass passed all 16 source/parser/factory/native checks; the final evidence run passed all 12 native preference cases with ancestor clipping metrics. Token verification, generator --check, native factory compilation and git diff --check pass. Existing tests were retained.

Normal measurements are 48px single-line and 55px two-line with a separator; enlarged 144-DPI text produces a 71px two-line row. The available default renderer is GLRenderer; explicit CairoRenderer and GLRenderer have identical measured text metrics. Reviewed captures do not reproduce the reported missing upper glyph pixels. Physical GNOME/Wayland/driver reproduction remains outstanding, as distinct from the confirmed theme geometry and scope fixes.
