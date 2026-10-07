# Fresh visual-conformance audit (before CSS changes)

The newly supplied HTML and repository reference are byte-identical (SHA256 `254f7cc14926302526517d9c312740873e4fbe40f2fab93c6541708777bbd3d5`). No replacement or modification is needed. Independently inspected the complete HTML styles/control markup, both GTK templates/generated themes, Shell CSS, all Vala pages/fixtures, SVGs, fontconfig, generation tools and tests. Runtime: Debian 13.5 Trixie, GTK3 3.24.49, GTK4 4.18.6, libadwaita 1.7.6.

This records the **initial** implementation, not final acceptance. PASS here means the specifically described existing check passed previously; remaining appearance is subject to the new rendered comparison. Later findings/results are recorded in the conformance report.

| Component | HTML requirement | Initial GTK3 | Initial GTK4 | Initial factory | Initial status |
|---|---|---|---|---|---|
| Authority/tokens | All palette plus component-specific sizes, colors, shadows | Generated root palette | Same | No complete component contract | PARTIAL: many inline values not extracted |
| Window controls | 32 target/16 glyph, 4 radius, 2 gap, no normal/hover/pressed shadow, dedicated focus | Normal shadow reset; state leakage possible | Generic hover/pressed shadows leak; generic focus outline | Simple+dense measured, no state lab | FAIL |
| Headerbar | 48 visual row, rgba white .92, normal back/forward; flat search/view/menu | Opaque white; all shadows removed | Opaque white; all shadows removed | All icons bordered; no split | FAIL |
| Ordinary buttons | 32 high, 12 horizontal padding, weight600, semantic shadows/focus | Padding10; incomplete primary/disabled focus variants | Same | Major types present | FAIL |
| Split button | 32 arrow/main, asymmetric joined radii | No specific split contract | Stock Adw.SplitButton | Present | PARTIAL |
| Sidebar | Width212, rows34, p50/p700, inset 2px stripe | Generic row padding8/12, no stripe | Same | StackSidebar lacks stripe, rows too tall | FAIL |
| Cards | Border-soft, radius8, card shadow | Present | Present | Native card boxes | PARTIAL: visual review outstanding |
| Boxed lists | Border-soft, radius8, no shadow | Card elevation incorrectly shared | Same | Boxed preferences nested in cards | FAIL |
| Preferences | Min50, padding8/12/8/16, title13/600, desc11.5/text2, separators | Generic rows only | Stock row internal minima/fonts remain | Most native rows; no button row | FAIL |
| Segmented | Border/surface2/radius6, padding2/gap2, height28 children, selected white shadow | Missing | Missing | Missing | FAIL |
| Tabs | Height36, text2, active text/650, inset10 underline2 | Full-width blue border, no size | Same | Notebook present | FAIL |
| View switch | Radius6 surface2/border/padding2, height28 children | Child radius only | Child radius only | Adw.ViewSwitcher with no container treatment | FAIL |
| Entry/search/password | Height32, padding10, min160, native focus | Basic input style | Basic input style; nested nodes unverified | Native controls present | PARTIAL |
| Dropdown | Height32, min150, padding12, gap18 | No dedicated minimum | No min150, inner row padding affects sizing | Narrow sample labels | FAIL |
| Spin/font/color | Height32, spin54 value/28 buttons, color tile16 | Generic styling | Generic styling | Native controls but stock chooser sample | PARTIAL |
| Switch | 40×22, track8, thumb16/4/border/shadow | Track minima approximated, thumb lacks border/shadow | Same | Only ON | FAIL |
| Checkbox/radio | 18×18, mixed/checked/dot, focus/disabled | Geometry present; baseline glyphs | Geometry present; baseline glyphs | Disabled missing | PARTIAL |
| Scale | Track #D8D9DF, height4, thumb16 | Uses border color | Same | Native 62% | FAIL: subtle color mismatch |
| Spinner | 20 diameter, p200 ring, p600 segment, 2 stroke | Unstyled | Unstyled | Active only | FAIL |
| Progress | Height8, #E7E8EC trough, p500 fill | Border-soft trough | Same | Native 68% | FAIL |
| Level | Eight segments/six filled, gap2, radius2, #E4E5E9 empty | Continuous style | Same | Continuous 0.7 | FAIL |
| Banner | p50/p200, padding12/14, radius8, gap12, 28 button | No equivalent global node | Color/radius only | Real Adw.Banner | PARTIAL |
| Toast | #222226, padding10/12, radius8, pop shadow, p300 action | No native equivalent | Text token used instead; spacing/action missing | Real toast without action | FAIL |
| Status | Tile48/8/p50/p600, title15, description12 | No native equivalent | Text only | Real StatusPage but stock tile | FAIL |
| Tooltip | #222226, white, radius4, padding6/8, font11, pop shadow | Wrong bg/padding, no shadow | Same | Real tooltip | FAIL |
| Popover/menu | Surface white .97, radius8, padding6, flat32 rows, text-danger trash | Opaque surface/basic menu rows | Opaque surface/basic model rows | Missing Open/Rename/Duplicate; trash red button | FAIL |
| Dialog | Radius8, strong dedicated shadow, body20, footer surface2/border/actions | Radius only | Radius only | Real alert, suggested instead of discard | FAIL |
| Dense data | p50 background/p800 selected text | Generic p700 | Same | List instead of true column presentation | FAIL |
| Scrollbars | Quiet overlay, thumb6/#B9BAC1/radius4 | Wrong color and baseline margins | Same | Real scroller | PARTIAL |
| Fontconfig | Strong sans-serif AND system-ui → Plus Jakarta Sans | Weak sans only | Same shared fontconfig | Required font absent | FAIL mapping; runtime font NOT TESTABLE until supplied |
| Motion | Stationary128 control/256 surface | Most transitions present | Most transitions present | No appearance provider | PARTIAL: inherited transitions need reset |
| Shell | Same semantics, proper palette/radii/shadows/font | N/A | N/A | N/A | NOT TESTABLE UNDER WSL visually; static selectors pass |

Additional discoveries beyond the feedback list: the token verifier ignores component CSS and pseudo-elements; generic row padding also affects dropdown menu rows; strong action shadows differ from generic control shadows; titlebar glyph state inherits normal focus borders; thumbnail/header display comparisons must distinguish actual border-box geometry from CSS content minima. Native font availability and browser font loading must be recorded rather than hidden by substituting fonts.
