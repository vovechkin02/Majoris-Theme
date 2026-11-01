# Layout spacing verification

GTK 4.18.6 / libadwaita 1.7.6 under WSL X11/Xvfb, cairo renderer.
12 light/dark profiles, 516 measured native gap assertions passed.
Profiles: standard (420px), narrow (320px), wide (760px), RTL, 200% scale, enlarged font.
Allocation tolerance: 1 logical pixel; all standard scale gaps were exact.

## Delivered

- Canonical spacing tokens, both HTML references, regenerated GTK3/4 light/dark CSS.
- Automatic PreferencesGroup arbitrary-content spacing; native Gtk.Dialog action areas and Gtk.ActionBar groups.
- Explicit semantic forms, search/results, action groups, footers, progress and connected containers.
- Native factory Layout & Spacing page with interactive allocation inspection.
- Native before/after screenshots, hidden/revealed editor states and measurement/hierarchy JSON.
- Files inventory and limitations in docs/layout-spacing-standard.md and docs/layout-spacing-files-inventory.md.

## Results

The first complete Meson run passed 158/165 checks. Two geometry failures were
fixed by lazily constructing the new factory page (14/14 targeted checks passed).
Both data-focus checks passed individually (1x and 2x). Native window edge states
passed after preserving the existing bridge priority. The final spacing run
passed 15/15 (12 native profiles, source contract and both GTK CSS parsers).
Generation --check passed. Compilation passed.

Two original source checks remain failing: theme-tree and design-tokens.
The checkout contains existing non-16px SVG viewBoxes and window glyphs that do
not match the HTML extractor. Window SVG files were unchanged by this task;
the initial working tree also contained user edits to three folder icons. Those
artworks were preserved. Token JSON itself matches both HTML extractions.
No existing tests were disabled, loosened or skipped.

Some intermediate logs include failed experimental FlowBox assertions or a
lower provider-priority experiment. Those experiments were corrected; the
final-spacing log and final geometry JSON describe the delivered implementation.

## Exact limitations

GtkBox property spacing adds to CSS border-spacing; margins add too. Native
internal PreferencesGroup boxes have zero property spacing and safely inherit
8px. Anonymous application boxes cannot be selected by their spacing property.
Generic popovers therefore retain application geometry and use an opt-in class
for Theme-owned composition. FlowBox CSS border-spacing is ineffective; its
native row/column properties remain necessary. GTK3 Box/Grid sibling gaps also
require native layout properties. No global widget mutation or Files change.

The bridge retains USER+1 priority to switch legacy installed themes correctly.
Intentional application CSS overrides use a provider at USER+2; tested without
!important. APPLICATION priority alone is insufficient with this integration.

## Screenshot provenance

All PNGs here are actual GTK X11 captures, not HTML. Files fixtures reproduce
the relevant native widget hierarchy, not a launched Files executable. Tags
before screenshots remove only the new content-container rule with a temporary
provider. Tags after and editor-visible screenshots inherit the Theme. Other
screenshots retain window context rather than being cropped into mockups.
Existing specialised regressions also have their native evidence in the other
artifacts directories (toolbar, sidebar, menus, tabs and data views).
