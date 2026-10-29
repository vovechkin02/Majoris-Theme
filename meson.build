project('majoris-theme', ['c', 'vala'], version: '0.1.0', meson_version: '>=1.0', default_options: ['prefix=/usr'])
python = find_program('python3')
# Theme tests do not require desktop portal services (absent in Xvfb/WSL).
add_test_setup('isolated', env: {'ADW_DISABLE_PORTAL': '1', 'GDK_BACKEND': 'x11'}, is_default: true)
theme_bridge = shared_library('majoris-gtk4-theme', 'integration/gtk4-theme-bridge.c', dependencies: [dependency('gtk4'), dependency('libadwaita-1')], install: true)
shared_library('majoris-gtk3-theme','integration/gtk3-theme-bridge.c',dependencies:[dependency('gtk+-3.0')],install:true)
install_data('scripts/with-majoris-gtk4.sh',rename:'majoris-gtk4',install_dir:get_option('bindir'),install_mode:'rwxr-xr-x')
install_data('scripts/with-majoris-gtk3.sh',rename:'majoris-gtk3',install_dir:get_option('bindir'),install_mode:'rwxr-xr-x')
subdir('ui')
subdir('factory')
install_subdir('theme/Majoris', install_dir: get_option('datadir') / 'themes')
install_data('theme/Majoris/gtksourceview-5/styles/majoris-light.xml', 'theme/Majoris/gtksourceview-5/styles/majoris-dark.xml', install_dir: get_option('datadir') / 'gtksourceview-5/styles')
install_data('design/sourceview/majoris-light.xml.in', 'design/sourceview/majoris-dark.xml.in', 'design/editor-tokens.json', install_dir: get_option('datadir') / 'majoris-theme/design/sourceview')
install_subdir('theme/Majoris-Dark', install_dir: get_option('datadir') / 'themes')
install_subdir('icons/Majoris', install_dir: get_option('datadir') / 'icons')
install_data('fonts/fontconfig/65-majoris-fonts.conf', install_dir: get_option('datadir') / 'fontconfig/conf.avail')
foreach name : ['design-tokens', 'css-selectors', 'theme-tree', 'installer', 'shadow-contract', 'radius-contract', 'colour-contract', 'selector-contract', 'fontconfig', 'factory-coverage', 'layout-contract']
  test(name, python, args: [files('tests/test-' + name + '.py')])
