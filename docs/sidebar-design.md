# Majoris sidebar contract

The light/dark canonical widget-factory references were explicitly revised on
26 October 2026 for sidebar finalisation. This supersedes their earlier sidebar
geometry only. Primitive palettes, fonts, window glyphs and unrelated components
retain their existing authority.

| Property | Contract |
|---|---|
| Preferred desktop width | 224px, chosen by the application |
| Surface gutters | 16px top/bottom, 8px horizontally |
| Row visual minimum / gap / pitch | 32px / 4px / 36px |
| Row horizontal inset / radius | 8px / 4px |
| Symbolic icon / icon-label gap | 16×16px / 8px |
| Selection stripe | 2px wide, 8px top and bottom |
| Normal / selected label | Plus Jakarta Sans 14px, Medium 500 / SemiBold 600 |
| Heading | 12px/600, 8px horizontal inset, 0px above the first heading; 16px above later headings; 8px below |
| Supporting description / badge | 12px/400 secondary text / 12px/600 count |
| Optional child indentation | 16px beyond parent content (24px total row inset) |
| Transition | 128ms cubic-bezier(.2,0,0,1), stationary |

The 32px minimum is the painted row, excluding its 4px bottom margin. GTK can
include CSS margins in allocation accessors: a 36px reported outer allocation
is not a 36px painted row. Larger native text may increase both row height and
pitch; no exact height or clipped label is imposed. Badges use a compact 20px
minimum line area and 4px corners rather than capsules.

## Opt-in containers and subcomponents

- `.sidebar`, `.navigation-sidebar`, `.majoris-sidebar`: scoped navigation
  surfaces and row states; none sets a global sidebar width.
- `majoris-sidebar-heading`: nonselectable Label, preferably a ListBox row
  header. CSS owns its group spacing; do not repeat that margin in application code.
- `majoris-sidebar-heading-first`: combine with the heading class only when
  its section begins the visible navigation content; this removes its top margin.
  The sidebar still supplies its 16px outer inset.
- `majoris-sidebar-description`: optional secondary 12px/400 text, including
  descriptions inside explicitly composed rows.
- `majoris-sidebar-badge`: optional trailing Label/count. The application
  supplies the value and its accessible meaning.
- `majoris-sidebar-group`: native Gtk.Expander group treatment.
- `majoris-sidebar-group-title`: the expander's native label widget, with the
  same minimum and typography as a row.
- `majoris-sidebar-child`: apply to child ListBoxRows for a 16px additional inset.
- `majoris-sidebar-native-divider`: add alongside the navigation class when
  the containing native split view already supplies separation. It suppresses
  the theme divider, preventing two adjacent lines. Use it only after verifying
  that the native container actually paints a divider. The current Majoris
  NavigationSplitView fixture retains one CSS-owned divider: native separation
  was not visible in its rendered pane, so suppressing this line would remove
  separation entirely.

Apply a navigation class to one owner: either a ListBox itself or an inner Box
containing a list, native headers and expandable groups. Do not also mark every
nested list as a sidebar, add duplicate 16px/8px margins, or put an extra card
around the pane. Native GtkStackSidebar is handled separately: its wrapper has
zero padding and its internal list owns the gutters, while the wrapper owns
one divider. Applications retain StackSidebar's native stack switching.

## Native row composition

```vala
Gtk.ListBoxRow navigation_row (string title, string icon_name, string? count) {
    var row = new Gtk.ListBoxRow ();
    var content = new Gtk.Box (Gtk.Orientation.HORIZONTAL, 8);
    var icon = new Gtk.Image.from_icon_name (icon_name);
    icon.pixel_size = 16;
    icon.halign = Gtk.Align.CENTER;
    icon.valign = Gtk.Align.CENTER;
    content.append (icon);
    var label = new Gtk.Label (title);
    label.xalign = 0; // LTR; use the corresponding alignment for RTL
    label.hexpand = true;
    label.valign = Gtk.Align.CENTER;
    label.ellipsize = Pango.EllipsizeMode.END;
    content.append (label);
    if (count != null) {
        var badge = new Gtk.Label (count);
        badge.valign = Gtk.Align.CENTER;
        badge.add_css_class ("majoris-sidebar-badge");
        content.append (badge);
        row.update_property (Gtk.AccessibleProperty.DESCRIPTION,
                             "Count: " + count, -1);
    }
    row.child = content;
    row.tooltip_text = title;
    row.update_property (Gtk.AccessibleProperty.LABEL, title, -1);
    return row;
}
var navigation = new Gtk.ListBox ();
navigation.add_css_class ("majoris-sidebar");
navigation.selection_mode = Gtk.SelectionMode.SINGLE;
navigation.append (navigation_row ("Documents", "folder-symbolic", "12"));
```

The row owns its full interactive surface. Its label and icon are not separate
buttons. Use native Box spacing=8 and centre image/badge allocations; preserve
the flexible, ellipsised label. Provide the complete title through accessibility
and a tooltip, and describe badge semantics (for example unread messages) in the
application's language. Do not pad SVGs to align them. GTK3 uses Box.pack_start,
Row.add, StyleContext.add_class and the native Image pixel-size API instead.

## Surfaces and states

