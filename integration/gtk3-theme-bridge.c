/* GTK3 uses its native named-theme loader; this adapts GNOME system preference. */
#include <gtk/gtk.h>
static GSettings *desktop;
static void update_scheme(GSettings *settings, const char *key, gpointer data) {
    char *scheme=g_settings_get_string(settings,"color-scheme");
    g_object_set(gtk_settings_get_default(),"gtk-application-prefer-dark-theme",g_str_equal(scheme,"prefer-dark"),NULL);
    g_free(scheme);
}
static gboolean ready(gpointer data) {
    if (!gdk_display_get_default()) return G_SOURCE_CONTINUE;
    GSettingsSchemaSource *source=g_settings_schema_source_get_default();
    GSettingsSchema *schema=source ? g_settings_schema_source_lookup(source,"org.gnome.desktop.interface",TRUE) : NULL;
    if (!schema) return G_SOURCE_REMOVE;
    g_object_set(gtk_settings_get_default(),"gtk-theme-name","Majoris",NULL);
    desktop=g_settings_new_full(schema,NULL,NULL);g_settings_schema_unref(schema);
    g_signal_connect(desktop,"changed::color-scheme",G_CALLBACK(update_scheme),NULL);
    update_scheme(desktop,"color-scheme",NULL);
    return G_SOURCE_REMOVE;
}
__attribute__((constructor)) static void preload_init(void) { g_timeout_add(50,ready,NULL); }
