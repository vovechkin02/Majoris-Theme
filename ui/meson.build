gtk_ui = dependency('gtk4', version: '>=4.18')
majoris_ui = shared_library('majoris-ui-gtk4', 'toolbar.vala',
  dependencies: gtk_ui, version: meson.project_version(), soversion: '0',
  vala_header: 'majoris-ui-gtk4.h', vala_vapi: 'majoris-ui-gtk4.vapi', install: true,
  install_dir: [get_option('libdir'), get_option('includedir') / 'majoris-ui-gtk4', get_option('datadir') / 'vala/vapi'])
install_data('majoris-ui-gtk4.deps', install_dir: get_option('datadir') / 'vala/vapi')
pkgconfig = import('pkgconfig')
pkgconfig.generate(majoris_ui, name: 'Majoris UI GTK4', filebase: 'majoris-ui-gtk4',
  description: 'Reusable native Majoris Toolbar', subdirs: 'majoris-ui-gtk4', requires: 'gtk4 >= 4.18')
majoris_ui_dep = declare_dependency(link_with: majoris_ui, dependencies: gtk_ui,
  include_directories: include_directories('.'))
