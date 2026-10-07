# Testing

Tier 1 uses Debian WSL: `meson setup build`, `meson compile -C build`, `meson test -C build --print-errorlogs`. Tests cover HTML tokens/exact SVGs, selector rules, installation tree, reversible installer conflicts/restoration, native GTK3/GTK4 CSS parsers and realized headerbar geometry. Geometry uses temporary CSS/icon directories, Xvfb and D-Bus; JSON is saved to ignored `artifacts/geometry.json`.

Install with `scripts/install-dev.sh`, launch with `scripts/run-factory.sh`, inspect with `scripts/run-inspector.sh`. Use Tab for focus, hold the pointer for pressed, hover, expand rows, open menus/dialogs, trigger toasts, scroll, and maximize/restore both Headerbars fixtures. Interactive states remain manual checks.

Optional `scripts/capture-factory.sh` captures the X11 WSLg window into ignored artifacts/screenshots. Compare hierarchy/geometry, not pixel identity. Stock `gtk4-demo` is an integration check. Nautilus and Control Center require full session services.

Parser warnings fail tests. Literal backslash-n is rejected. Selector tests inspect rule heads rather than comments; native fixtures exercise real windowcontrols/buttons/images, entry, dropdown and menus. Broader state/appearance validation needs visual inspection.

Tier 2 is a Majoris VM/ISO for Shell, Mutter, GDM and desktop integration. Exact typography awaits Plus Jakarta Sans. The browser tool blocked the local HTML page, so side-by-side rendered comparison remains outstanding.
