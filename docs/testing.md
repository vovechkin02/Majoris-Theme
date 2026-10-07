# Testing

Run `meson setup build`, `meson compile -C build`, then `meson test -C build --print-errorlogs` in Debian Trixie. The Windows helper is `scripts/wsl.ps1 test`. The 18 tests include full HTML declaration/pseudo-element extraction and generated CSS/SVG drift; parsed semantic shadow/radius/color/state contracts; strong font aliases; reversible installer restoration, conflicts and asset migration; native GTK3/GTK4 parsers and titlebar colors; GTK3 painted button backgrounds; and native simple/dense/split geometry. Source contracts explicitly do not claim computed GTK appearance.

Generate after template changes with `python3 tools/generate-theme.py`, preserving the reference. Synchronize generated CSS and assets back to the Windows checkout before using its helper again. Capture refuses generated-theme drift rather than silently inspecting an older stylesheet.

```bash
./scripts/install-dev.sh
./scripts/render-html-reference.sh
./scripts/capture-visual-regressions.sh
python3 tools/report-visual-conformance.py
```

The renderer needs Chromium and Pillow. Native capture needs Xvfb, D-Bus, xwd/xwininfo, ImageMagick, Openbox, xcompmgr, xdotool and gtk4-demo; GTK3 painted probes need python3-cairo and python3-gi-cairo. Bootstrap includes these Trixie packages. Captures use scale 1, a 1440x1080 display, 1280x960 gallery windows, Cairo and disabled animations. Header stress fixtures use their intentionally smaller widths. Font resolution and all capture conditions are recorded in JSON.

The reference is captured unchanged at 1440x1080 and 1440x4000, without crops or replacement CSS. Blank frames are rejected. Full-page rendering avoids a Chromium headless scrolling failure observed on this runtime. Remote font hosts are disabled to compare the installed fallback consistently. Plus Jakarta Sans runtime verification exits 77 if absent; this is never reported as a pass.

The Visual States laboratory holds real GTK flags, clearly labeled as diagnostics. It includes default/hover/pressed/focus/disabled/selected/backdrop for buttons, titlebar controls, inputs, selection controls and navigation. Pointer/Tab interaction remains available. Tooltip capture actually moves the pointer over Back. Popup captures preserve the full popup surface separately because xwd root capture omitted override-redirect surfaces on this setup; full-display captures are retained too.

`artifacts/geometry.json`, screenshots, logs and the generated conformance report are ignored build evidence. Reviewed observations live in `docs/visual-review.json`; regenerating the report does not automatically grant visual acceptance. Inspect changed captures and update the review record deliberately.

Final Majoris VM checks remain necessary for Mutter/Shell, fractional scaling, maximized/restore behavior, keyboard/input behavior and desktop applications. Installed GTK3 native fixtures and stock gtk4-demo provide local integration evidence. Nautilus and Control Center are absent from this Debian environment. Exact typography awaits the specified font.
