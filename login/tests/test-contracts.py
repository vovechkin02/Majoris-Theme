#!/usr/bin/env python3
"""Source/resource contracts, explicitly not a PAM or compositor acceptance test."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
import tinycss2

ROOT = Path(__file__).resolve().parents[1]


class LoginContracts(unittest.TestCase):
    def test_generated(self):
        subprocess.run(['python3', str(ROOT / 'scripts/generate-theme.py'), '--check'], check=True)

    def test_palettes(self):
        parsed = tinycss2.parse_stylesheet((ROOT / 'theme/login.css').read_text(), skip_comments=True, skip_whitespace=True)
        rules = {}
        for rule in parsed:
            self.assertEqual(rule.type, 'qualified-rule')
            declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
            self.assertTrue(all(d.type == 'declaration' for d in declarations))
            values = {d.name: tinycss2.serialize(d.value).strip().upper() for d in declarations}
            for selector in tinycss2.serialize(rule.prelude).strip().split(','):
                rules.setdefault(selector.strip(), {}).update(values)
        tokens = json.loads((ROOT / 'theme/tokens.json').read_text())
        for variant, t in tokens.items():
            root = f'.majoris-login.majoris-{variant}'
            self.assertEqual(rules[root]['color'], t['text'].upper())
            self.assertEqual(rules[root + ' .majoris-card']['background-color'], t['card'].upper())
            self.assertEqual(rules[root + ' .login-dialog-prompt-entry']['background-color'], t['field'].upper())
            for suffix in ['', ':hover', ':active', ':focus', ':insensitive']:
                self.assertIn(root + ' .majoris-primary' + suffix if suffix != ':focus' else root + ' StButton:focus', rules)
            self.assertEqual(rules[root + ' .majoris-primary StLabel']['color'], '#FFFFFF')
        self.assertEqual(len([k for k in rules if '.majoris-light' in k]), len([k for k in rules if '.majoris-dark' in k]))

    def test_resources(self):
        for file in ET.parse(ROOT / 'resources.gresource.xml').iter('file'):
            self.assertTrue((ROOT / file.text).is_file(), file.text)
        self.assertGreaterEqual(len(list((ROOT / 'assets/icons').glob('*.svg'))), 12)
        self.assertEqual(len(list((ROOT / 'assets/fonts/static').glob('*.ttf'))), 4)
        self.assertIn('SIL OPEN FONT LICENSE', (ROOT / 'assets/fonts/OFL.txt').read_text())

    def test_schema(self):
        with tempfile.TemporaryDirectory() as temporary:
            subprocess.run(['glib-compile-schemas', '--strict', '--dry-run', str(ROOT / 'config')], check=True)
        keys = {key.attrib['name']: key for key in ET.parse(ROOT / 'config/org.majoris.login.gschema.xml').iter('key')}
        self.assertEqual(keys['appearance'].find('default').text, "'dark'")
        config = (ROOT / 'config/20-majoris-login').read_text()
        for setting in ['disable-user-list', 'AutomaticLogin', 'disable-restart-buttons']:
            self.assertNotIn(setting, config)

    def test_native_ownership(self):
        patch = (ROOT / 'patches/gnome-shell-48.7/0001-majoris-login-presentation.patch').read_text()
        module = (ROOT / 'shell/majorisLogin.js').read_text()
        for forbidden in ['answerQuery(', 'new Gdm.Client', 'checkPassword', 'spawn_command_line', 'child_process', 'Alex Morgan', 'Jordan Lee']:
            self.assertNotIn(forbidden, module)
        for untouched in ['gdm/util.js', 'misc/loginManager.js', 'misc/systemActions.js']:
            self.assertNotIn('--- a/js/' + untouched, patch)
        self.assertIn('prompt._activateNext(', module)
        self.assertIn("'activateSuspend'", module)
        self.assertIn('MajorisLogin.syncSensitivity', patch)
        self.assertIn('password_visible = false', patch)
        self.assertIn('MajorisLogin.enabled() ? 0 : -global.screen_height', patch)
        self.assertNotIn('Main.popModal', module)
        self.assertNotIn('openSession', module)

    def test_version_fail_closed(self):
        spec = importlib.util.spec_from_file_location('prepare', ROOT / 'scripts/prepare-shell.py')
        prepare = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(prepare)
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary)
            (source / 'debian').mkdir()
            (source / 'debian/changelog').write_text('gnome-shell (49.0-1) unstable; urgency=medium\n\n  * Deliberate incompatible source\n\n -- Test <test@example.invalid>  Mon, 12 Oct 2026 10:00:00 +1100\n')
            with self.assertRaisesRegex(SystemExit, 'Unsupported Debian Shell source'):
                prepare.prepare(source, check_only=True)
            self.assertFalse((source / 'debian/patches').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
