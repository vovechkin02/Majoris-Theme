# Typography

Majoris requires **Plus Jakarta Sans**, followed by Noto Sans, Cantarell and sans-serif only when unavailable. No font files were supplied. Put properly licensed Plus Jakarta Sans files and their license in `fonts/PlusJakartaSans/`; development installation links that directory and refreshes fontconfig.

Check `fc-match "Plus Jakarta Sans"` and `fc-scan fonts/PlusJakartaSans/*`. On the tested Trixie system, fc-match returns Cantarell: exact typography cannot be certified. The fontconfig rule installs locally during development; production installation places it in `/usr/share/fontconfig/conf.avail` for the distribution to enable.
