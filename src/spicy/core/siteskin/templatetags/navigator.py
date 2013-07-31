from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from spicy import utils


register = template.Library()


@register.simple_tag
def nav_order_url(
        nav_filter_object, field, title, style_common='icon-sort',
        style_desc='icon-sort-down', style_asc='icon-sort-up'):
    """

    :param nav_filter_object: class
     ``spicy.core.siteskin.navigation.Navigation``
    :param field: Model field name used for filtering
    :param title: title
    :param style_common:
    :param style_desc:
    :param style_asc:
    """
    style = style_common
    qd = nav_filter_object.querydict.copy()
    oldfield = nav_filter_object.field

    if field == oldfield:
        qd['order'] = 'desc'
        style = style_desc

        if nav_filter_object.order_q == 'desc':
            qd['order'] = 'asc'
            style = style_asc
    else:
        qd['order'] = 'asc'

    qd['field'] = field
    return '<a href="?{0}" title="{1}">{1} <i class="{2}"></i></a>'.format(
        qd.urlencode(), unicode(title).encode('utf-8'), style)


@register.simple_tag
def nav_filter_url(nav_filter_object, field, value, title,   extra_style=''):
    """
    :param nav_filter_object: class
     ``spicy.core.siteskin.navigation.Navigation``
    :param field: Model field name used for filtering
    :param value: value for filtering
    :param title: title
    :param style_common:
    """

    request = nav_filter_object.request
    qd = nav_filter_object.querydict.copy()

    try:
        del qd['page']
    except KeyError:
        pass

    if qd.get(field) == value:
        del qd[field]
        url = request.path + '?' + qd.urlencode()
        return '<a href="{0}" class="active">{1}</a>'.format(
            url, unicode(title).encode('utf-8'))
    else:
        qd[field] = value
        url = request.path + '?' + qd.urlencode()
        return '<a href="%s" %s>%s</a>' % (
            url, utils.mk_style(extra_style), title)


# TODO refactoring

@register.filter
def activate(request_path):
    for path, index in settings.NAVIGATOR_MAP:
        if request_path.startswith(path):
            return index
    return settings.DEFAULT_NAVIGATOR


@register.simple_tag
def menu(
        request, url_path, title, li_style='', extra_style='', get='',
        url_params=''):

    if url_path:
        if url_params:
            url = reverse(url_path, args=str(url_params).split(','))
        else:
            url = reverse(url_path)
    else:
        url = request.path

    if get:
        url += '?' + get

    path = request.path + '?' + request.META['QUERY_STRING']
    if path.rstrip('?') == url:
        li_style = li_style + ' ' + 'activated'
        content = '<a href="%s" class="ui-corner-left">%s</a>' % (
            url, unicode(title))
    else:
        content = '<a href="%s" %s>%s</a>' % (
            url, utils.mk_style(extra_style), unicode(title))

    return '<li %(class)s>%(content)s</li>' % {
        'class': utils.mk_style(li_style), 'content': content}
