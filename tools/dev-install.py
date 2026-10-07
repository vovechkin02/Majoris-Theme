"""User-local reversible installation with an explicit journal and conflict checks."""
import json,os,sys,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
home=Path.home()
data=Path(os.environ.get('XDG_DATA_HOME',home/'.local/share'))
config=Path(os.environ.get('XDG_CONFIG_HOME',home/'.config'))
state=Path(os.environ.get('XDG_STATE_HOME',home/'.local/state'))/'majoris-theme'
journal=state/'install.json'
def present(p): return p.exists() or p.is_symlink()
def expected(p,target): return p.is_symlink() and os.readlink(p)==target
if sys.argv[1]=='install':
    previous=[]
    if journal.exists():
        previous=json.loads(journal.read_text())
        assert all(expected(Path(r['path']),r['target']) for r in previous),'Installation changed; restore or resolve conflicts first'
    state.mkdir(parents=True,exist_ok=True)
    pairs=[(data/'themes/Majoris',root/'theme/Majoris'),(data/'icons/Majoris',root/'icons/Majoris'),
           (config/'gtk-4.0/colors.css',root/'theme/Majoris/gtk-4.0/colors.css'),(config/'gtk-4.0/gtk.css',root/'theme/Majoris/gtk-4.0/gtk.css'),(config/'gtk-4.0/gtk-dark.css',root/'theme/Majoris/gtk-4.0/gtk-dark.css'),
           (config/'gtk-4.0/assets',root/'theme/Majoris/gtk-4.0/assets'),
           (config/'fontconfig/conf.d/65-majoris-fonts.conf',root/'fonts/fontconfig/65-majoris-fonts.conf')]
    if (root/'fonts/PlusJakartaSans').is_dir(): pairs.append((data/'fonts/PlusJakartaSans',root/'fonts/PlusJakartaSans'))
    installed={r['path'] for r in previous}
    pairs=[(path,target) for path,target in pairs if str(path) not in installed]
    if not pairs:print('Majoris development installation already active');sys.exit()
    records=previous.copy()
    for i,(path,target) in enumerate(pairs,start=len(previous)):
        path.parent.mkdir(parents=True,exist_ok=True)
        backup=state/('backup-'+str(i))
        assert not present(backup),'Unexpected backup: '+str(backup)
        records.append({'path':str(path),'target':str(target),'backup':str(backup) if present(path) else None})
    journal.write_text(json.dumps(records,indent=2)+'\n')
    try:
        for r in records[len(previous):]:
            path=Path(r['path'])
            if r['backup']: shutil.move(str(path),r['backup'])
            path.symlink_to(r['target'],target_is_directory=Path(r['target']).is_dir())
    except Exception:
        print('Partial installation: journal preserved for recovery',file=sys.stderr); raise
    print('Installed symlinks; previous files recorded in '+str(journal))
else:
    if not journal.exists(): print('No Majoris development installation'); sys.exit()
    records=json.loads(journal.read_text())
    conflicts=[r['path'] for r in records if present(Path(r['path'])) and not expected(Path(r['path']),r['target'])]
    assert not conflicts,'Refusing to overwrite changes made after installation: '+', '.join(conflicts)
    for r in reversed(records):
        path=Path(r['path'])
        if present(path): path.unlink()
        if r['backup'] and present(Path(r['backup'])): shutil.move(r['backup'],str(path))
    journal.unlink()
    print('Restored previous user files')
