# GTK4/libadwaita

GTK theme settings alone are insufficient for libadwaita. Explicit light/dark development installation symlinks the selected gtk.css, gtk-dark.css and both colour files into the normal user override directory; relative imports resolve beside the symlink path. Existing files are journaled and backed up. No application appearance stylesheet masks theme failures.

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


Development `--variant=auto` backs up the existing gtk.css through the same
journal and links a neutral comment-only file. It imports neither light nor
dark CSS. Use the factory or `scripts/with-majoris-gtk4.sh PROGRAM` to attach the
unchanged StyleManager bridge. Auto installation alone does not globally attach
libraries to arbitrary applications. Changing light/dark/auto modes retains the
original backup; uninstall restores original files or symlinks and rejects later
user edits. Both explicit modes still select their fixed user CSS entrypoints.

The shared generated `desktopwindow` exception is emitted after native overrides
so active/backdrop desktop windows remain transparent, square, borderless and
shadowless. Native GTK3/4 style-render probes verify zero alpha without changing
normal application styling. Actual DING focus/wallpaper lifecycle is a GNOME VM
check, not a claim from those native probes.

This theme provides CSS and the GTK3/GTK4 bridges. The OS/session provides global
attachment/dispatcher policy, Shell extension activation, wallpaper and Mutter
lifecycle. No session-wide LD_PRELOAD or `/etc/environment` policy is installed
here. See [VM validation](theme-state-vm-checklist.md).
