"""Native spacing inheritance and Files-derived hierarchy regressions (GTK4/Adw 1.7)."""
import ctypes,json,os,subprocess
from pathlib import Path
import gi
gi.require_version('Gtk','4.0');gi.require_version('Adw','1')
from gi.repository import Gtk,Adw,Gdk,GLib
ROOT=Path(__file__).resolve().parents[1]
variant=os.environ.get('MAJORIS_VARIANT','light');profile=os.environ.get('MAJORIS_SPACING_PROFILE','standard')
out=ROOT/'artifacts/layout-spacing'/variant/profile;out.mkdir(parents=True,exist_ok=True)
Adw.init();Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK if variant=='dark' else Adw.ColorScheme.FORCE_LIGHT)
os.environ['MAJORIS_THEME_ROOT']=str(ROOT/'theme/Majoris')
ctypes.CDLL(str(ROOT/'build/libmajoris-gtk4-theme.so')).majoris_theme_attach()
Gtk.Settings.get_default().set_property('gtk-enable-animations',False)
if profile=='large-font':Gtk.Settings.get_default().set_property('gtk-xft-dpi',144*1024)
if profile=='rtl':Gtk.Widget.set_default_direction(Gtk.TextDirection.RTL)
def settle():
 loop=GLib.MainLoop();GLib.timeout_add(120,lambda:(loop.quit(),False)[1]);loop.run()
def box(cls='',orientation=Gtk.Orientation.VERTICAL,spacing=0):
 b=Gtk.Box(orientation=orientation,spacing=spacing)
 if cls:b.add_css_class(cls)
 return b
def button(text):return Gtk.Button(label=text)
def children(w):
 c=w.get_first_child()
 while c:yield c;c=c.get_next_sibling()
def hierarchy(w):return dict(type=w.__class__.__name__,node=w.get_css_name(),classes=list(w.get_css_classes()),visible=w.get_visible(),spacing=w.get_spacing() if isinstance(w,Gtk.Box) else None,children=[hierarchy(c) for c in children(w)])
def bounds(w,parent):
 ok,r=w.compute_bounds(parent);assert ok
 return [r.get_x(),r.get_y(),r.get_width(),r.get_height()]
measurements=[]
def measure(name,a,b,target,axis='vertical'):
 p=a.get_parent();assert p==b.get_parent();aa=bounds(a,p);bb=bounds(b,p)
 gap=(bb[1]-aa[1]-aa[3]) if axis=='vertical' else (bb[0]-aa[0]-aa[2] if bb[0]>=aa[0] else aa[0]-bb[0]-bb[2])
 def margins(w):return dict(start=w.get_margin_start(),end=w.get_margin_end(),top=w.get_margin_top(),bottom=w.get_margin_bottom())
 record=dict(name=name,parent=p.__class__.__name__,node=p.get_css_name(),classes=list(p.get_css_classes()),first=a.__class__.__name__,second=b.__class__.__name__,first_allocation=aa,second_allocation=bb,gap=gap,target=target,axis=axis,explicit_spacing=p.get_spacing() if isinstance(p,Gtk.Box) else {'row':p.get_row_spacing(),'column':p.get_column_spacing()} if isinstance(p,(Gtk.Grid,Gtk.FlowBox)) else None,first_margins=margins(a),second_margins=margins(b),padding=[getattr(p.get_style_context().get_padding(),k) for k in ('top','right','bottom','left')],border=[getattr(p.get_style_context().get_border(),k) for k in ('top','right','bottom','left')])
 measurements.append(record);assert abs(gap-target)<=1,record
