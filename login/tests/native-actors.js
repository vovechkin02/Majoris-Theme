// SPDX-License-Identifier: GPL-2.0-or-later
// Real Shell/St actor and CSS fixture. No authentication is attempted here.
// The runner supplies mocked system services; this is NOT a GDM/PAM test.
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';
import MetaTest from 'gi://MetaTest';
import St from 'gi://St';

import * as LoginDialog from 'resource:///org/gnome/shell/gdm/loginDialog.js';
import * as AuthPrompt from 'resource:///org/gnome/shell/gdm/authPrompt.js';
import * as GdmUtil from 'resource:///org/gnome/shell/gdm/util.js';
import * as UnlockDialog from 'resource:///org/gnome/shell/ui/unlockDialog.js';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as Scripting from 'resource:///org/gnome/shell/ui/scripting.js';

export const METRICS = {};
Gio._promisify(Shell.Screenshot.prototype, 'screenshot', 'screenshot_finish');
let monitor;

export function init() {
    global.connect('shutdown', () => monitor?.destroy());
    GLib.timeout_add_seconds(GLib.PRIORITY_LOW, 2, () => {
        const [width, height] = (GLib.getenv('MAJORIS_LOGIN_SIZE') ?? '1280x720').split('x').map(Number);
        monitor = MetaTest.TestMonitor.new(global.context, width, height, 60.0);
        return GLib.SOURCE_REMOVE;
    });
}

function assert(condition, message) {
    if (!condition)
        throw new Error(message);
}

export async function run() {
    await Scripting.sleep(1000);
    Main.overview.hide();
    Main.messageTray.bannerBlocked = true;
    Main.sessionMode.pushMode('unlock-dialog');
    Main.layoutManager.screenShieldGroup.show();
    GLib.setenv('XDG_SESSION_ID', 'dummy', true);
    const settings = new Gio.Settings({schema_id: 'org.majoris.login'});
    const output = GLib.getenv('MAJORIS_LOGIN_CAPTURE_DIR');
    GLib.mkdir_with_parents(output, 0o755);
    const measurements = [];
    const login = new LoginDialog.LoginDialog(Main.layoutManager.screenShieldGroup);
    assert(login._majoris, 'Native login enhancement not loaded');
    login._userSelectionBox.hide();
    login._bannerView.hide();
    login.show();
    const prompt = login._authPrompt;
    prompt.setUser(login._userManager.get_user(GLib.get_user_name()));
    prompt._updateEntry(true);
    prompt.setQuestion(_('Password'));
    prompt.show();
    const capture = async (variant, view) => {
        await Scripting.sleep(350);
        const file = Gio.File.new_for_path(`${output}/${variant}-${view}.png`);
        const stream = file.replace(null, false, Gio.FileCreateFlags.NONE, null);
        await new Shell.Screenshot().screenshot(false, stream);
        stream.close(null);
    };
    for (const variant of ['dark', 'light']) {
        settings.set_string('appearance', variant);
        await capture(variant, 'login');
        login.grab_key_focus();
        await capture(variant, 'login-unfocused');
        prompt._entry.grab_key_focus();
        const entryBox = prompt._entry.get_transformed_position();
        prompt.setMessage(_('Authentication failed. Please try again.'), GdmUtil.MessageType.ERROR);
        await capture(variant, 'password-error');
        assert(JSON.stringify(entryBox) === JSON.stringify(prompt._entry.get_transformed_position()), 'Error moved the credential field');
        prompt.setMessage('', GdmUtil.MessageType.NONE);
        prompt.setUser(null);
        prompt.setQuestion(_('Username'));
        await capture(variant, 'other-user');
        prompt.hide();
        login._userSelectionBox.show();
        for (const user of login._userManager.list_users())
            login._userList.addUser(user);
        login._notListedButton.show();
        await capture(variant, 'accounts');
        login._userSelectionBox.hide();
        prompt.show();
        prompt.setUser(login._userManager.get_user(GLib.get_user_name()));
        prompt._updateEntry(true);
        prompt.setQuestion(_('Password'));
        // Empty fixture response only; never collect or render real credentials.
        prompt._passwordEntry.password_visible = true;
        prompt.clear();
        assert(!prompt._passwordEntry.password_visible, 'Clear must reset password visibility');
        prompt.updateSensitivity(false);
        assert(!prompt._majorisSubmit.reactive, 'Duplicate submission must be disabled');
        await capture(variant, 'authenticating');
        prompt.updateSensitivity(true);
        assert(prompt._majorisSubmit.reactive, 'Retry must re-enable submit');
        for (const role of ['keyboard', 'a11y', 'quickSettings', 'majorisLoginPower']) {
            const indicator = Main.panel.statusArea[role];
            assert(indicator?.menu, `Missing native ${role} control`);
            indicator.menu.open();
            await capture(variant, role);
            indicator.menu.close();
        }
        const geometry = prompt.get_allocation_box();
        measurements.push({variant, width: geometry.get_width(), height: geometry.get_height(), entry: entryBox, monitor: Main.layoutManager.primaryMonitor});
    }
    login.destroy();
    const unlock = new UnlockDialog.UnlockDialog(Main.layoutManager.screenShieldGroup);
    assert(unlock._majoris, 'Native lock enhancement not loaded');
    unlock.show();
    for (const variant of ['dark', 'light']) {
        settings.set_string('appearance', variant);
        await capture(variant, 'locked-clock');
        // Presentation fixture only; do not invoke verifier.begin or modal grab.
        const unlockPrompt = new AuthPrompt.AuthPrompt(unlock._gdmClient, AuthPrompt.AuthPromptMode.UNLOCK_ONLY);
        unlock._promptBox.add_child(unlockPrompt);
        unlockPrompt.setUser(unlock._user);
        unlockPrompt.setQuestion(_('Password'));
        unlock._setTransitionProgress(1);
        await capture(variant, 'unlock-prompt');
        assert(unlock._clock.translation_y === 0 && unlock._promptBox.translation_y === 0, 'Lock transition moved vertically');
        assert(unlock._clock.scale_x === 1 && unlock._promptBox.scale_x === 1, 'Lock transition scaled the UI');
        unlockPrompt.destroy();
        unlock._setTransitionProgress(0);
    }
    unlock.destroy();
    Main.sessionMode.popMode('unlock-dialog');
    Gio.File.new_for_path(`${output}/geometry.json`).replace_contents(JSON.stringify(measurements, null, 2), null, false, Gio.FileCreateFlags.NONE, null);
    console.log('Majoris native actor fixture PASS (authentication and VM acceptance NOT tested)');
}
