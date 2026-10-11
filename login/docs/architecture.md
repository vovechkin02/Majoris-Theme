# Architecture and ownership

The downstream patch adds `js/gdm/majorisLogin.js` to Shell's compiled JavaScript
resource, with hooks in `gdm/loginDialog.js`, `gdm/authPrompt.js`,
`ui/unlockDialog.js`, `ui/screenShield.js`, `ui/layout.js`, `ui/boxpointer.js`,
`ui/userWidget.js`, `ui/status/accessibility.js`, `ui/status/keyboard.js` and
`ui/sessionMode.js`. The resource is part of the
version-matched Debian Shell rebuild, not a user extension or an installed-file
replacement. Exact module hashes are checked before quilt applies either patch.

`LoginDialog` retains AccountsService filtering (system/locked users excluded),
GDM's hidden-list and manual/domain username paths, timed login, realm hints,
session enumeration/defaults and session launch. `AuthPrompt` retains native
GDM conversations, secret/nonsecret stages, fingerprint/smartcard messages,
choice lists, retry/lockout, cancellation, Caps Lock and St.PasswordEntry.
The added Sign In button calls the same `_activateNext` path as Enter; its
sensitivity follows the current prompt and disallows duplicate submissions.
The native Cancel action is presented as Switch Account. Clearing and successful
completion reset password visibility and sensitive response text. No response
is logged, copied to a label, or included in the visual test screenshots.

`UnlockDialog` retains its own verifier and current user, tap/key/touch handling,
notification privacy policy, and user switching. `ScreenShield` keeps every
modal grab, authentication check and completion callback. Only presentation
timing/opacity replaces curtain movement. Wallpaper assets cover every monitor;
authentication stays on GNOME's primary-monitor constraint.

The bottom panel keeps the native input source selector, dwell click, complete
accessibility menu and NetworkManager Quick Settings. A separate power button
uses native SystemActions capability properties and its Suspend/Restart/Power
Off methods, preserving logind/polkit/inhibitors and EndSessionDialog. No shell
commands perform actions. Reduced Motion binds the native enable-animations key;
all existing useful accessibility options remain available.

The private `org.majoris.login` schema supplies enabled/appearance/logo settings.
Dark is the default; light is a complete separate palette from the prototype.
Install-time defaults only affect the GDM profile. Lock presentation reads the
user session's schema defaults/settings; administrators can supply a system
dconf default/lock for consistent policy. An absent schema or CSS uses stock UI.
No user-home assets are read before login. Fonts are bundled with their SIL OFL.

## Visual translation and deliberate deviations

Prototype tokens are preserved in `theme/tokens.json`; the St CSS generator
explicitly scopes every rule to private login/menu/panel classes. GTK rules and
the existing desktop theme are untouched. Cards use 8px radii, 432px outer width,
36/40/28px padding, 72px avatars and 48px inputs. Error space is reserved.
Hover/focus is 128ms, main fades 256ms, and St reduced-motion is respected.
The atmospheric wallpaper is precomposited at 3840×2160; controls remain native
vector/text actors and scale through St/Mutter. Card translucency overlays this
static background; no expensive live blur shader is added.

The repository has no approved Majoris logo, so a typographic wordmark replaces
the placeholder glyph. Administrators can set an approved system-wide SVG path
using the logo key. The module supplies the prototype's symbolic SVG geometry;
native keyboard/network/password widgets retain appropriate GNOME symbolic icons.

Network functionality remains in GNOME's complete Quick Settings popover rather
than a custom reduced Wi-Fi-only menu. Other-user authentication uses sequential
native username/PAM prompts rather than collecting a speculative password before
GDM asks for one. Session names come from installed GDM sessions, never fixed
Majoris/X11 labels. Native authentication messages remain authoritative rather
than a hardcoded password-only instruction. Admin banners retain a scroll view.
Confirmation dialogs remain native, preserving authorization semantics.

No claim of pixel-perfect prototype parity or production VM acceptance follows
from source/resource contracts. Native screenshots and the VM matrix identify
what has actually been exercised. The upstream APIs and exact Debian source were
reviewed from https://packages.debian.org/source/trixie/gnome-shell and the
matching downloaded source package. Supported logo configuration is documented
at https://help.gnome.org/system-admin-guide/login-logo.html.en.
