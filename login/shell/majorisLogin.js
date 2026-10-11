// SPDX-License-Identifier: GPL-2.0-or-later
// Presentation only. GDM's AuthPrompt, verifier, user list and screen shield
// remain the owners of credentials, conversations and the modal lock grab.
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GObject from 'gi://GObject';
import GLib from 'gi://GLib';
import GnomeDesktop from 'gi://GnomeDesktop';
import St from 'gi://St';

const DATA = '/usr/share/majoris-login';
let settings;
let Main;

export function enabled() {
    const schema = Gio.SettingsSchemaSource.get_default().lookup('org.majoris.login', true);
    if (!schema)
        return false;
    settings ??= new Gio.Settings({settings_schema: schema});
    return settings.get_boolean('enabled') &&
        Gio.File.new_for_path(`${DATA}/theme/login.css`).query_exists(null);
}

export function duration(milliseconds) {
    return St.Settings.get().enable_animations ? milliseconds : 0;
}

export function appearance() {
    if (!enabled())
        return 'dark';
    return settings.get_string('appearance');
}

export function initials(name) {
    const words = name.trim().split(/\s+/u).filter(Boolean);
    return words.slice(0, 2).map(word => Array.from(word)[0]).join('').toLocaleUpperCase();
}

export function avatarFallback(user) {
    return new St.Label({
        text: initials(user?.get_real_name() || user?.get_user_name() || ''),
        style_class: 'majoris-avatar-initials',
        x_align: Clutter.ActorAlign.CENTER,
        y_align: Clutter.ActorAlign.CENTER,
    });
}

function move(actor, parent, index = -1) {
    actor.get_parent()?.remove_child(actor);
    if (index < 0)
        parent.add_child(actor);
    else
        parent.insert_child_at_index(actor, index);
}

export function decoratePrompt(prompt) {
    if (!enabled())
        return;
    prompt.add_style_class_name('majoris-card');
    prompt._majorisQuestion = new St.Label({style_class: 'majoris-question'});
    prompt.insert_child_at_index(prompt._majorisQuestion, 1);
    prompt._majorisIntro = new St.Label({text: _('Sign in to continue'), style_class: 'majoris-intro', x_align: Clutter.ActorAlign.CENTER});
    prompt.insert_child_at_index(prompt._majorisIntro, 1);
    prompt._mainBox.orientation = Clutter.Orientation.VERTICAL;
    prompt._defaultButtonWell.clear_constraints();
    prompt._defaultButtonWell.set_width(-1);
    prompt._majorisSubmit = new St.Button({
        style_class: 'majoris-primary',
        reactive: true,
        can_focus: true,
        track_hover: true,
        x_expand: true,
        accessible_name: _('Sign In'),
    });
    const contents = new St.BoxLayout({x_align: Clutter.ActorAlign.CENTER});
    contents.add_child(new St.Label({text: _('Sign In'), y_align: Clutter.ActorAlign.CENTER}));
    contents.add_child(new St.Icon({icon_name: 'go-next-symbolic', icon_size: 16}));
    move(prompt._defaultButtonWell, contents);
    prompt._majorisSubmit.child = contents;
    prompt._majorisSubmit.connect('clicked', () => {
        // Exactly the same native path as Enter, including username queries.
        if (prompt._entry.reactive && prompt._entry.visible && !prompt._authList.visible)
            prompt._activateNext(prompt._entry === prompt._passwordEntry);
    });
    prompt._majorisFooter = new St.BoxLayout({style_class: 'majoris-auth-footer', x_expand: true});
    move(prompt.cancelButton, prompt._majorisFooter);
    prompt.cancelButton.label = _('Switch Account');
    prompt.cancelButton.add_style_class_name('majoris-text-action');
    prompt.add_child(prompt._majorisSubmit);
    prompt.add_child(prompt._majorisFooter);
    prompt._message.y_expand = false;
    prompt._userWell.y_expand = false;
    prompt.connect('destroy', () => {
        prompt._majorisSubmit = null;
    });
}

export function syncSensitivity(prompt, sensitive) {
    if (!prompt._majorisSubmit)
        return;
    prompt._majorisSubmit.reactive = sensitive && !prompt._authList.visible;
    prompt._majorisSubmit.can_focus = prompt._majorisSubmit.reactive;
    if (prompt._majorisSubmit.reactive)
        prompt._majorisSubmit.remove_style_pseudo_class('insensitive');
    else
        prompt._majorisSubmit.add_style_pseudo_class('insensitive');
}