endforeach
test('exact font runtime mapping',python,args:[files('tests/test-fontconfig.py'),'--runtime'])
test('Shell static grammar and Trixie selectors', python, args: [files('tools/validate-shell.py')])
foreach version : ['3', '4']
  test('GTK' + version + ' CSS parser', find_program('xvfb-run'), args: ['-a', python.full_path(), files('tools/validate-css.py'), version])
  test('GTK' + version + ' native state colours',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-native-state-colours.py'),version])
endforeach
test('native headerbar geometry', find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', python.full_path(), files('tests/test-geometry.py'), factory.full_path()], timeout: 30)
test('GTK3 realized widget styles', find_program('xvfb-run'), args: ['-a', python.full_path(), files('tests/test-gtk3-widgets.py')])

foreach name : ['dark-contract', 'dark-contrast']
  test(name, python, args: [files('tests/test-' + name + '.py')])
endforeach
foreach version : ['3','4']
  test('GTK'+version+' rendered dark spinner',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-spinner-assets.py'),version])
  test('GTK' + version + ' dark native state colours', find_program('dbus-run-session'), args: ['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-native-state-colours.py'),version], env: {'MAJORIS_VARIANT':'dark'})
endforeach
test('variant geometry equality',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-variant-geometry.py'),factory.full_path()],timeout:45)
test('native GTK4 live and system switching',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-variant-switching.py')],env:{'GSETTINGS_BACKEND':'memory','XDG_CURRENT_DESKTOP':'GNOME'})
test('GTK3 native variant selection',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-gtk3-variant-selection.py')])
test('Dark Shell static grammar and Trixie selectors',python,args:[files('tools/validate-shell.py')],env:{'MAJORIS_VARIANT':'dark'})

test('window edge contract',python,args:[files('tests/test_window_edge_contract.py')])

foreach version : ['3','4']
  test('GTK'+version+' checkbox states',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-checkbox-states.py'),version])
endforeach

test('native window edge states',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 1440x1080x24',python.full_path(),files('tests/test-window-edge-runtime.py'),factory.full_path()],timeout:60)

foreach name : ['desktop-window-contract', 'shell-variant-contract']
  test(name,python,args:[files('tests/test-'+name+'.py')])
endforeach
foreach version : ['3','4']
  test('GTK'+version+' native desktop transparency',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-desktop-window-native.py'),version])
endforeach

test('neutral auto install with native GTK4 bridge',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-auto-install-bridge.py')])

test('Majoris Login source and resource contracts',python,args:[files('login/tests/test-contracts.py')])

test('native shared layout',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-layout-native.py')],timeout:30)

test('editor component contracts',python,args:[files('tests/test-editor-contract.py')])
test('SourceView schemes and reversible discovery',python,args:[files('tests/test-sourceview.py')])
test('native editor components',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-editor-native.py')],timeout:30)
test('editor staged packaging',python,args:[files('tests/test-editor-package.py')],timeout:30)
test('native editor components at 200 percent',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 2880x2160x24',python.full_path(),files('tests/test-editor-native.py')],env:{'GDK_SCALE':'2'},timeout:30)

location_test = executable('location-native-test', 'tests/location-native.vala', 'factory/src/location-bar.vala',
  link_with: theme_bridge, dependencies: [majoris_ui_dep, dependency('gtk4'), dependency('libadwaita-1')])
test('location component contract', python, args: [files('tests/test-location-contract.py')])
test('native location interactions', find_program('dbus-run-session'),
  args: ['--', find_program('xvfb-run').full_path(), '-a', location_test.full_path()],
  env: {'MAJORIS_THEME_ROOT': meson.project_source_root() / 'theme/Majoris', 'GTK_A11Y': 'none', 'GDK_BACKEND': 'x11'}, timeout: 30)

foreach menu_version : ['3', '4']
  foreach menu_scale : ['1', '2']
    foreach menu_variant : ['light', 'dark']
      test('native menu GTK' + menu_version + ' ' + menu_variant + ' scale ' + menu_scale,
        find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-menu-native.py'), menu_version],
        env: {'GDK_SCALE': menu_scale, 'MAJORIS_VARIANT': menu_variant, 'GDK_BACKEND': 'x11', 'GTK_A11Y': 'none'}, timeout: 30)
    endforeach
  endforeach
endforeach

test('menu source contract', python, args: [files('tests/test-menu-contract.py')])

install_data('factory/src/menu-row.vala', 'integration/menu_rows.py', install_dir: get_option('datadir') / 'majoris-theme/integration')

foreach tab_version : ['3', '4']
  foreach tab_scale : ['1', '2']
    foreach tab_variant : ['light', 'dark']
      test('tab system GTK' + tab_version + ' ' + tab_variant + ' scale ' + tab_scale,
        find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-tabs-native.py'), tab_version],
        env: {'GDK_SCALE': tab_scale, 'MAJORIS_VARIANT': tab_variant, 'GDK_BACKEND': 'x11', 'GTK_A11Y': 'none'}, timeout: 45)
    endforeach
  endforeach
endforeach

foreach tab_variant : ['light', 'dark']
  test('tab system 125 percent text ' + tab_variant,
    find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-tabs-native.py'), '4'],
    env: {'GDK_DPI_SCALE': '1.25', 'MAJORIS_TAB_TEXT_SCALE': '1.25', 'MAJORIS_VARIANT': tab_variant, 'GDK_BACKEND': 'x11', 'GTK_A11Y': 'none'}, timeout: 45)
endforeach

test('sidebar contracts',python,args:[files('tests/test-sidebar-contract.py')])
foreach version : ['3','4']
  foreach scale : ['1','2']
    test('GTK'+version+' native sidebar '+scale+'x',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 2880x2160x24',python.full_path(),files('tests/test-sidebar-native.py'),version],env:{'GDK_SCALE':scale,'GSK_RENDERER':'cairo','GTK_A11Y':'none','GIO_USE_VFS':'local'},timeout:60)
  endforeach
endforeach
test('native sidebar input and adaptation',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 1440x1080x24',python.full_path(),files('tests/test-sidebar-interaction.py')],timeout:45)

foreach version : ['3','4']
  foreach scale : ['1','2']
    test('GTK'+version+' sidebar initial padding '+scale+'x',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',python.full_path(),files('tests/test-sidebar-padding.py'),version],env:{'GDK_SCALE':scale,'GSK_RENDERER':'cairo','GTK_A11Y':'none','GIO_USE_VFS':'local','ADW_DISABLE_PORTAL':'1'},timeout:30)
  endforeach
endforeach

test('data view source contracts',python,args:[files('tests/test-data-view-contract.py')])
foreach scale : ['1','2']
  test('data view GTK4 native '+scale+'x',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 2880x2160x24',python.full_path(),files('tests/test-data-view-native.py')],env:{'GDK_SCALE':scale,'GSK_RENDERER':'cairo','GTK_A11Y':'none','GIO_USE_VFS':'local'},timeout:90)
  test('data view GTK3 native '+scale+'x',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 2880x2160x24',python.full_path(),files('tests/test-data-view-gtk3.py')],env:{'GDK_SCALE':scale,'GTK_A11Y':'none','GIO_USE_VFS':'local'},timeout:60)
endforeach
test('data view native interactions',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 1440x1080x24',python.full_path(),files('tests/test-data-view-interaction.py')],env:{'GIO_USE_VFS':'local','GTK_A11Y':'none'},timeout:90)

test('data view native states',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 1440x1080x24',python.full_path(),files('tests/test-data-view-state.py')],env:{'GIO_USE_VFS':'local','GTK_A11Y':'none'},timeout:180)

# Genuine native input and Pango measurements; screenshots are local test artifacts.
foreach scale : ['1', '2']
  foreach subject : ['focus', 'metadata']
    test('data view ' + subject + ' validation ' + scale + 'x', find_program('dbus-run-session'),
      args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-data-view-' + subject + '.py')],
      env: {'GDK_SCALE': scale, 'GDK_BACKEND': 'x11', 'GSK_RENDERER': 'cairo', 'GTK_A11Y': 'none', 'GIO_USE_VFS': 'local'}, timeout: 150)
  endforeach
endforeach

foreach toolbar_version : ['3', '4']
  foreach toolbar_scale : ['1', '2']
    foreach toolbar_variant : ['light', 'dark']
      test('toolbar system GTK' + toolbar_version + ' ' + toolbar_variant + ' scale ' + toolbar_scale,
        find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-toolbar-native.py'), toolbar_version],
        env: {'GDK_SCALE': toolbar_scale, 'MAJORIS_VARIANT': toolbar_variant, 'GDK_BACKEND': 'x11', 'GTK_A11Y': 'none'}, timeout: 45)
    endforeach
  endforeach
endforeach

test('toolbar component contract', python, args: [files('tests/test-toolbar-contract.py')])

# A GTK4-only client of the installed reusable component; no factory source linkage.
toolbar_api_test=executable('toolbar-api-test','tests/toolbar-api.vala',dependencies:majoris_ui_dep)
test('universal toolbar public API without theme',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a',toolbar_api_test.full_path()],env:{'GTK_A11Y':'none','GTK_THEME':'Adwaita','XDG_CONFIG_HOME':meson.project_build_root()/'no-toolbar-theme'},timeout:30)
test('universal toolbar staged external consumer',python,args:[files('tests/test-toolbar-package.py')],timeout:45)

polish_probe=executable('toolbar-polish-probe','tests/toolbar-polish.vala',dependencies:[majoris_ui_dep,dependency('libadwaita-1')],link_with:theme_bridge)
foreach scale : ['1','2']
  test('toolbar polish native '+scale+'x',find_program('dbus-run-session'),args:['--',find_program('xvfb-run').full_path(),'-a','-s','-screen 0 2880x2160x24',python.full_path(),files('tests/test-toolbar-polish.py')],env:{'GDK_SCALE':scale,'GIO_USE_VFS':'local','GTK_A11Y':'none'},timeout:90)
endforeach

foreach location_scale : ['1', '2']
  test('location standardisation native ' + location_scale + 'x', find_program('dbus-run-session'),
    args: ['--', find_program('xvfb-run').full_path(), '-a', '-s', '-screen 0 2880x2160x24', python.full_path(), files('tests/test-location-standardisation.py')],
    env: {'GDK_SCALE': location_scale, 'GDK_BACKEND': 'x11', 'GTK_A11Y': 'none', 'GIO_USE_VFS': 'local', 'ADW_DISABLE_PORTAL': '1'}, timeout: 150)
endforeach
