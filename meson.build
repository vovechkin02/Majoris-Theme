project('majoris-theme', ['c', 'vala'], version: '0.1.0', meson_version: '>=1.0', default_options: ['prefix=/usr'])
python = find_program('python3')
# Theme tests do not require desktop portal services (absent in Xvfb/WSL).
add_test_setup('isolated', env: {'ADW_DISABLE_PORTAL': '1', 'GDK_BACKEND': 'x11'}, is_default: true)
theme_bridge = shared_library('majoris-gtk4-theme', 'integration/gtk4-theme-bridge.c', dependencies: [dependency('gtk4'), dependency('libadwaita-1')], install: true)
shared_library('majoris-gtk3-theme','integration/gtk3-theme-bridge.c',dependencies:[dependency('gtk+-3.0')],install:true)
install_data('scripts/with-majoris-gtk4.sh',rename:'majoris-gtk4',install_dir:get_option('bindir'),install_mode:'rwxr-xr-x')
install_data('scripts/with-majoris-gtk3.sh',rename:'majoris-gtk3',install_dir:get_option('bindir'),install_mode:'rwxr-xr-x')
subdir('factory')
install_subdir('theme/Majoris', install_dir: get_option('datadir') / 'themes')
install_subdir('theme/Majoris-Dark', install_dir: get_option('datadir') / 'themes')
install_subdir('icons/Majoris', install_dir: get_option('datadir') / 'icons')
install_data('fonts/fontconfig/65-majoris-fonts.conf', install_dir: get_option('datadir') / 'fontconfig/conf.avail')
foreach name : ['design-tokens', 'css-selectors', 'theme-tree', 'installer', 'shadow-contract', 'radius-contract', 'colour-contract', 'selector-contract', 'fontconfig', 'factory-coverage']
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