| Role | Light | Dark |
|---|---|---|
| Sidebar | #F2F2F4 | #1D1D20 |
| Primary / secondary text | #1C1C1F / #626269 | #F4F4F5 / #A9A9B0 |
| Divider | #E5E5E9 | #313136 |
| Hover / pressed | #ECECEF / #E2E2E6 | #303035 / #38383D |
| Selected surface | #EEF2FF | rgba(99,102,241,.16) |
| Selected hover / pressed | #E0E7FF / #C7D2FE | rgba(99,102,241,.22) / rgba(99,102,241,.28) |
| Selected foreground | #4338CA | #C7D2FE |
| Indicator / focus | #6366F1 | #818CF8 |

Only selected rows receive the stripe. Hover/pressed selected rows retain it.
A keyboard-focused unselected row gets an inset 2px focus treatment, not a
selection fill or stripe. Disabled rows use tertiary foreground with no hover,
pressed surface or indicator. Backdrop reduces normal emphasis and gently blends
selected text toward secondary text while retaining selection and its stripe.
There are no row borders, shadows, transforms, scales or sliding indicators.
The only gradient images construct the narrow indicator; pane surfaces are flat.

## Groups, scrolling and adaptive navigation

Use native ListBox headers for headings; they are not selectable rows and have
no hover/selection treatment. For expandable sections, use Gtk.Expander with a
label carrying `majoris-sidebar-group-title` and a child ListBox. Mark child rows
`majoris-sidebar-child`; expansion controls are distinct from selected rows.
Coordinate selection across multiple lists in application code, preserving the
active page while a group is collapsed. The GTK4 expander exposes
`expander-widget > box > title > expander`; GTK3 uses its `expander`/title structure. Their
scoped selectors differ rather than inventing a shared internal node tree.

Place the single padded surface inside a native ScrolledWindow. Let overlay
scrollbars and native keyboard focus scrolling work normally; do not add an
opaque trough or scrolling shadow. A fixed account/storage footer, if needed,
belongs outside the scroller in a native vertical Box. Use plain labels and
native layout there; avoid a second navigation padding owner.

Choose 224px as a preferred starting width, not as a CSS lock. Files or Settings
may use wider names, while other applications may choose narrower panes. The
factory's standalone fixture uses NavigationSplitView with a 224px minimum,
320px maximum and a fraction anchored to its 900px default window. A native
Breakpoint at 650px switches to collapsed navigation. Header controls expose
navigation/content, and content remains available in a 390px window.

Application-owned breakpoint handlers save the chosen row, set the native
collapsed property, then restore selection/focus when returning to desktop.
This avoids libadwaita restoring an earlier focused row as the active page.
The fixture's `change_layout()` demonstrates this without changing toolkit
navigation. Do not let unrelated global Space/Return accelerators steal native
list/expander activation. The factory disables only its unused Open/Preview
placeholder actions in this new window; other menu fixtures retain them.

RTL applications should use GTK's locale/default reading direction (or apply
it consistently to all widgets when changing it live). Box ordering and child
indentation mirror, labels align toward the appropriate start edge, and the
stripe/divider move to the leading/trailing edges respectively. CSS cannot
supply an application's navigation structure or language direction.

## GTK3 indicator and accessibility notes

GTK4 supports the fixed-inset gradient directly. GTK3 cannot parse calc() in
this gradient, so two opaque end caps mask a 2px solid stripe. End-cap colours
are generated from the same semantic selected/hover/pressed surfaces, composited
over the sidebar for alpha colours. Both implementations retain fixed 8px ends
when text enlarges; no percentage-inset approximation or custom drawing widget
is used. Toolkit-specific unsupported properties are omitted from GTK3 output.

Fontconfig resolves actual Medium and SemiBold Plus Jakarta Sans faces. Tests
convert GTK3's point descriptions to logical pixels and compare GTK4 absolute
pixel descriptions correctly. Device scaling is distinct from text enlargement.
The approved absolute 14px CSS does not grow merely by changing legacy Xft DPI
in this X11 environment. Non-clipping enlarged-text tests therefore request
2× text using native Pango attributes, growing painted rows from 32px to 36px
while keeping 8px indicator caps. Real GNOME text-scaling settings, fractional
scaling, Wayland and screen-reader behavior remain session acceptance checks;
the tests do not claim those settings were exercised.

Installing the theme supplies presentation for matching structures, not a
fully structured sidebar in every third-party application. Row contents,
accessible descriptions, group composition, counts, preferred widths, adaptive
collapse, focus/selection coordination and actual navigation remain app-owned.
See [the implementation report](sidebar-finalisation.md) for before/after values,
validation evidence and remaining checks.

## Initial section spacing

`SidebarNavigation.configure(list)` installs the factory's reusable native
header composition. `SidebarNavigation.append_navigation(list, row, section)`
associates an optional section title with a row. GTK's public header callback
supplies the previous visible row; a null predecessor applies the first-heading
modifier. Visibility changes invalidate headers, while GTK also re-evaluates
headers after insertions, removals and reordering. Hide all rows belonging to a
section to hide that section; do not leave an empty header or spacer behind.
A list beginning directly with a row needs no heading or compensation margin.
Standalone headings in static compositions explicitly receive the same modifier.
GTK3 apps can use the equivalent public ListBox header callback and CSS classes.
See [padding correction and native measurements](sidebar-padding.md).
