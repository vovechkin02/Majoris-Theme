# Majoris design authority

`reference/majoris-widget-factory.html` is preserved byte-for-byte. GTK runtime constraints are second in authority; external themes are selector references only.

Indigo #6366F1 is the selection accent. Suggested buttons use #4F46E5 as specified by the HTML. Compact controls have 4px corners; windows, cards, menus and dialogs have 8px corners. Button fades are stationary at 128ms; surface motion is 256ms. Semantic shadows are extracted verbatim. Window controls have 32px targets and exact 16px SVG geometry, on the right.

Regenerate tokens/icons with `python3 tools/extract-design-tokens.py`, then CSS with `python3 tools/generate-theme.py`. Edit templates, never generated CSS. Verification reports the specific HTML token or glyph that changed. Dark design is pending: gtk-dark.css imports the light design and makes no dark-mode conformance claim.
