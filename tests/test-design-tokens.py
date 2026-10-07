import runpy
import sys
import subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools'))
runpy.run_path(str(root/'tools/verify-design-tokens.py'))
subprocess.run([sys.executable,str(root/'tools/generate-theme.py'),'--check'],check=True)
