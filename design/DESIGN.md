# Majoris design authority

`reference/majoris-widget-factory.html` is preserved byte-for-byte. GTK runtime constraints are second in authority; external themes are selector references only.

Indigo #6366F1 is the selection accent. Suggested buttons use #4F46E5 as specified by the HTML. Compact controls have 4px corners; windows, cards, menus and dialogs have 8px corners. Button fades are stationary at 128ms; surface motion is 256ms. Semantic shadows are extracted verbatim. Window controls have 32px targets and exact 16px SVG geometry, on the right.

Regenerate tokens/icons with `python3 tools/extract-design-tokens.py`, then CSS with `python3 tools/generate-theme.py`. Edit templates, never generated CSS. Verification reports the specific HTML token or glyph that changed. Dark generation uses the effective dark HTML cascade and independent native overrides; see the token layers below.

## Primitive, semantic and surface layers

Both unchanged HTML authorities are extracted in source order. The primitive
indigo scale is invariant between light and dark: p50 #EEF2FF, p100 #E0E7FF,
p200 #C7D2FE, p300 #A5B4FC, p400 #818CF8, p500 #6366F1, p600 #4F46E5,
p700 #4338CA and p800 #3730A3. No dark component may redefine a palette index.

Dark semantic tokens are action_primary #6366F1, action_primary_hover #7377F3,
action_primary_pressed #4F46E5, focus_color #818CF8, action_danger #DC3C4D,
action_danger_hover #E34B5B and action_danger_pressed #B92F3E. These are
independent identities, including focus versus p400. Mixed checkbox marks use
the canonical p600 in both schemes; they do not consume the focus token.

Background, surface, surface-secondary, hover, active, border and border-soft
form the scheme-specific surface layer. Sidebar selected text (#C7D2FE) and
table selected text (#E0E7FF) remain separate dark component states. Both use
rgba(99,102,241,.16) backgrounds; sidebar and tab indicators remain #818CF8.

Shared templates retain light primitive mappings. Dark generation remaps only
primary action declarations and focus declarations to semantic names; inherited
selection fallbacks are overridden by the explicit dark component cascade.
Spinner assets keep their intentional fixed ring/arc paints. The verifier checks
both stored HTML extractions, generated primitive definitions and independent
semantic states, including a negative regression for corrupt dark p700.