// Uses the same SystemActions methods as GNOME's ShutdownItem. Availability,
// inhibitors, policy and EndSessionDialog confirmations are deliberately native.
async function powerButton() {
    // Import after Shell startup: importing status/dialog classes while
    // AuthPrompt is evaluated would create a cyclic class initialization.
    const PanelMenu = await import('../ui/panelMenu.js');
    const SystemActions = await import('../misc/systemActions.js');
    const button = new PanelMenu.Button(0, _('Power'));
    button.add_child(new St.Icon({icon_name: 'system-shutdown-symbolic', style_class: 'system-status-icon'}));
    const actions = SystemActions.getDefault();
    for (const [label, capability, method] of [
        [_('Suspend'), 'can-suspend', 'activateSuspend'],
        [_('Restart…'), 'can-restart', 'activateRestart'],
        [_('Power Off…'), 'can-power-off', 'activatePowerOff'],
    ]) {
        const item = button.menu.addAction(label, () => actions[method]());
        actions.bind_property(capability, item, 'visible', GObject.BindingFlags.SYNC_CREATE);
    }
    button.menu.connect('open-state-changed', (_menu, open) => {
        if (open)
            actions.forceUpdate();
    });
    return button;
}

function box(x, y, width, height) {
    const allocation = new Clutter.ActorBox();
    allocation.set_origin(Math.round(x), Math.round(y));
    allocation.set_size(Math.max(0, Math.round(width)), Math.max(0, Math.round(height)));
    return allocation;
}

export class Chrome {
    constructor(root, {lock = false} = {}) {
        this.root = root;
        this.lock = lock;
        root.add_style_class_name('majoris-login');
        this.header = new St.BoxLayout({style_class: 'majoris-header'});
        this.brand = new St.BoxLayout({style_class: 'majoris-brand', x_expand: true});
        // No placeholder mark: the repository supplies no approved logo.
        const logo = settings.get_string('logo');
        if (logo && Gio.File.new_for_path(logo).query_exists(null))
            this.brand.add_child(new St.Icon({gicon: Gio.FileIcon.new(Gio.File.new_for_path(logo)), icon_size: 28}));
        this.brand.add_child(new St.Label({text: 'majoris'}));
        this.header.add_child(this.brand);
        this.date = new St.Label({style_class: 'majoris-top-date', y_align: Clutter.ActorAlign.CENTER});
        this.header.add_child(this.date);
        root.add_child(this.header);
        this.caption = new St.Label({text: _('Your space. Your way.'), style_class: 'majoris-caption'});
        root.add_child(this.caption);
        this.clock = new GnomeDesktop.WallClock({time_only: true});
        this.clock.connect('notify::clock', () => this._updateClock());
        this._updateClock();
        this.themeFile = Gio.File.new_for_path(`${DATA}/theme/login.css`);
        St.ThemeContext.get_for_stage(global.stage).get_theme().load_stylesheet(this.themeFile);
        settings.connectObject('changed::appearance', () => this.sync(), root);
        this.a11y = new Gio.Settings({schema_id: 'org.gnome.desktop.a11y.interface'});
        this.a11y.connectObject('changed::high-contrast', () => this.sync(), root);
        Main.sessionMode.connectObject('updated', () => this.sync(), root);
        Main.layoutManager.connectObject('monitors-changed', () => this.sync(), root);
        Main.layoutManager.connectObject('startup-complete', () => this.sync(), root);
        Main.layoutManager.panelBox.connectObject('notify::height', () => this.positionPanel(), root);
        root.connect('destroy', () => this.destroy());
        this.sync();
    }

    _updateClock() {
        const date = GLib.DateTime.new_now_local();
        this.date.text = `${date.format(_('%A, %-d %B'))}   ${this.clock.clock}`;
    }

