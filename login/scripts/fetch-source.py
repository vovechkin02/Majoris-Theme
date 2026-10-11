#!/usr/bin/env python3
"""Fetch the reviewed source archives and verify all pinned SHA-256s.

For release builds, use apt source acquisition from authenticated Debian Sources
indices (or dscverify with debian-keyring) in addition to these pins.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('destination', type=Path)
args = parser.parse_args()
pins = json.loads((ROOT / 'patches/compatibility.json').read_text())
args.destination.mkdir(parents=True, exist_ok=True)
for name, digest in pins['source_archives_sha256'].items():
    target = args.destination / name
    if not target.exists():
        request = urllib.request.Request(pins['source_url'] + name, headers={'User-Agent': 'Majoris-Login-source-builder/0.1'})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != digest:
            raise SystemExit(f'Source checksum mismatch: {name}')
        target.write_bytes(data)
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise SystemExit(f'Existing source checksum mismatch: {name}')
    print(f'Verified {name}')
