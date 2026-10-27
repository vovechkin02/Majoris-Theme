"""Stage the actual library outputs and compile/run an independent Vala consumer."""
import os,sys,subprocess,tempfile,shlex
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='majoris-ui-package-') as directory:
 stage=Path(directory)
 subprocess.run(['meson','install','-C',str(root/'build'),'--no-rebuild','--destdir',str(stage)],check=True,stdout=subprocess.DEVNULL)
 pc=next(stage.rglob('majoris-ui-gtk4.pc'));header=next(stage.rglob('majoris-ui-gtk4.h'));vapi=next(stage.rglob('majoris-ui-gtk4.vapi'));library=next(stage.rglob('libmajoris-ui-gtk4.so'))
 assert (vapi.parent/'majoris-ui-gtk4.deps').read_text().strip()=='gtk4'
 # Relocate only the staged package's prefix; system GTK dependencies stay native.
 content=pc.read_text();content=content.replace('prefix=/usr\n','prefix='+str(stage/'usr')+'\n');pc.write_text(content)
 env={**os.environ,'PKG_CONFIG_PATH':str(pc.parent),'LD_LIBRARY_PATH':str(library.parent),'GTK_A11Y':'none','GTK_THEME':'Adwaita','XDG_CONFIG_HOME':str(stage/'empty-config')}
 flags=subprocess.check_output(['pkg-config','--cflags','--libs','majoris-ui-gtk4'],env=env,text=True)
 assert str(header.parent) in flags and str(library.parent) in flags,flags
 consumer=stage/'consumer';source=root/'tests/toolbar-api.vala'
 command=['valac',str(source),'--vapidir='+str(vapi.parent),'--pkg','majoris-ui-gtk4','-o',str(consumer)]
 for flag in shlex.split(flags):command+=['-X',flag]
 subprocess.run(command,env=env,check=True,capture_output=True,text=True)
 subprocess.run(['dbus-run-session','--','xvfb-run','-a',str(consumer)],env=env,check=True,timeout=15)
print('Staged header, VAPI, deps, pkg-config, library and external no-theme consumer passed')
