factory = executable('majoris-theme-factory',
  'src/main.vala', 'src/application.vala', 'src/window.vala', 'src/factory-page.vala', 'src/headerbar-tests.vala', 'src/geometry-report.vala', 'src/visual-states.vala',
  dependencies: [dependency('gtk4', version: '>=4.18'), dependency('libadwaita-1', version: '>=1.7')], install: true)
install_data('data/com.majoris.ThemeFactory.desktop.in', rename: 'com.majoris.ThemeFactory.desktop', install_dir: get_option('datadir') / 'applications')
install_data('data/com.majoris.ThemeFactory.metainfo.xml.in', rename: 'com.majoris.ThemeFactory.metainfo.xml', install_dir: get_option('datadir') / 'metainfo')
