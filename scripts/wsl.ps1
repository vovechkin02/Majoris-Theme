param([ValidateSet('bootstrap','build','test','install','uninstall','factory','inspector')][string]$Action='build')
$ErrorActionPreference='Stop'
$repo=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$linuxPath=(& wsl -d debian -- wslpath -a $repo.Replace('\','/')).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot access Debian WSL' }
function Quote-Bash([string]$value) {
  if ($value.Contains([char]39)) { throw 'Apostrophes in workspace paths are unsupported' }
  return ([string][char]39) + $value + ([string][char]39)
}
$source=Quote-Bash $linuxPath
# Synchronize source, preserving the Linux build tree and excluding Windows Git metadata.
$sync="set -euo pipefail; mkdir -p ~/src/Majoris-Theme; cd $source; tar --exclude=.git --exclude=build --exclude=artifacts --exclude=__pycache__ -cf - . | tar -xf - -C ~/src/Majoris-Theme; cd ~/src/Majoris-Theme; chmod +x scripts/*.sh; "
$command=switch ($Action) {
  bootstrap {'./scripts/bootstrap-debian.sh'}
  build {'if [ ! -f build/build.ninja ]; then meson setup build; fi; meson compile -C build'}
  test {'./scripts/test.sh'}
  install {'./scripts/install-dev.sh'}
  uninstall {'./scripts/uninstall-dev.sh'}
  factory {'./scripts/run-factory.sh'}
  inspector {'./scripts/run-inspector.sh'}
}
& wsl -d debian -- bash -lc ($sync+$command)
exit $LASTEXITCODE
