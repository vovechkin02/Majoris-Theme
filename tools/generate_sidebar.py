"""Version-aware fixed-inset indicators; geometry and colours stay HTML-owned."""
from design import html_value

def sidebar_values(tokens,variant,version):
    inset=html_value(tokens,'.nav.active:before','top')
    focus='@focus_color' if variant=='dark' else '@primary_500'
    result={'sidebar_focus':focus,'sidebar_selected_text':('@primary_700' if variant=='light' else html_value(tokens,'.nav.active','color'))}
    for name,role,selector in [('sidebar_indicator_image','selected','.nav.active'),('sidebar_indicator_hover','hover','.nav.active:hover'),('sidebar_indicator_pressed','pressed','.nav.active:active')]:
        if version=='4':
            image=f'linear-gradient(to bottom, transparent {inset}, {focus} {inset}, {focus} calc(100% - {inset}), transparent calc(100% - {inset}))'
        else:
            # GTK3 has no calc(). Two opaque end caps mask a solid 2px stripe.
            # Alpha selection is composited over the semantic sidebar surface.
            value=html_value(tokens,selector,'background')
            if value.startswith('rgba'):
                alpha=value.rsplit(',',1)[1].rstrip(')')
                mask=f'mix(@majoris_sidebar_surface, @primary_500, {alpha})'
            else: mask='@majoris_sidebar_'+role
            image=f'linear-gradient(to bottom, {mask} {inset}, transparent {inset}), linear-gradient(to top, {mask} {inset}, transparent {inset}), linear-gradient(to bottom, {focus}, {focus})'
        result[name]=image
    return result
