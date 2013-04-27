from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

register = template.Library()

@register.filter
def activate(request_path):
    for path, index in settings.NAVIGATOR_MAP: 
        if request_path.startswith(path):
            return index
    return settings.DEFAULT_NAVIGATOR

@register.simple_tag
def nav_order_url(field, nav_filter):
    qd = nav_filter.querydict.copy()
    oldfield = nav_filter.field
    if field == oldfield:
        qd['order'] = 'asc' if nav_filter.order_q == 'desc' else 'desc'
    else:
        qd['order'] = 'asc'
    
    qd['field'] = field
    return '?' + qd.urlencode()

def mk_style(name):
    if name:
        return 'class="%s"'%name 
    return ''

@register.simple_tag
def nav_filter(title, field, value, nav_filter,  extra_style=''):
    request = nav_filter.request
    qd = nav_filter.querydict.copy()
    
    try: del qd['page']
    except KeyError: pass
    
    if qd.get(field) == value:
        del qd[field]
        url = request.path + '?' + qd.urlencode()
        return '<a href="%s" class="active">%s</a>'%(url, title)
    else:
        qd[field] = value
        url = request.path + '?' + qd.urlencode()
        return '<a href="%s" %s>%s</a>'%(url, mk_style(extra_style), title)

@register.simple_tag
def nav_filter_icon(field, nav_filter, style_down, style_up):
    if field == nav_filter.field:
        if nav_filter.order_q == 'desc':
            return '<span class="%s">'%(style_down)
        elif nav_filter.order_q == 'asc':
            return '<span class="%s">'%(style_up)
    return ''

