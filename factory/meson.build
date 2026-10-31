factory = executable('majoris-theme-factory',
  'src/switches.vala', 'src/toolbars.vala', 'src/data-views.vala', 'src/sidebar-fixture.vala', 'src/menu-row.vala', 'src/location-bar.vala', 'src/editor-fixture.vala', 'src/main.vala', 'src/application.vala', 'src/window.vala', 'src/factory-page.vala', 'src/headerbar-tests.vala', 'src/geometry-report.vala', 'src/visual-states.vala', 'src/window-edge.vala',
  link_with: theme_bridge,
  dependencies: [majoris_ui_dep, dependency('gtksourceview-5', version: '>=5.16'), dependency('gtk4', version: '>=4.18'), dependency('libadwaita-1', version: '>=1.7')], install: true)
install_data('data/com.majoris.ThemeFactory.desktop.in', rename: 'com.majoris.ThemeFactory.desktop', install_dir: get_option('datadir') / 'applications')
install_data('data/com.majoris.ThemeFactory.metainfo.xml.in', rename: 'com.majoris.ThemeFactory.metainfo.xml', install_dir: get_option('datadir') / 'metainfo')

install_subdir('data/thumbnails',install_dir:get_option('datadir') / 'majoris-theme')
