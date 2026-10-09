# Surgical conformance completion — 2026-10-09

This targeted pass preserves both supplied HTML authorities byte-for-byte. It
resolves the concrete theme defects below; it does not certify the full GNOME
session or replace legitimate native widget structures.

1. **Exact files changed:** [surgical manifest](surgical-changed-files.txt).
   Source templates and generators own the generated CSS. No sibling app assets
   or source were modified. [Light scope proof](../artifacts/surgical-light-scope.json)
   verifies that every changed light declaration belongs to CSD/decoration edges
   or managed states.
2. **Debian:** 13.5 Trixie, WSL distribution `debian`. All builds, tests and native
   captures ran in Debian.
3. **GTK3:** 3.24.49.
4. **GTK4:** 4.18.6.
5. **libadwaita:** 1.7.6; Meson 1.7.0, Vala 0.56.18.
6. **Baseline:** 28/28 passed, no skips/failures. Geometry, both complete capture
   suites, versions and source snapshots are preserved under
   `artifacts/baseline-final-fixes/`, captured before any surgical edits.
7. **Final:** clean `meson setup --wipe build`, compilation and full suite:
   32/32 passed, no skips/failures/timeouts. Existing tests remain enabled.
   The earlier native dark-state test incorrectly mutated primitive palette
   expectations to action values; it now keeps primitives intact and separately
   checks semantic component colours. The negative p700 regression proves that
   correct action hover cannot conceal a corrupt primitive. New tests render all
   six checkbox states in both toolkits/schemes and verify genuine CSD classes,
   actual maximize/fullscreen, restore glyph geometry and native edge pixels.
8. **Canonical palette, both schemes:** p50 #EEF2FF, p100 #E0E7FF, p200 #C7D2FE,
   p300 #A5B4FC, p400 #818CF8, **p500 #6366F1, p600 #4F46E5, p700 #4338CA,
   p800 #3730A3**. GTK3/4 dark palette definitions occur once each and retain
   these identities.
9. **Dark semantic actions:** `action_primary` #6366F1,
   `action_primary_hover` #7377F3, `action_primary_pressed` #4F46E5,
   `focus_color` #818CF8; danger #DC3C4D / #E34B5B / #B92F3E.
   Primary buttons/banner/dialog responses inherit the semantic action states.
   Sidebar selected text #C7D2FE and table selected text #E0E7FF remain distinct;
   their background is rgba(99,102,241,.16). Dark spinner assets remain unchanged,
   with ring #34365D and arc #818CF8. Shell selection/accent retains #6366F1;
   its focus/danger consume independent semantic values.
10. **Dark mixed checkbox:** #4F46E5, not focus #818CF8. The exact p600 mark is
    present in actual native GTK3 and GTK4 output. Dedicated captures show
    unchecked, checked, inconsistent, disabled unchecked, disabled checked and
    focus in both variants. Dark unchecked surface/border remain #26262A/#4A4A50,
    checked surface #6366F1. [Native captures](../artifacts/checkbox-probes).
11. **GTK4 outer edge:** global `window.csd` owns the 1px border, 8px radius and
    unchanged authority window shadow. Light edge is rgba(20,20,25,.12), dark
    rgba(255,255,255,.07). The inherited Adw outline is suppressed to avoid a
    second edge. GTK3 decoration uses the corresponding exact reference edge.
    [Native pixel proof](../artifacts/window-edge-pixel-validation.json) verifies
    a single visible 1px edge; this is not merely a source-only result.
12. **Managed states:** maximized, fullscreen, tiled, tiled-left/right/top/bottom
    use supported GTK classes and reset radius/border allocation/shadow to zero.
    GTK3 decoration padding is also cleared. Native X11 maximized/fullscreen
    frames fill the 1440x1080 display with square corners and no edge inset.
    Directional tiling is explicitly a CSS diagnostic under Openbox, requiring
    actual Mutter tiling acceptance. [Managed-state geometry](../artifacts/window-edge-probes/geometry.json).
13. **Window-control focus:** documented HTML ambiguity is resolved in favour
    of its explicit state-verification example: transparent reserved 1px border
    plus external 2px halo, light rgba(99,102,241,.24), dark
    rgba(129,140,248,.36). Plates remain 32x32; no generic control shadow or
    coloured inner border is added. Default/hover/pressed/close/focus/backdrop
    source and native colour checks remain in place.
14. **Geometry:** all requested internal dimensions are preserved. With an
    actual composited CSD, normal simple/dense/content client widths decrease by
    the required 2px outer border reservation; the fixed 212px sidebar remains
    212px. Solid-CSD fallback geometry reports remain identical to baseline.
    [CSD baseline/final measurements](../artifacts/csd-baseline-final-geometry.json).

    | Allocation | Light | Dark |
    |---|---:|---:|
    | Simple header | 48px | 48px |
    | Dense header | 48px | 48px |
    | Split sidebar header | 48px | 48px |
    | Split content header | 48px | 48px |
    | Minimize / maximize / restore / close | 32x32 | 32x32 |
    | Every title glyph | 16x16 | 16x16 |

15. **Screenshot differences:** both full suites include overview, buttons,
    selection, all visual-state pages, simple/dense/split headers and eight new
    edge/state diagnostics. [Complete comparison](../artifacts/final-fixes-baseline-comparison.json)
    records raw full-frame differences: 4/27 original light images and 2/27 original
    dark images are pixel-identical, with eight new edge diagnostics per scheme.
    Expected changes are the outer GTK4 edge
    and its 1px interior-origin shift, dark mixed mark and removal of the dark
    titlebar inner focus border. GTK3 edge paints now use exact authority values.
    Light GTK3 and complete popup captures remain pixel-identical. Source-scope
    validation rejects unrelated light styling changes; broad visual review
    retains the established typography, palette, spacing and component hierarchy.
    Explicit family, sans-serif and system-ui all resolve to Plus Jakarta Sans.
16. **Symbolic audit:** read-only scan of 20 source SVGs finds six likely bugs:
    Calculator's symbolic app icon and Clock's symbolic app icon plus focus,
    stopwatch, timer and world resources contain #2e3436 paints. The report
    recommends `currentColor` and owning-app light/dark validation. Four theme
    window glyphs inherit currentColor; spinner fixed paints are intentional.
    [Classified findings](../artifacts/symbolic-icon-audit.md). Vendored references,
    build and staged copies are excluded; no automatic app rewrite occurred.
17. **Native toolkit constraints:** Adw preference-row internals;
    Adw.ViewSwitcher icon/content structure; popover arrow and accelerator layout;
    Adw.Banner positioning; Adw.Toast adaptive width and close control;
    Adw.AlertDialog response layout; native tooltip arrow differences; overlay
    scrollbar allocation; GTK3 solid-CSD fallback. Native widgets remain intact.
18. **GNOME/Mutter VM validation:** actual Wayland/Mutter floating shadows and
    transparent corners, inactive/restored/tiled windows, fractional scaling,
    Shell St rendering and User Themes switching, panel, Quick Settings,
    notifications/calendar, overview/search/dash, portals, Settings and GDM.
    Root XWD captures retain the baseline's black transparent-corner pixels and
    clipped exterior CSD shadows; those compositor effects are not certified by
    this WSL pass. There is no blanket fully-conformant claim.

[Issue-by-issue conformance report](../artifacts/visual-conformance-report.md)
records palette integrity, mixed checkboxes, outer edge, focus interpretation and
symbolic audit separately, with native and VM limitations preserved.
