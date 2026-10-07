# Implementation report — feedback pass, 7 October 2026

The feedback implementation and available Debian validation are complete. The original HTML remains byte-preserved. Component appearance was reviewed through actual native captures and an unchanged Chromium reference, alongside native geometry/color checks and parsed CSS contracts. Final design acceptance remains **PARTIAL** for exact typography and the toolkit/environment boundaries listed below; passing token tests alone is not treated as visual acceptance.

## 1. Exact files changed

[changed-files.txt](changed-files.txt) is the exact tracked/untracked source manifest for this pass. Ignored generated evidence lives in `artifacts/`. Changes include component extraction/generation, GTK3/GTK4/Shell templates and generated CSS, exact spinner vectors, native gallery/state/header fixtures, semantic/native tests, strong font aliases, reversible asset installation, capture/reference/report tools, dependency bootstrap and documentation. Window SVGs and the reference HTML are unchanged.

## 2. Runtime tested

Debian GNU/Linux **13.5 Trixie**, existing WSL distribution `debian`; GTK3 **3.24.49**, GTK4 **4.18.6**, libadwaita **1.7.6**, Vala **0.56.18**, Meson **1.7.0**, Ninja **1.12.1**. Shell static reference: gnome-shell-common **48.7-0+deb13u2**. Chromium **154.0.8037.92** renders the reference. Native captures use Xvfb X11, Openbox, xcompmgr, Cairo and scale1. No distribution upgrade or replacement was performed.

## 3. Discrepancies found

The [fresh audit](visual-conformance-audit.md) records the initial state before these edits. Major failures were generic shadows/focus leaking into titlebar controls, 49px headers against the HTML's 48px border-box, card elevation on boxed lists, missing sidebar/segmented/tab/view-switch treatments, incomplete component-specific token extraction, narrow dropdowns, approximate switches, continuous level bars, incorrect tooltip/toast surfaces, incomplete menu/dialog/status samples and weak/missing font aliases. The factory and existing tests covered too little native state behavior to certify the appearance.

## 4. Discrepancies fixed

- Extract every CSS declaration, grouped rule, pseudo-element and inline style. Generate from component rules, preserving subtle track/trough/tooltip/scrollbar colors and shadow families; detect generated CSS/SVG drift.
- Explicit titlebar default/hover/pressed/focus/backdrop and close states. Remove generic shadows, outlines and libadwaita image-circle backgrounds; retain the specified 4px plate radius and exact glyphs.
- Normalize header border-box sizing to48. Back/Forward are normal bordered controls; Search/View/Menu are flat. Add a real split fixture with two aligned48px headers and square internal joins.
- Implement sidebar p50/p700 selection and inset stripe; distinguish p800 dense-data selection. Unelevated boxed lists, reference card-header/body hierarchy, preference minimum/padding/type/separators and subtitle opacity resets.
- Native segmented controls, 36px tabs with an inset underline, label-only StackSwitcher and real Adw.ViewSwitcher coverage. GTK3 translates unsupported weight650 to600 and replaces the stock orientation-specific underline.
- Entries/choosers/dropdowns/switch/selection-control geometry and states; remove GTK3 gradient overlays and double combobox borders. Theme exact progress/scale colors, discrete eight-block level and native vector spinner.
- Correct real banner, toast, tooltip, popover/menu, status and alert-dialog nodes. Native text-danger Trash rows stay flat. Dialog body/footer/shadow and primary banner action follow the reference.
- Replace fake spaced data text with a real Gtk.ColumnView/SingleSelection using the exact Documents/Majoris Design.md/Wallpaper.png sample and 1.4:.8:.8 columns.
- Strong sans-serif **and system-ui** aliases. Reversible asset/font installation can extend an existing journal without changing its earlier backups.
- Native state laboratory, both-toolkit scrolling, actual pointer-triggered tooltip, full-display captures plus complete popup surfaces, unchanged reference rendering, reviewed component report and stock gtk4-demo integration capture. No appearance CssProvider exists in the Vala factory.

## 5. Newly discovered differences

Actual inspection found inherited libadwaita control-image circles, GTK3 blue gradient masks despite correct computed backgrounds, white native tooltip children, compounded disabled-indicator opacity, dimmed preference subtitles, missing switcher page icons, wrong real dialog/banner CSS nodes and an initially stretched spinner. These were corrected rather than hidden in screenshots.

The HTML has a focus ambiguity: the grouped live `:focus-visible` rule sets a p500 border, while the dedicated `.window-control.is-focus` illustration explicitly overrides its border to transparent. Native titlebar focus follows the dedicated ring-only illustration with a transparent border; both rules remain extracted and the choice is tested/documented. The reference was not edited to erase the ambiguity.

Chromium returned blank scrolled reference frames. They were rejected. The final renderer captures the unchanged source at1440x1080 and1440x4000, showing the entire reference without crops or wrapper styling. Root xwd captures omitted native override-redirect surfaces; separate uncropped popup/tooltip-window captures retain the full native surfaces instead of compositing them into a fabricated desktop image.

## 6. Geometry results

| Native fixture | Content | Padding total | Divider | Allocated / painted height |
|---|---:|---:|---:|---:|
| Simple / Clock-style |32|15|1|48|
| Dense / Files-style |32|15|1|48|
| Split sidebar header |32|15|1|48|
| Split content header |32|15|1|48|

The divider is included in48, consistent with HTML border-box sizing. Geometry checks derive expectations from HTML tokens rather than repeating a hand-written49 target. Normal and flat header icon plates are32x32, entry/dropdown height32, dropdown minimum150, switch40x22, StackSwitcher button28 and notebook tab-label allocation36. Sidebar row allocation36 comprises the painted34px target and2px gap. Actual JSON and the generated report expose toolkit nodes; unavailable notebook CSS nodes are reported honestly rather than converted into fake widget allocations.

