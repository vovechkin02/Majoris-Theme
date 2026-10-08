/* Read-only allocation probe for optional real GTK4 applications. */
#include <gtk/gtk.h>
#include <stdio.h>
static void tree(GtkWidget *w, FILE *f, int depth) {
 char **classes=gtk_widget_get_css_classes(w);
 fprintf(f,"%*s%s css=%s size=%dx%d margin=%d,%d,%d,%d classes=",depth,"",G_OBJECT_TYPE_NAME(w),gtk_widget_get_css_name(w),gtk_widget_get_allocated_width(w),gtk_widget_get_allocated_height(w),gtk_widget_get_margin_top(w),gtk_widget_get_margin_bottom(w),gtk_widget_get_margin_start(w),gtk_widget_get_margin_end(w));
 for(int i=0;classes[i];i++)fprintf(f,"%s ",classes[i]);
 fprintf(f,"\n");g_strfreev(classes);
 for(GtkWidget*c=gtk_widget_get_first_child(w);c;c=gtk_widget_get_next_sibling(c))tree(c,f,depth+1);
}
static gboolean dump(gpointer unused) {
 const char *path=g_getenv("MAJORIS_APP_REPORT");if(!path)return G_SOURCE_REMOVE;
 GListModel *windows=gtk_window_get_toplevels();
 if(!g_list_model_get_n_items(windows))return G_SOURCE_CONTINUE;
 FILE *f=fopen(path,"w");if(!f)return G_SOURCE_REMOVE;
 for(guint i=0;i<g_list_model_get_n_items(windows);i++){GtkWidget*w=g_list_model_get_item(windows,i);tree(w,f,0);g_object_unref(w);}
 fclose(f);return G_SOURCE_REMOVE;
}
__attribute__((constructor)) static void setup(void){g_timeout_add_seconds(4,dump,NULL);}
