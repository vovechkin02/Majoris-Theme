# Font aliases

Both `sans-serif` and `system-ui` use strong fontconfig aliases to Plus Jakarta Sans, then Noto Sans and Cantarell. The alias source is `fonts/fontconfig/65-majoris-fonts.conf`. Run `fc-cache -f` after development installation.

Plus Jakarta Sans is not bundled in the supplied theme assets or installed in this Debian environment. Obtain its licensed font files for final typography acceptance and place them under `fonts/PlusJakartaSans`; the development installer adds this directory when present, including on an existing installation. Run `fc-match sans-serif` and `fc-match system-ui`; the separate runtime Meson test must resolve both to Plus Jakarta Sans. It currently skips with exit 77, while static strong-alias checks pass.
