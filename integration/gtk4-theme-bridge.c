/* Generic GTK4/libadwaita theme integration. No widgets, colours or geometry here. */
#include <adwaita.h>
#include <glib/gstdio.h>
static GtkCssProvider *provider;
static AdwStyleManager *manager;
static char *theme_dir;
static void update_theme(void) {
    gboolean dark = adw_style_manager_get_dark(manager);
    char *path = g_build_filename(theme_dir, dark ? "gtk-dark.css" : "gtk.css", NULL);
    gtk_css_provider_load_from_path(provider, path);
    const char *report = g_getenv("MAJORIS_VARIANT_REPORT");
    if (report) {
        FILE *f = fopen(report, "a");
        if (f) { fprintf(f, "%s\n", dark ? "dark" : "light"); fclose(f); }
    }
    g_free(path);
}
static void changed(GObject *object, GParamSpec *property, gpointer data) { update_theme(); }
void majoris_theme_attach(void) {
    if (provider || !gdk_display_get_default()) return;
    const char *root = g_getenv("MAJORIS_THEME_ROOT");
    if (root) theme_dir = g_build_filename(root, "gtk-4.0", NULL);
    else {
        theme_dir = g_build_filename(g_get_user_data_dir(), "themes", "Majoris", "gtk-4.0", NULL);
        if (!g_file_test(theme_dir, G_FILE_TEST_IS_DIR)) {
            g_free(theme_dir); theme_dir = g_strdup("/usr/share/themes/Majoris/gtk-4.0");
        }
    }
    char *path = g_build_filename(theme_dir,"gtk-dark.css",NULL);
    gboolean exists = g_file_test(path,G_FILE_TEST_IS_REGULAR); g_free(path);
    if (!exists) { g_free(theme_dir); theme_dir = NULL; return; }
    manager = adw_style_manager_get_default();
    provider = gtk_css_provider_new();
    gtk_style_context_add_provider_for_display(gdk_display_get_default(), GTK_STYLE_PROVIDER(provider), GTK_STYLE_PROVIDER_PRIORITY_USER + 1);
    g_signal_connect(manager,"notify::dark",G_CALLBACK(changed),NULL);
    update_theme();
}
static gboolean ready(gpointer data) {
    if (!gdk_display_get_default()) return G_SOURCE_CONTINUE;
    majoris_theme_attach(); return G_SOURCE_REMOVE;
}
__attribute__((constructor)) static void preload_init(void) { g_timeout_add(50,ready,NULL); }
