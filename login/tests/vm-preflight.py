#!/usr/bin/env python3
"""Read-only real-VM prerequisites. This does not certify login/unlock success."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
checks = {}
for name, command in {
    'packages': ['dpkg-query', '-W', '-f=${Package} ${Version}\n', 'gdm3', 'gnome-shell', 'gnome-shell-common', 'majoris-login-resources'],
    'gdm_active': ['systemctl', 'is-active', 'gdm3'],
    'font': ['fc-match', '-f', '%{family}\n', 'Plus Jakarta Sans'],
    'boot_id': ['cat', '/proc/sys/kernel/random/boot_id'],
}.items():
    result = subprocess.run(command, text=True, capture_output=True)
    checks[name] = {'exit_code': result.returncode, 'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}
checks['authentication_tested'] = False
checks['lock_security_tested'] = False
checks['vm_matrix_completed'] = False
args.output.write_text(json.dumps(checks, indent=2) + '\n')
print(args.output)
raise SystemExit(0 if all(checks[name]['exit_code'] == 0 for name in ['packages', 'gdm_active', 'font']) else 1)
