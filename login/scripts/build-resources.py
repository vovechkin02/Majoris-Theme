#!/usr/bin/env python3
"""Build the independent architecture-all package with unmodified dpkg tooling."""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, default=ROOT.parent / 'artifacts/login-packages')
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='majoris-login-resources-') as temporary:
    source = Path(temporary) / 'majoris-login-resources-0.1.0'
    shutil.copytree(ROOT, source, symlinks=True)
    shutil.copytree(source / 'packaging/debian', source / 'debian')
    subprocess.run(['dpkg-buildpackage', '-us', '-uc', '-b'], cwd=source, check=True)
    for package in Path(temporary).glob('*'):
        if package.is_file():
            shutil.copy2(package, args.output / package.name)
