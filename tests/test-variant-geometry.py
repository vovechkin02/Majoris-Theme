"""Realized geometry is invariant under the native colour scheme."""
import json,os,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for variant in ('light','dark'):
 subprocess.run([sys.executable,str(root/'tests/test-geometry.py'),sys.argv[1]],env={**os.environ,'MAJORIS_VARIANT':variant},check=True,stdout=subprocess.DEVNULL)
light=json.loads((root/'artifacts/geometry-light.json').read_text());dark=json.loads((root/'artifacts/geometry-dark.json').read_text())
assert light==dark,'Native allocations, CSS nodes or resolved font differ between variants'
print('Entire realized widget tree and geometry reports are identical in light/dark')
