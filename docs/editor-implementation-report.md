# Editor implementation report — 17 October 2026

Implemented the three reusable GTK4 classes, independently generated light/dark
SourceView schemes, safe development/system packaging, native Vala composite
fixture, automated tests and integration documentation. The original approved
HTML, primitive palette, window-control SVGs, Notebook rules and application
repositories are unchanged.

`majoris-document-tabs` uses inspected Trixie libadwaita 1.7 nodes and native
selected/attention states. It provides flat 38px tabs, a 2px selection underline,
neutral hover/press, focus and backdrop, 22px close controls and native overflow.
`majoris-editor-toolbar` provides a 40px strip with 28px actions;
`majoris-statusbar` provides a 34px secondary strip with 28px native selectors.
Theme ownership is confined to opt-in components and their direct/grouped
controls, excluding popover contents. Native layout owns action/group spacing.

Source schemes `majoris-light` and `majoris-dark` cover editor surfaces, caret,
selection/unfocused selection, current line, gutter/numbers, margin, brackets,
search, whitespace and common source/markup/diff/error/warning roles. The
independent syntax palettes are owned by XML templates; approved UI primitives
are unchanged. Comments intentionally use secondary text for readable contrast.
Both schemes are discoverable simultaneously from standard user/system paths.
Applications explicitly choose the matching scheme; third-party selection is
preserved unless application code opts into automatic Majoris colours.

The native fixture includes plain text, Markdown, Vala, Python, a long filename,
a pinned page and an attention/unsaved page, plus a larger overflow fixture.
It supports native closing/reordering and shared appearance controls. Formatting
toggles, separators, tooltips and status MenuButtons use GTK widgets; it is an
integration fixture rather than a Notepad implementation. SourceView presents
syntax, line numbers, search matches and selection. Existing factory categories
and diagnostics remain present.

## Validated results

Debian 13 Trixie, GTK 4.18.6, libadwaita 1.7.6, GtkSourceView 5.16.0:

- Meson configuration/build succeeded using already-installed dependencies.
- All 45 registered tests passed, with zero failures/skips and exact Plus Jakarta Sans.
- Generation and `--check` passed; all GTK3/GTK4 light/dark outputs are synchronized.
- Both SourceView XMLs passed the installed Relax NG schema and real runtime discovery.
- Explicit, repeat and auto development installs preserve original schemes,
  reject edited installation files and restore previous data on uninstall.
- Actual staged `/usr` installation includes the factory, launcher, generated
  CSS, both system-discoverable schemes and maintainable source templates.
- Real default-font allocations are 38px / 40px / 34px bars, with 28px controls,
  at 100% and 200%. State changes leave those allocations unchanged.
- Native page switching, pinning, reordering, closing and narrow overflow passed.
- Light → dark → light and third-party scheme ownership passed. The actual
  Vala factory app.scheme action also updated all five source buffers in both
  scaling runs (`editor-factory-switching.json` and `editor-factory-switching-2x.json`). Existing native
  headerbar/window glyph, Notebook, button, GTK parser, palette and bridge tests passed.
- Light, dark and system editor launch workflows completed with diagnostic exit.

## Visual comparison and deliberate differences

The supplemental document-tabs section shows a flat surface, emphasized active
label and narrow bottom indigo indicator. Native normal/focus/state/overflow
captures reproduce that direction without raised selected tabs or hover movement.
Native tab width negotiation and icon-only pinned tabs replace HTML flex/max-width
logic; the theme does not impose a CSS maximum that would break native overflow.
Close glyphs use installed symbolic artwork and native reserved allocation,
with neutral close hover rather than the window-close destructive treatment.
Native attention is represented by TabPage indicators, not a fabricated dirty state.

The editor/statusbar section specifies subordinate flat actions and a quiet
secondary status strip. Native composite captures show integrated surfaces,
single dividers and no independent control shadows. Default geometry matches
its 38/40/34/28px contract. Narrow overflow fixtures hide lower-priority status
selectors and horizontally scroll toolbar actions. All labels/icons remain native.

The syntax section's proposed light/dark colours informed the two XML schemes.
Native SourceView shows the approved white / #202023 editor surfaces, subtle
current-line and gutter regions, visible selection/search, and independently
tuned readable syntax. Comment colours are stronger than the proposed faint
swatches to meet the 4.5:1 contrast contract. Editor content is explicitly
monospace while application chrome remains Plus Jakarta Sans.

Two necessary corrections to existing global rules are included: selection
styling is scoped to ordinary text controls/non-source TextViews so SourceView
schemes own source selection; GTK4 TextView's explicit monospace opt-in now
wins over the universal UI family. Ordinary entries and other controls preserve
their existing selection colours. The capture runner now exposes the installed
icon overlay/fallbacks in an isolated data directory; earlier missing formatting
icons were an environment defect, not a redesigned icon set.

Native detached tab drag previews have no TabBar ancestor. Their existing
libadwaita preview styling is deliberately retained instead of adding a global
`dnd tab` selector. Close-button keyboard behavior remains libadwaita-owned.
Large accessibility fonts may increase native minima rather than clip controls.
The on-disk Trixie XML schema excludes newer metadata/underline-colour extensions,
so the schemes use its supported structure and error/warning underlines.

References and native screenshots are directly captured; no screenshot is
cropped, recoloured, composited or resized for acceptance. Supplemental reference
copies isolate review sections and load local fonts; their original target CSS
and markup are unchanged. Both source/font hashes are recorded. Full frames and
logs are in `artifacts/screenshots/editor-html`, `light`, `dark`, `light-2x` and
`dark-2x`. Existing control capture workflows run alongside the editor pages.
Git-baseline CSS was reconstructed in ignored evidence and the same existing
button, Notebook/navigation and simple-headerbar fixtures were captured with
identical fonts/icons. All three light-mode full-frame comparisons contain
**zero changed pixels** (`artifacts/editor-baseline-comparison.json`). This is
direct evidence for those fixtures, not a claim of exhaustive pixel equality
across every component. No baseline is overwritten to grant acceptance automatically.

## Outstanding environment-dependent checks

A real Majoris GNOME/Mutter session is still required for pointer drag/drop and
cross-window transfer, keyboard/screen-reader interaction, real activation and
backdrop, Wayland/fractional scaling, enlarged accessibility fonts and real
portal/system-following transitions. The implemented GTK4 bridge architecture
is preserved; no global dispatcher or unrelated application attachment was added.

Use [the integration guide](editor-components.md) for Notepad adoption. No
Notepad application code was changed. Source changes are ready for that separate
application integration, subject to the documented session acceptance checks.