## 7. Window-control results

Simple and dense fixtures both realize minimize/maximize/close plates at **32x32** and image allocations at **16x16**. Plate radius is **4px**. Hover uses neutral hover/text; pressed uses active/text; close uses danger/white then danger-press/white. Backdrop uses tertiary glyph contrast. Normal/hover/pressed/backdrop have no generic shadows. Focus is the dedicated2px indigo halo with transparent border and no control drop shadow. Source contracts check shadow/border/image resets; GTK3/GTK4 actual foregrounds and GTK3 actual backgrounds pass; native state images support the visual conclusion.

## 8. Generated screenshots

[Generated component report](../artifacts/visual-conformance-report.md) links every section to the full HTML reference and native evidence, with PASS/PARTIAL and a reason. The suite includes overview/scrolled, buttons, selection, inputs, ranges, preferences, navigation/data, menus, real tooltip, banner/toast, dialog/status, simple/dense/split and five state-lab groups. Additional complete menu/tooltip surfaces, GTK3 native/scrolled fixtures and stock gtk4-demo are captured. JSON records viewport, scale, font, renderer, theme and actual pages. Evidence is ignored generated output, while reviewed observations and scripts are committed source.

## 9. Automated coverage added

Parsed semantic shadow, radius, color, selector/state/motion contracts; complete component extraction and CSS/SVG generation drift; native factory coverage; strong fontconfig aliases and separately skipped exact-font resolution; both native CSS parsers and titlebar colors; actual GTK3 painted normal/primary backgrounds; realized header/control/dropdown/switch/tab/sidebar geometry; reversible installer asset migration/conflict/restore; spinner-vector size/stroke and installation-tree checks. Parsed contracts explicitly state that they are source checks, not computed GTK style introspection.

## 10. Full Meson result

**18 tests: 17 passed, 0 failed, 1 skipped, 0 timeouts.** The skipped test is exact Plus Jakarta Sans runtime resolution (exit77), because the font is absent. Both GTK parsers and all light/dark-entrypoint/palette checks pass. Compiler deprecations exercise native ColorButton/FontButton and allocation APIs; generated Vala C warnings remain. Some GTK3 state-probe runs emit a Pixman invalid-rectangle diagnostic; logs are retained and the actual painted color assertions pass. Factory capture logs are inspected for theme parser errors; these diagnostics are not represented as pixel-level proof.

## 11. Native applications tested

Built and ran Majoris Theme Factory in native Debian GTK4/libadwaita, all three stress fixtures, real native GTK3 controls and scrollers, and stock **gtk4-demo** with user theme overrides. gtk4-demo's optional source-highlighting warning is retained. Nautilus, GNOME Control Center and Majoris Clock are not installed in this environment; full application/session integration remains a target VM check.

## 12. Remaining limitations and reasons

- **Typography:** Plus Jakarta Sans was neither supplied nor installed. Strong aliases are fixed, but fallback glyph metrics/line wrapping cannot certify the intended font. The runtime test correctly skips rather than using a renamed substitute.
- **Native preferences/choosers:** libadwaita EntryRow/PasswordEntryRow/SpinRow and GTK font/color controls own their edit/preview layouts. Their public APIs and theme nodes do not turn them into the HTML's simplified suffix inputs/swatches. Natural text and expanded rows can exceed a50px minimum.
- **Adw.ViewSwitcher:** its real native content includes page icons; the reference's iconless example uses native Gtk.StackSwitcher in the gallery. Both are themed and demonstrated rather than replacing Adw widgets with HTML-like pictures.
- **Banner:** Adw.Banner centers its title and does not expose the reference's leading information-glyph layout via theme CSS. Surface/action treatment is inspected.
- **Toast:** libadwaita retains a close control and wider native minimum/layout. GTK CSS does not implement `max-width:360px`, so exact browser width is not achievable by the standalone theme alone.
- **Dialog/menu:** Adw.AlertDialog owns equal-width response layout instead of HTML's compact right-aligned buttons; native popovers retain an arrow/accelerators absent from the browser illustration. Their surface/state treatment is verified.
- **GTK3:** weight650 is unsupported and translates to600. Native notebook/chooser/header APIs differ, and GTK4 computed shadow/radius APIs are not exposed; source checks plus real images supplement native color/geometry evidence without pretending the unavailable values were introspected.
- **Desktop/compositor:** WSL Xvfb/Openbox is not Majoris GNOME Shell/Mutter. Shell runtime states, desktop application overrides, fractional scaling and compositor-owned shadows/corners cannot be certified here. Static Shell grammar/selectors do pass.

## 13. Final Majoris VM validation

Supply/install Plus Jakarta Sans and require both fc-match mappings and the font runtime test to pass. Run the same gallery, state-lab, parser/geometry and capture workflows under the target GNOME/Mutter session at100% and fractional scaling. Inspect real pointer/keyboard focus/press/backdrop, maximize/restore glyphs, inner split joins, shadow clipping and overlay scrollbars. Exercise Majoris Clock, Files/Nautilus, Control Center, real document/data views, dialogs and toasts. Inspect Shell panel/menus/quick settings/calendar/notifications/overview and its native focus/selected states. These are explicit final acceptance items, not checks claimed to have run in WSL.

Reference SHA256 remains `254F7CC14926302526517D9C312740873E4FBE40F2FAB93C6541708777BBD3D5`, identical to the supplied file.
