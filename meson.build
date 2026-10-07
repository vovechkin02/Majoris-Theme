project('majoris-theme', ['c', 'vala'], version: '0.1.0', meson_version: '>=1.0', default_options: ['prefix=/usr'])
python = find_program('python3')
subdir('factory')
install_subdir('theme/Majoris', install_dir: get_option('datadir') / 'themes')
install_subdir('icons/Majoris', install_dir: get_option('datadir') / 'icons')
install_data('fonts/fontconfig/65-majoris-fonts.conf', install_dir: get_option('datadir') / 'fontconfig/conf.avail')
foreach name : ['design-tokens', 'css-selectors', 'theme-tree', 'installer']
  test(name, python, args: [files('tests/test-' + name + '.py')])
endforeach
test('Shell static grammar and Trixie selectors', python, args: [files('tools/validate-shell.py')])
foreach version : ['3', '4']
  test('GTK' + version + ' CSS parser', find_program('xvfb-run'), args: ['-a', python.full_path(), files('tools/validate-css.py'), version])
endforeach
test('native headerbar geometry', find_program('dbus-run-session'), args: ['--', find_program('xvfb-run').full_path(), '-a', python.full_path(), files('tests/test-geometry.py'), factory.full_path()], timeout: 30)
test('GTK3 realized widget styles', find_program('xvfb-run'), args: ['-a', python.full_path(), files('tests/test-gtk3-widgets.py')])
