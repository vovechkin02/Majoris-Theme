#!/usr/bin/env python3
"""Prepare a matching, already Debian-patched source tree for dpkg-buildpackage.

Fail closed on version AND upstream file hashes. This is not a binary resource
replacement or an installed-file patcher. Run as an ordinary build user.
"""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def prepare(source, check_only=False):
    source = source.resolve()
    compatibility = json.loads((ROOT / 'patches/compatibility.json').read_text())
    version = subprocess.check_output(['dpkg-parsechangelog', '-SVersion'], cwd=source, text=True).strip()
    if version != compatibility['debian_source_version']:
        raise SystemExit(f'Unsupported Debian Shell source {version}; expected {compatibility["debian_source_version"]}. Revalidate patches before changing the pin.')
    for name, expected in compatibility['source_sha256'].items():
        actual = hashlib.sha256((source / name).read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f'Source mismatch: {name}; refusing dirty or incompatible source')
    if check_only:
        print('Exact source version and all patched module hashes verified')
        return
    if not shutil.which('quilt'):
        raise SystemExit('Install quilt before preparing the source tree')
    if not (source / '.pc/applied-patches').exists():
        raise SystemExit('Use dpkg-source -x first, with Debian patches applied')
    patch_dir = source / 'debian/patches/majoris'
    patch_dir.mkdir(exist_ok=True)
    hooks = 'majoris/0001-majoris-login-presentation.patch'
    shutil.copyfile(ROOT / 'patches/gnome-shell-48.7/0001-majoris-login-presentation.patch', source / 'debian/patches' / hooks)
    module = (ROOT / 'shell/majorisLogin.js').read_text()
    module_patch = ''.join(difflib.unified_diff([], module.splitlines(True), fromfile='/dev/null', tofile='b/js/gdm/majorisLogin.js'))
    (patch_dir / '0002-majoris-login-module.patch').write_text(module_patch)
    with (source / 'debian/patches/series').open('a') as series:
        series.write('\n' + hooks + '\nmajoris/0002-majoris-login-module.patch\n')
    environment = {**os.environ, 'QUILT_PATCHES': 'debian/patches'}
    subprocess.run(['quilt', 'push', '-a', '--fuzz=0'], cwd=source, env=environment, check=True)
    changelog = source / 'debian/changelog'
    date = subprocess.check_output(['date', '-R'], text=True).strip()
    entry = f'''gnome-shell ({version}+majoris1) trixie; urgency=medium

  * Add version-validated Majoris native greeter and lock presentation.
    Keep GDM/PAM, AccountsService and the modal screen shield unchanged.

 -- Majoris contributors <maintainers@majoris.invalid>  {date}

'''
    changelog.write_text(entry + changelog.read_text())
    # The two packages remain independent build products, with an explicit
    # runtime resource dependency on the custom Shell common package.
    control = source / 'debian/control'
    text = control.read_text()
    marker = 'Package: gnome-shell-common\n'
    assert marker in text
    start = text.index(marker)
    index = text.index('Depends:', start) + len('Depends:')
    text = text[:index] + ' majoris-login-resources (= 0.1.0),\n        ' + text[index:]
    control.write_text(text)
    print(f'Prepared gnome-shell {version}+majoris1; build normally with dpkg-buildpackage -us -uc')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    prepare(args.source, args.check)
