# Reference analysis

Inspected all three supplied archives in Debian before implementation. The HTML is the visual authority; none of the reference CSS or artwork is copied.

* Material: separate `gtk-3.0` and `gtk-4.0` entrypoints import local `colors.css`. GTK3 uses legacy style properties and titlebutton selectors; GTK4 uses windowcontrols and popover contents. Its animations (scale, translate and rubberband), palette and rounded shapes conflict with Majoris and are excluded. Its separate GTK4 deployment illustrates why selecting a GTK theme alone cannot style libadwaita.
* Unity8 revamp: a Shell-only directory with CSS and symbolic assets. Panel, popup, calendar, overview and quick-setting classes are useful selector references. Its Ubuntu orange, black panel, Ubuntu font and branded assets are excluded. Version comments reference GNOME 46–48; these are hints, not proof of Trixie compatibility.
* Sunrise: a Shell-only generated stylesheet, assets, INSTALL, AUTHORS and LGPL-2.1 COPYING. It illustrates Shell popup/notification/workspace hierarchy and asset-relative paths. Some selectors are historical; validate against Trixie rather than assuming they survive. Its orange borders, dark surfaces and large radii are excluded.

The archives provide no Plus Jakarta Sans font and no authoritative dark Majoris palette. All implementation is original, with tokens and window glyph geometry derived from the user-supplied HTML. Reference licenses stay with the external archives; no fragments were reused.