w=Adw.Window(title='Majoris layout spacing',default_width=320 if profile=='narrow' else 760 if profile=='wide' else 420,default_height=820)
scroll=Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER);w.set_content(scroll)
page=Adw.PreferencesPage();scroll.set_child(page)
g=Adw.PreferencesGroup(title='Tags assignment');page.add(g)
search=Gtk.SearchEntry();lst=Gtk.ListBox();lst.add_css_class('boxed-list')
for name in ('Documents','Work'):lst.append(Adw.ActionRow(title=name))
editor=box(spacing=4);editor.append(Gtk.Entry(placeholder_text='Tag name'));editor.append(Gtk.Label(label='Validation message'));editor.set_visible(False)
actions=box(orientation=Gtk.Orientation.HORIZONTAL,spacing=8);actions.append(button('New Tag'));actions.append(button('Manage Tags'))
for child in (search,lst,editor,actions):g.add(child)
manage=Adw.PreferencesGroup(title='Manage Tags');page.add(manage)
ml=Gtk.ListBox();ml.add_css_class('boxed-list');ml.append(Adw.ActionRow(title='Work'))
ma=box(orientation=Gtk.Orientation.HORIZONTAL,spacing=8);ma.append(button('Rename'));ma.append(button('Delete'));manage.add(ml);manage.add(ma)
fixtures=[]
for cls,target in [('majoris-control-stack',8),('majoris-compact-stack',4),('majoris-section-stack',16),('majoris-major-stack',32),('majoris-connected-group',0),('majoris-action-group',8)]:
 b=box(cls,orientation=Gtk.Orientation.HORIZONTAL if cls in ('majoris-connected-group','majoris-action-group') else Gtk.Orientation.VERTICAL)
 a=button('First');c=button('Second');b.append(a);b.append(c)
 group=Adw.PreferencesGroup(title=cls);group.add(b);page.add(group);fixtures.append((cls,b,a,c,target))
w.present();settle()
# First screenshot captures the real Tags relevant hierarchy at its existing width.
wid=subprocess.check_output(['xdotool','search','--name','^Majoris layout spacing$'],text=True).splitlines()[-1]
def capture(name):
 p=out/(name+'.xwd');subprocess.run(['xwd','-silent','-id',wid,'-out',str(p)],check=True);subprocess.run(['magick',str(p),str(p.with_suffix('.png'))],check=True);p.unlink()