    sync() {
        const palette = appearance();
        if (this.a11y.get_boolean('high-contrast'))
            this.root.add_style_class_name('majoris-high-contrast');
        else
            this.root.remove_style_class_name('majoris-high-contrast');
        this.root.remove_style_class_name(palette === 'dark' ? 'majoris-light' : 'majoris-dark');
        this.root.add_style_class_name(`majoris-${palette}`);
        if (this.sessionMenu) {
            this.sessionMenu.remove_style_class_name(palette === 'dark' ? 'majoris-light' : 'majoris-dark');
            this.sessionMenu.add_style_class_name(`majoris-${palette}`);
        }
        // A uniform native background on every monitor; no private wallpaper
        // from the user's session is revealed behind the lock prompt.
        if (this.lock) {
            for (const widget of this.root._backgroundGroup.get_children())
                wallpaper(widget, palette);
            const primary = Main.layoutManager.primaryMonitor;
            if (primary) {
                const scale = St.ThemeContext.get_for_stage(global.stage).scale_factor;
                const size = Math.min(164, Math.max(88, primary.width / scale * 0.12));
                this.root._clock._time.set_style(`font-size: ${size}px;`);
            }
        } else {
            this.backgrounds ??= new St.Widget({layout_manager: new Clutter.FixedLayout()});
            if (!this.backgrounds.get_parent())
                Main.layoutManager.screenShieldGroup.insert_child_at_index(this.backgrounds, 0);
            this.backgrounds.destroy_all_children();
            for (const monitor of Main.layoutManager.monitors) {
                const actor = new St.Widget();
                actor.set_position(monitor.x, monitor.y);
                actor.set_size(monitor.width, monitor.height);
                wallpaper(actor, palette);
                this.backgrounds.add_child(actor);
            }
        }
        this.syncPanel();
    }

    syncPanel() {
        const active = Main.sessionMode.isGreeter || Main.sessionMode.isLocked;
        if (!Main.panel)
            return;
        Main.panel.remove_style_class_name('majoris-dark');
        Main.panel.remove_style_class_name('majoris-light');
        if (active) {
            if (Main.panel.statusArea.a11y)
                Main.panel.statusArea.a11y.visible = true;
            const quick = Main.panel.statusArea.quickSettings;
            if (quick?._system?.get_parent() && !this.powerStatus) {
                this.powerStatus = quick._system;
                this.powerStatusParent = quick._system.get_parent();
                this.powerStatusParent.remove_child(this.powerStatus);
            }
            Main.panel.add_style_class_name('majoris-login-panel');
            Main.panel.add_style_class_name(`majoris-${appearance()}`);
            // Keep all native indicators, including dwell click and network.
            // A dedicated power button makes the prototype action accessible.
            if (!this.power && !this.powerPending) {
                this.powerPending = true;
                powerButton().then(button => {
                    this.powerPending = false;
                    if (this.destroyed || !(Main.sessionMode.isGreeter || Main.sessionMode.isLocked)) {
                        button.destroy();
                        return;
                    }
                    this.power = button;
                    Main.panel.addToStatusArea('majorisLoginPower', button, -1, 'right');
                    this.syncPanel();
                }).catch(logError);
            }
            for (const indicator of Object.values(Main.panel.statusArea)) {
                const menu = indicator.menu?.actor;
                if (!menu)
                    continue;
                menu.add_style_class_name('majoris-login-menu');
                menu.remove_style_class_name('majoris-light');
                menu.remove_style_class_name('majoris-dark');
                menu.add_style_class_name(`majoris-${appearance()}`);
                if (this.a11y.get_boolean('high-contrast'))
                    menu.add_style_class_name('majoris-high-contrast');
                else
                    menu.remove_style_class_name('majoris-high-contrast');
                // The native panel is now at the bottom; open menus upward.
                if (indicator.menu._boxPointer)
                    indicator.menu._boxPointer.updateArrowSide(St.Side.BOTTOM);
            }
        } else {
            this.restorePowerStatus();
            Main.panel.statusArea.a11y?._syncMenuVisibility();
            Main.panel.remove_style_class_name('majoris-login-panel');
            this.power?.destroy();
            this.power = null;
            for (const indicator of Object.values(Main.panel.statusArea)) {
                indicator.menu?.actor.remove_style_class_name('majoris-login-menu');
                indicator.menu?.actor.remove_style_class_name('majoris-light');
                indicator.menu?.actor.remove_style_class_name('majoris-dark');
                indicator.menu?.actor.remove_style_class_name('majoris-high-contrast');
                if (indicator.menu?._boxPointer)
                    indicator.menu._boxPointer.updateArrowSide(St.Side.TOP);
            }
        }
        this.positionPanel();
    }

