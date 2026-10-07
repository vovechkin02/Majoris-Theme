"""Native computed foreground colors (GTK4) and backgrounds (GTK3).

GTK4 does not expose computed box-shadow/radius; their separate contracts
and full-frame state screenshots are explicitly source/render checks.
"""
import sys,gi
from css_contract import ROOT,TOKENS
version=sys.argv[1];gi.require_version('Gtk',version+'.0')
from gi.repository import Gtk,GLib
if version=='4':
    gi.require_version('Adw','1');from gi.repository import Adw,Gdk
    Adw.init();window=Adw.Window()
else:
    from gi.repository import Gdk
    Gtk.init([]);window=Gtk.Window()
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
provider=Gtk.CssProvider();provider.load_from_path(str(ROOT/f'theme/Majoris/gtk-{version}.0/gtk.css'))
if version=='4':Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
else:Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
if version=='4':
    window.set_content(box);controls=Gtk.WindowControls(side=Gtk.PackType.END);controls.set_decoration_layout(':minimize,maximize,close');box.append(controls);window.present()
else:
    window.add(box);controls=Gtk.Box();box.pack_start(controls,False,False,0)
    for name in ('minimize','maximize','close'):
        b=Gtk.Button(label=name);b.get_style_context().add_class('titlebutton');b.get_style_context().add_class(name);controls.pack_start(b,False,False,0)
    window.show_all()
def settle():
    loop=GLib.MainLoop();GLib.timeout_add(150,lambda:(loop.quit(),False)[1]);loop.run()
settle()
buttons=[]
if version=='4':
    child=controls.get_first_child()
    while child:buttons.append(child);child=child.get_next_sibling()
else:buttons=controls.get_children()
assert len(buttons)==3
def rgb(color):return tuple(round(v*255) for v in (color.red,color.green,color.blue))
def expected(token):return tuple(bytes.fromhex(TOKENS['color'][token][1:]))
for b in buttons:
    close=b.has_css_class('close') if version=='4' else b.get_style_context().has_class('close')
    for state,color in [(Gtk.StateFlags.NORMAL,'text_secondary'),(Gtk.StateFlags.PRELIGHT,'surface' if close else 'text'),(Gtk.StateFlags.ACTIVE,'surface' if close else 'text'),(Gtk.StateFlags.BACKDROP,'text_tertiary')]:
        b.set_state_flags(state,True);settle()
        actual=b.get_style_context().get_color() if version=='4' else b.get_style_context().get_color(state)
        assert rgb(actual)==expected(color),(version,close,state,rgb(actual),expected(color))
        if version=='3' and state in (Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE):
            background=b.get_style_context().get_background_color(state)
            token=('danger' if state==Gtk.StateFlags.PRELIGHT else 'danger_pressed') if close else ('hover' if state==Gtk.StateFlags.PRELIGHT else 'active')
            assert rgb(background)==expected(token),(token,rgb(background))
if version=='3':
    import cairo
    for style,palette in [('',['surface','hover','active']),('suggested-action',['primary_600','primary_700','primary_800'])]:
        b=Gtk.Button(label='Native background probe')
        if style:b.get_style_context().add_class(style)
        box.pack_start(b,False,False,0);b.show();settle()
        for state,token in zip([Gtk.StateFlags.NORMAL,Gtk.StateFlags.PRELIGHT,Gtk.StateFlags.ACTIVE],palette):
            b.set_state_flags(state,True);settle()
            surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,32,32)
            Gtk.render_background(b.get_style_context(),cairo.Context(surface),0,0,32,32)
            surface.flush();pixel=bytes(surface.get_data()[16*surface.get_stride()+16*4:16*surface.get_stride()+16*4+4])
            actual=(pixel[2],pixel[1],pixel[0])
            assert actual==expected(token),(style,state,'rendered background',actual,expected(token))
window.destroy()
print('GTK'+version+' native titlebar foreground-state colors passed'+('; native backgrounds passed' if version=='3' else ''))
