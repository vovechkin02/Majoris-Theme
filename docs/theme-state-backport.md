# Theme-state backport completion — 2026-10-11

The theme-owned ISO fixes now originate in the theme repository. The builder can
copy `theme/Majoris/` verbatim and retain only its session activation machinery.
No palette, typography, application geometry or native bridge implementation was
changed. Full GNOME/DING/St lifecycle acceptance remains a VM check.

1. **Exact files changed:** [complete manifest](theme-state-backport-files.txt).
   Baseline sources, 32/32 tests, screenshots and geometry are preserved under
   `artifacts/pre-theme-state-backport/`. No user appearance preference was changed.
2. **Authoritative sources:** `design/templates/gtk-common.css.in` owns the six
   desktop selectors; the generators emit this block last. `shell.css.in` owns
   explicit panel/container/child/state selectors. `generate-theme.py` and
   `generate_dark.py` map semantic panel, popup, search, control, disabled,
   selected, focus and tooltip values. Generated output passes `--check`.
3. **Generated outputs:** four GTK light/dark entrypoints and the light/dark
   Shell files, plus the conventional `Majoris-Dark` Shell alias. No manual-only
   output patch remains. Ordinary GTK declarations and assets retain their
   existing values; only the desktop compatibility block is added to GTK CSS.
4. **DING compatibility:** `window.desktopwindow`, its backdrop/background
   combinations and `.desktopwindow` normal/backdrop have transparent background
   and border, no background image, zero border width/radius and no shadow.
   Emitting this shared block after native/dark overrides avoids equal-specificity
   CSD rules repainting the desktop. DING source/packages were not modified.
5. **GTK3 desktop result:** light/dark normal and backdrop source contracts pass.
   A real GtkWindow context renders background/frame with zero alpha in both
   states; the ordinary window remains opaque before/after the class is removed.
6. **GTK4 desktop result:** the same four native state/variant probes pass with
   the existing GTK4 parser. These are native style-render tests, not a claim
   about live DING wallpaper, icon or compositor behaviour.
7. **Light Shell:** white panel/transient surfaces and #1C1C1F foregrounds are
   explicitly assigned to panel clock/status labels/icons, popup/menu, Quick
   Settings, system/power, calendar, message, notification and dialog descendants.
   Search remains white; no permanent-dark workaround was introduced.
8. **Dark Shell:** panel #202023, transients rgba(40,40,44,.98), search #28282C,
   text #F4F4F5 and search border/focus #3B3B40/#818CF8. Explicit semantic values
   replace a broad `color:` substitution that inadvertently also matched
   `background-color:` and turned dark surfaces white. Tooltip inversion remains
   intentional. Legitimate #FFFFFF selected foregrounds remain allowed.
9. **Quick Settings:** icon buttons keep 4px radius and use light default/hover/
   active #F2F2F4/#ECECEF/#E2E2E6, dark #28282C/#303035/#38383D. Insensitive
   controls and their children use #8A8A92 light / #7F7F88 dark. Checked menu,
   toggle and menu-toggle backgrounds use #6366F1; wildcard, StLabel, StIcon and
   named label/icon/arrow children explicitly become #FFFFFF. Both independent
   stylesheets pass Light → Dark → Light and Dark → Light → Dark source contracts.
10. **Development auto before/after:** auto previously linked GTK4 user gtk.css
    to fixed light CSS. It now links `integration/gtk4-auto.css`, a neutral
    comment-only file with no imports/declarations. Explicit light/dark still
    link their fixed entrypoints. The existing journal backs up files/symlinks,
    retains originals across mode changes, rejects later edits and restores on
    uninstall. Tests cover repeat install, migration, all modes, original files
    and symlinks. A real neutral install also passes both live bridge cycles.
11. **GTK3 bridge:** unchanged. It follows GNOME colour-scheme through native
    gtk-application-prefer-dark-theme with the named Majoris theme. Its existing
    variant selection tests remain enabled.
12. **GTK4 bridge:** unchanged. It watches Adw.StyleManager::dark and loads the
    active entrypoint at user priority + 1. The factory links it; other processes
    require the existing wrapper or distro-owned attachment. Neutral auto mode
    alone does not globally inject a library into arbitrary processes.
13. **Distro ownership:** no session dispatcher, dlopen interposer, global
    LD_PRELOAD, `/etc/environment` edit, desktop extension, ISO hook, DING package
    configuration or wallpaper hook was copied here. Majoris OS/session owns
    global bridge attachment, Shell extension activation/switching, wallpaper
    and the full GNOME/Mutter lifecycle. Theme ownership remains assets, two
    reusable bridges, development helpers and variant tests.
14. **Light geometry:** simple, dense, split sidebar and split content headers
    remain 48px; title plates 32x32 and glyphs 16x16, including restore. The whole
    realized geometry report must equal the saved baseline; regular application
    CSS is checked independently against the baseline, excluding only DING.
15. **Dark geometry:** the same dimensions and complete baseline equality.
    Light/dark widget trees remain identical. Both final 35-frame native suites
    are pixel-identical uncropped against their saved counterparts (70/70).
    Exact Plus Jakarta Sans validation remains enabled.
16. **Tests:** Debian 13.5 Trixie, GTK3 3.24.49, GTK4 4.18.6, libadwaita 1.7.6.
    Baseline 32/32; final clean Meson suite **37/37**, zero failures/skips/timeouts.
    Existing tests were preserved. New tests cover parsed DING contracts, native
    GTK3/GTK4 transparency, exact Shell properties/descendants and source cycles,
    plus a neutral auto install with native GTK4 bridge cycles. Installer tests
    were strengthened rather than disabled. See the generated evidence report
    for the final screenshot comparison and generation checks.
17. **Remaining VM-only checks:** [exact checklist](theme-state-vm-checklist.md)
    covers four desktop focus/scheme combinations with wallpaper and Home/Trash
    visible; readable panel/clock/tray/Quick Settings, disabled and checked
    controls; both switching sequences without logout and no stale foreground,
    popup or disabled colours. Actual DING/St rendering, installed-session
    dispatch, late-loading GJS/GI processes, Shell extension activation,
    Wayland/Mutter shadows/corners/tiling, scaling, portals, Settings and GDM
    remain GNOME VM acceptance. Native toolkit constraints from prior passes
    remain documented and their widgets were not replaced.

[Generated evidence report](../artifacts/theme-state-backport-report.md) ·
[Full-frame and geometry comparison](../artifacts/theme-state-backport-comparison.json) ·
[Native desktop paint evidence](../artifacts/desktop-window-probes) ·
[Neutral auto bridge evidence](../artifacts/auto-install-bridge.json)