    positionPanel() {
        const monitor = Main.layoutManager.primaryMonitor;
        if (!monitor)
            return;
        const panel = Main.layoutManager.panelBox;
        const scale = St.ThemeContext.get_for_stage(global.stage).scale_factor;
        const active = Main.sessionMode.isGreeter || Main.sessionMode.isLocked;
        panel.set_position(monitor.x, active ? monitor.y + monitor.height - panel.height - 32 * scale : monitor.y);
    }

    restorePowerStatus() {
        if (this.powerStatus) {
            this.powerStatusParent.add_child(this.powerStatus);
            this.powerStatus = null;
            this.powerStatusParent = null;
        }
    }

    allocate(width, height) {
        const scale = St.ThemeContext.get_for_stage(global.stage).scale_factor;
        const margin = (width / scale < 640 ? 20 : 48) * scale;
        this.header.allocate(box(margin, 32 * scale, width - margin * 2, 32 * scale));
        this.caption.allocate(box(margin, height - 54 * scale, width / 2, 22 * scale));
        this.caption.visible = width / scale >= 640;
    }

    allocateLogin(dialog, allocation) {
        const [width, height] = allocation.get_size();
        this.allocate(width, height);
        const scale = St.ThemeContext.get_for_stage(global.stage).scale_factor;
        const margin = 24 * scale;
        const top = 104 * scale;
        const bottom = height - 96 * scale;
        for (const actor of [dialog._authPrompt, dialog._userSelectionBox]) {
            if (!actor.visible)
                continue;
            const w = Math.min(432 * scale, width - 2 * margin);
            const [, naturalHeight] = actor.get_preferred_height(w);
            const h = Math.min(naturalHeight, bottom - top);
            actor.allocate(box((width - w) / 2, top + (bottom - top - h) / 2, w, h));
        }
        // Admin banners retain their scroll view, above the card.
        if (dialog._bannerView.visible)
            dialog._bannerView.allocate(box(margin, 68 * scale, width - margin * 2, 32 * scale));
        if (dialog._logoBin.visible)
            dialog._logoBin.allocate(box(0, 0, 0, 0));
    }

    destroy() {
        this.destroyed = true;
        this.restorePowerStatus();
        this.power?.destroy();
        this.backgrounds?.destroy();
        this.clock.run_dispose();
        Main.panel?.remove_style_class_name('majoris-login-panel');
        Main.panel?.remove_style_class_name('majoris-light');
        Main.panel?.remove_style_class_name('majoris-dark');
        for (const indicator of Object.values(Main.panel?.statusArea ?? {})) {
            for (const name of ['majoris-login-menu', 'majoris-light', 'majoris-dark', 'majoris-high-contrast'])
                indicator.menu?.actor.remove_style_class_name(name);
            indicator.menu?._boxPointer?.updateArrowSide(St.Side.TOP);
        }
        const monitor = Main.layoutManager.primaryMonitor;
        if (monitor)
            Main.layoutManager.panelBox.set_position(monitor.x, monitor.y);
    }
}

export function createChrome(root, params, main) {
    Main = main;
    return enabled() ? new Chrome(root, params) : null;
}

export function wallpaper(widget, palette = appearance()) {
    widget.set_style(`background-image: url("${DATA}/assets/wallpapers/${palette}.png"); background-size: cover;`);
}

export function configureLogin(dialog, main) {
    const chrome = createChrome(dialog, {}, main);
    if (!chrome)
        return null;
    dialog._userSelectionBox.add_style_class_name('majoris-card');
    const heading = new St.Label({text: _('Choose an Account'), style_class: 'majoris-heading'});
    dialog._userSelectionBox.insert_child_at_index(heading, 0);
    dialog._notListedButton.child.text = _('Other User');
    move(dialog._sessionMenuButton, dialog._authPrompt._majorisFooter);
    dialog._sessionMenuButton.x_expand = true;
    dialog._sessionMenuButton.x_align = Clutter.ActorAlign.END;
    dialog._sessionMenuButton._menu.actor.add_style_class_name('majoris-login-menu');
    dialog._sessionMenuButton._menu.actor.add_style_class_name(`majoris-${appearance()}`);
    chrome.sessionMenu = dialog._sessionMenuButton._menu.actor;
    dialog._authPrompt._majorisSubmit.connect('notify::reactive', () => {
        if (!dialog._authPrompt._majorisSubmit.reactive)
            dialog._sessionMenuButton.updateSensitivity(false);
    });
    dialog.connect('destroy', () => dialog._sessionMenuButton._menu.destroy());
    return chrome;
}