# Before: remove only the newly added PreferencesGroup content default above the bridge provider.
before=Gtk.CssProvider();before.load_from_data(b'preferencesgroup > box > box:not(.header) { border-spacing: 0; }')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),before,Gtk.STYLE_PROVIDER_PRIORITY_USER+2);settle();capture('tags-before')
Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),before);settle();capture('tags-after')
measure('search-list',search,lst,8);measure('list-actions-hidden-editor',lst,actions,8);measure('manage-list-actions',ml,ma,8)
measure('tags-buttons',actions.get_first_child(),actions.get_last_child(),8,'horizontal')
editor.set_visible(True);settle();measure('list-editor',lst,editor,8);measure('editor-actions',editor,actions,8);capture('tags-editor-visible')
editor.set_visible(False);settle();measure('hide-editor-again',lst,actions,8)
extra=button('Dynamic');g.add(extra);settle();measure('insert',actions,extra,8);g.remove(extra);settle();measure('remove',lst,actions,8)
for cls,b,a,c,target in fixtures:measure(cls,a,c,target,'horizontal' if b.get_orientation()==Gtk.Orientation.HORIZONTAL else 'vertical')
# GtkBox adds explicit spacing to CSS: document and measure this limitation.
b,a,c=fixtures[0][1:4]
for explicit,target in [(6,14),(8,16),(12,20)]:b.set_spacing(explicit);settle();measure('explicit-'+str(explicit),a,c,target)
b.set_spacing(0);c.set_margin_top(3);settle();measure('child-margin-is-additive',a,c,11);c.set_margin_top(0)
override=Gtk.CssProvider();override.load_from_data(b'box.majoris-control-stack { border-spacing: 4px; }');Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),override,Gtk.STYLE_PROVIDER_PRIORITY_USER+2);settle();measure('application-provider-override',a,c,4);Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),override)
# Boxed ActionRows have only their existing 1px separator, never the new 8px gap.
settle();measure('continuous-rows',lst.get_first_child(),lst.get_last_child(),0)
# Measure page group gap in page coordinates.
measure('page-groups',g,manage,16)
# Generic popover direct content; GtkPopoverMenu remains a separate scrolled hierarchy.
pop=Gtk.Popover();pb=box('majoris-control-stack');pa=Gtk.SearchEntry();pc=button('Search results');pb.append(pa);pb.append(pc);pop.set_child(pb)
anchor=Gtk.MenuButton(label='Popover');anchor.set_popover(pop);ma.append(anchor);pop.popup();settle();measure('popover-content',pa,pc,8);capture('popover-content');pb.remove_css_class('majoris-control-stack');pb.set_spacing(8);settle();measure('popover-explicit-spacing-preserved',pa,pc,8);pop.popdown()
# Native actionbar is identifiable; inner start/end boxes have zero explicit spacing.
ab=Gtk.ActionBar();ab1=button('Apply');ab2=button('Reset');ab.pack_start(ab1);ab.pack_start(ab2);g.add(ab);settle();measure('native-actionbar',ab1,ab2,8,'horizontal')
# Semantic progress: 8px title/detail, 4px bar/support, 16px content/footer.
progress=box('majoris-progress-content');title=Gtk.Label(label='Copying files');detail=box('majoris-progress-detail');bar=Gtk.ProgressBar(fraction=.5);support=Gtk.Label(label='6 of 12 files');detail.append(bar);detail.append(support);progress.append(title);progress.append(detail)
footer=box('majoris-footer-layout');footer.append(progress);fa=box('majoris-action-footer',Gtk.Orientation.HORIZONTAL);f1=button('Pause');f2=button('Cancel');fa.append(f1);fa.append(f2);footer.append(fa);g.add(footer);settle();measure('progress-title-detail',title,detail,8);measure('progress-support',bar,support,4);measure('content-footer',progress,fa,16);measure('footer-buttons',f1,f2,8,'horizontal')
# Files Split and Sharing both mix an internal preference-row list with standalone actions.
files_groups=[]
for label in ('Split File','Sharing settings'):
 fg=Adw.PreferencesGroup(title=label);page.add(fg);files_groups.append((label,fg))
 fr=Adw.ActionRow(title='Destination' if label=='Split File' else 'Sharing state');fg.add(fr)
 fr2=Adw.SwitchRow(title='Manifest' if label=='Split File' else 'Enabled');fg.add(fr2)
 fb=button('Split File' if label=='Split File' else 'Reload Sharing State');fg.add(fb);settle()
 measure(label+'-rows-action',fr.get_parent(),fb,8);measure(label+'-continuous-rows',fr,fr2,0)
# A zero-property form field separates its label and input without global label margins.
field=box('majoris-field');fl=Gtk.Label(label='Name');fi=Gtk.Entry();field.append(fl);field.append(fi);g.add(field);settle();measure('form-label-input',fl,fi,4)
# Explicitly marked form Grid and neutral FlowBox retain native layout managers.
grid=Gtk.Grid();grid.add_css_class('majoris-form-layout');ga=button('Grid A');gb=button('Grid B');gc=button('Grid C');grid.attach(ga,0,0,1,1);grid.attach(gb,1,0,1,1);grid.attach(gc,0,1,1,1);g.add(grid);settle();measure('form-grid-columns',ga,gb,8,'horizontal');measure('form-grid-rows',ga,gc,8)
flow=Gtk.FlowBox(selection_mode=Gtk.SelectionMode.NONE,min_children_per_line=2,max_children_per_line=2);flow.append(button('Flow A'));flow.append(button('Flow B'));g.add(flow);probe=Gtk.CssProvider();probe.load_from_data(b'flowbox.spacing-probe { border-spacing: 8px; }');flow.add_css_class('spacing-probe');Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),probe,Gtk.STYLE_PROVIDER_PRIORITY_USER+2);settle();measure('flow-css-spacing-unsupported',flow.get_first_child(),flow.get_last_child(),0,'horizontal');Gtk.StyleContext.remove_provider_for_display(Gdk.Display.get_default(),probe);flow.remove_css_class('spacing-probe');flow.set_row_spacing(8);flow.set_column_spacing(8);settle();measure('neutral-flow-columns',flow.get_first_child(),flow.get_last_child(),8,'horizontal')
# Screenshot actual native composed regions by scrolling the native PreferencesPage.
def capture_at(widget,name):
 ok,rect=widget.compute_bounds(page);assert ok
 # PreferencesPage owns its own native scrolledwindow.
 page_scroll=page.get_first_child();page_scroll.get_vadjustment().set_value(rect.get_y());settle();capture(name)
