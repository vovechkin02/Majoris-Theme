# GTK4/libadwaita

GTK theme settings alone are insufficient for libadwaita. Development installation symlinks gtk.css, gtk-dark.css **and colors.css** into the normal user override directory; relative imports resolve beside the symlink path. Existing files are journaled and backed up. No application appearance stylesheet masks theme failures.

The gallery uses Trixie's libadwaita 1.7 widgets including AlertDialog, SwitchRow and SpinRow. Deprecated but available ColorButton and FontButton intentionally exercise native legacy controls. CSS parsing and simple/dense border-box geometry are tested.
Native spinner vectors live in gtk-4.0/assets and are linked alongside user CSS. Re-running the installer adds new asset/font links while preserving existing backups. The real-node mappings include dialog.alert/floating-sheet and banner/revealer/widget; stock toolkit image backgrounds, preference subtitle opacity and nested menu-button styling require explicit cascade resets.

The factory contains two focus descriptions for titlebar buttons. Its generic
focus selector gives a coloured inner border, but its later explicit
state-verification example reserves a transparent border and shows an external
halo. Majoris follows that explicit example in both toolkits: a transparent 1px
reserved border, unchanged 32x32 plate and external 2px halo. Light uses
rgba(99,102,241,.24); dark uses rgba(129,140,248,.36). No regular control shadow
is added. The supplied HTML has not been changed.

Floating GTK4 CSD windows receive the authority's 1px outer edge, 8px radius and
window shadow on window.csd. GTK3 owns the corresponding decoration node.
Managed maximized/fullscreen/tiled and directional tiled GTK classes remove the
outer border allocation, shadow and radius. Actual maximize/fullscreen are
exercised with Openbox; tiled classes are diagnostic equivalents under X11.
Mutter/Wayland tiling, fractional scaling and compositor shadows require GNOME
VM acceptance. The outer edge reserves 1px on each side, without increasing the
internal 48px header allocation or the 32px controls and 16px glyphs.
