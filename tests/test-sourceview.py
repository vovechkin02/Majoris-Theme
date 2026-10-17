"""Schema validity and actual standard XDG discovery through reversible installation."""
import ctypes, ctypes.util, os, subprocess, sys, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
# Validate against the installed GtkSourceView Relax NG schema using its libxml2 dependency.
lib=ctypes.CDLL(ctypes.util.find_library('xml2'))
for name,args,restype in [('xmlRelaxNGNewParserCtxt',[ctypes.c_char_p],ctypes.c_void_p),('xmlRelaxNGParse',[ctypes.c_void_p],ctypes.c_void_p),('xmlRelaxNGNewValidCtxt',[ctypes.c_void_p],ctypes.c_void_p),('xmlReadFile',[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int],ctypes.c_void_p),('xmlRelaxNGValidateDoc',[ctypes.c_void_p,ctypes.c_void_p],ctypes.c_int)]:
 f=getattr(lib,name);f.argtypes=args;f.restype=restype
parser=lib.xmlRelaxNGNewParserCtxt(b'/usr/share/gtksourceview-5/styles/styles.rng')
schema=lib.xmlRelaxNGParse(parser);assert schema
context=lib.xmlRelaxNGNewValidCtxt(schema)
for variant in ('light','dark'):
 doc=lib.xmlReadFile(str(root/f'theme/Majoris/gtksourceview-5/styles/majoris-{variant}.xml').encode(),None,0)
 assert doc and lib.xmlRelaxNGValidateDoc(context,doc)==0
with tempfile.TemporaryDirectory(prefix='majoris-source-install-') as temp:
 env={**os.environ,'XDG_CONFIG_HOME':temp+'/config','XDG_DATA_HOME':temp+'/data','XDG_STATE_HOME':temp+'/state'}
 styles=Path(temp)/'data/gtksourceview-5/styles';styles.mkdir(parents=True)
 original=styles/'majoris-light.xml';original.write_text('original user scheme')
 personal='<style-scheme id="personal" name="Personal" version="1.0"/>'
 unrelated=styles/'personal.xml';unrelated.write_text(personal)
 command=[sys.executable,str(root/'tools/dev-install.py')]
 for mode in ('light','dark','auto'):
    subprocess.run(command+['install','--variant='+mode],env=env,check=True,capture_output=True)
 assert styles.is_dir() and not styles.is_symlink()
 assert original.is_symlink() and unrelated.read_text()==personal
 # Fresh process is necessary because default XDG search paths are initialized once.
 probe="""import gi;gi.require_version('GtkSource','5')
from gi.repository import GtkSource
m=GtkSource.StyleSchemeManager.get_default()
for id in ('majoris-light','majoris-dark'):
 s=m.get_scheme(id);assert s and s.get_style('def:keyword') and s.get_style('search-match'),id
 assert m.get_scheme_ids().count(id)==1
print('Both Majoris IDs discovered from standard XDG styles path')
"""
 subprocess.run([sys.executable,'-c',probe],env=env,check=True)
 original.unlink();original.write_text('user edit')
 for operation in ('install','uninstall'):
    result=subprocess.run(command+[operation],env=env,capture_output=True)
    assert result.returncode!=0 and original.read_text()=='user edit'
 original.unlink();original.symlink_to(root/'theme/Majoris/gtksourceview-5/styles/majoris-light.xml')
 subprocess.run(command+['uninstall'],env=env,check=True,capture_output=True)
 assert original.read_text()=='original user scheme' and not original.is_symlink()
 assert not (styles/'majoris-dark.xml').exists()
 assert unrelated.read_text()==personal
print('Source schemes: schema, XDG discovery, repeats, conflict rejection and restoration passed')