for cls,b,a,c,target in fixtures:capture_at(b,cls)
for label,fg in files_groups:capture_at(fg,label.lower().replace(' ','-')+'-after')
for widget,name in ((manage,'manage-tags-after'),(footer,'dialog-footer'),(progress,'progress-content'),(g,'preferences-content'),(field,'form-field')):capture_at(widget,name)
# Single/empty containers retain no child-driven gap; RTL and resizing run through same assertions.
empty=box('majoris-control-stack');single=box('majoris-control-stack');single.append(button('Only child'));g.add(empty);g.add(single);settle()
# Long text uses natural wrapping at each responsive width.
long_group=Adw.PreferencesGroup(title='Long text');page.add(long_group);long_label=Gtk.Label(label='An explanatory description should wrap naturally while controls remain usable. '*4,wrap=True,xalign=0);long_group.add(long_label);long_group.add(Gtk.Entry());settle();measure('long-text-input',long_label,long_label.get_next_sibling(),8)
# A visible empty Box still participates in GTK layout; hiding it removes its gap.
es=box('majoris-control-stack');e1=button('First');e0=box();e2=button('Second');es.append(e1);es.append(e0);es.append(e2);g.add(es);settle();measure('visible-empty-native-participation',e1,e2,16);e0.set_visible(False);settle();measure('hidden-empty-no-reserved-gap',e1,e2,8)
single_bounds=bounds(single.get_first_child(),single);assert single_bounds[1]==0 and single_bounds[3]==single.get_allocated_height(),single_bounds
hierarchies={'tags':hierarchy(g),'page':hierarchy(page),'popover':hierarchy(pop),'menu':hierarchy(Gtk.PopoverMenu()),'searchbar':hierarchy(Gtk.SearchBar()),'actionbar':hierarchy(Gtk.ActionBar()),'flowbox':hierarchy(Gtk.FlowBox())}
# Map native dialog structures before recording them: libadwaita creates sheets lazily.
pd=Adw.PreferencesDialog();pp=Adw.PreferencesPage();pg=Adw.PreferencesGroup(title='Native dialog group');pg.add(Gtk.SearchEntry());pg.add(button('Action'));pp.add(pg);pd.add(pp);pd.present(w);settle();hierarchies['preferences-dialog']=hierarchy(pd);pd.close();settle()
ad=Adw.AlertDialog(heading='Heading',body='Body');ad.add_response('ok','OK');ad.present(w);settle();hierarchies['adw-alert-dialog']=hierarchy(ad);ad.close();settle()
gd=Gtk.Dialog(title='Native dialog',transient_for=w);gd.get_content_area().append(Gtk.Entry());gd1=gd.add_button('Cancel',Gtk.ResponseType.CANCEL);gd2=gd.add_button('Apply',Gtk.ResponseType.OK);gd.present();settle();dv=gd.get_first_child();measure('native-dialog-body-footer',dv.get_first_child(),dv.get_last_child(),16);measure('native-dialog-buttons',gd1,gd2,8,'horizontal');hierarchies['gtk-dialog']=hierarchy(gd);gd.close()
hierarchies['navigation-page']=hierarchy(Adw.NavigationPage.new(Gtk.Label(label='Content'),'Page'))
hierarchies['toolbar-view']=hierarchy(Adw.ToolbarView())
(out/'spacing-measurements.json').write_text(json.dumps(measurements,indent=2))
(out/'container-hierarchies.json').write_text(json.dumps(hierarchies,indent=2))
(out/'regression-results.json').write_text(json.dumps(dict(variant=variant,profile=profile,gtk=Gtk.get_major_version().__str__()+'.'+str(Gtk.get_minor_version()),adw=Adw.get_minor_version(),assertions=len(measurements),substitution='Files relevant native hierarchy, not Files executable'),indent=2))
w.close();print(f'{variant}/{profile}: {len(measurements)} native gap assertions passed')
