# Disposable GNOME VM acceptance

These checks are **unverified until recorded on an actual GDM/PAM session**.
Headless St screenshots, D-Bus fixtures and upstream unit tests do not satisfy
this matrix. Use a Debian 13 amd64 VM snapshot, the matched package trio, two
throwaway local accounts, and the saved stock recovery pair. Never use a real
password in screenshots, command arguments, test files or debug logs.

## Preflight and evidence

```sh
python3 login/tests/vm-preflight.py --output /tmp/majoris-login-preflight.json
dpkg-query -W gdm3 gnome-shell gnome-shell-common majoris-login-resources
systemctl is-active gdm3
journalctl -b -u gdm3 --no-pager
```

Review logs locally for exceptions/crashes; redact identifiers before sharing.
Keep screenshots only with empty/cleared credential fields. Record each check's
result, package version, monitor/scale, palette, boot ID, and evidence filename.
Do not mark an unavailable hardware authentication mechanism as passed.

| Area | Executable procedure | Acceptance |
|---|---|---|
| Boot/login | Boot the installed ISO; sign in to each throwaway account | GDM launches; installed session opens; no Shell exception |
| Incorrect response | Enter one deliberately incorrect password, then the correct one | Native retry/lockout policy; readable error; field/button positions stable |
| Switching | Begin a response, select Switch Account, choose another account | Old response cleared; native conversation cancelled; correct avatar/name |
| Other user | Choose Other User; enter a valid local username, then respond to PAM | Native sequential prompts; successful session start |
| Domain/multi-factor | Configure supported PAM/domain test environment, then use its account | Every native factor/question/choice displayed; no password-only assumption |
| Fingerprint/smartcard | Use configured test hardware and remove/reinsert while prompting | Native messages, cancellation, fallback and completion preserved |
| Account policy | Test one/many/zero eligible accounts, hidden-list setting, disabled account, long names, no avatar | No service accounts; hidden list still permits manual login; names/initials fit |
| Session chooser | Install two supported sessions, select each; remove one and repeat | Only installed sessions shown; selected/default session remembered; disabled during submit |
| Password eye | Toggle visibility with throwaway input; cancel/switch/submit | Masked by default; mask resets; no response in logs/labels/captures |
| Keyboard | Tab/Shift+Tab, Enter/Escape, Caps Lock; change each configured layout | Predictable focus and correct entered symbols; native layout really changes |
| Accessibility | Enable large text, high contrast, screen reader, OSK, zoom, sticky/slow/mouse keys, reduced motion | Native effects work; full menu retained; no clipped authentication controls |
| Network | Test wired/Wi-Fi/offline/no hardware in native Quick Settings | Actual state shown; policy respected; no fake connectivity |
| Power | Select Suspend, Restart, Power Off with and without inhibitors/policy | Native capability gating, confirmation and action; no bypass |
| Lock clock | Lock with Super+L; reveal with click, Enter and touch | Actual locale/timezone clock; fade only; no access to desktop |
| Unlock | Fail once then unlock; cancel and retry; switch user while locked | Native verifier/PAM; modal screen shield remains secure |
| Privacy | Create private notifications/windows, lock, inspect both monitors | Native notification policy preserved; no private session wallpaper/content leak |
| Suspend/resume | Suspend locked/unlocked; resume and authenticate | No bypass, crash, frozen field or stale input |
| Both palettes | Set dark/light in GDM profile and lock settings, refocus every control/menu | Correct card/input/text/menu/focus/error/disabled colours; no opaque white dark card |
| Geometry | Repeat at 1280×720, 1920×1080, 2560×1440, 3840×2160, 125/150/200%, wide/narrow monitors | Card/controls accessible; vector/text sharp; no overlap or off-screen popup |
| Multiple monitors | Change primary, hotplug, rotate, sleep/wake | One usable authentication surface; consistent secondary backgrounds |
| Translation | Use RTL locale and long translated strings, large text | Labels remain readable; keyboard order and menus usable |
| User desktop | Unlock and inspect ordinary apps/panel/settings/extensions | Native desktop preferences and existing Majoris theme unchanged; panel returns to top |
| Removal/recovery | Run both documented console recovery paths, log in, lock/unlock, reboot | Stock GDM and user session operational; accounts/data/autologin intact |
| Update | Install a stock newer Debian Shell pair in a snapshot | Stock fallback; no package hold/security-update block; revalidation required before custom rebuild |

## Native renderer fixture (not VM acceptance)

With the patched Shell build and build dependencies present:

```sh
sudo bash login/scripts/verify-native.sh /build/gnome-shell-48.7 BUILD_USER "$PWD/artifacts/login-native"
```

This uses a private mount namespace, private system/session buses and GNOME's
upstream mocked system services. It renders real LoginDialog/AuthPrompt/
UnlockDialog/St actors, captures empty-field states and checks reserved error
geometry, sensitivity, password masking reset, and fade-only movement. No PAM
answer, real login, lock grab, service restart or power action is performed.
The fixture's account belongs to the upstream mock AccountsService, which is
test data, not a production hardcoded account.
