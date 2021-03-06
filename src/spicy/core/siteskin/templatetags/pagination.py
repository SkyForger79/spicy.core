# -*- coding: utf-8 -*-
import urllib
from django import template
from spicy.core.siteskin import defaults


register = template.Library()


@register.inclusion_tag(
    defaults.SITESKIN + '/siteskin/pagination.html', takes_context=True)
def sk_pagination(context, style='default', neighbours=False):
    return _pagination(context, style='default', neighbours=False)


@register.inclusion_tag(
    'spicy.core.admin/admin/pagination.html', takes_context=True)
def pagination(context, style='default', neighbours=False):
    return _pagination(context, style, neighbours=False)


@register.inclusion_tag('pagination.html', takes_context=True)
def paginate(context, style='default', neighbours=False):
    return _pagination(context, style='default', neighbours=False)


def _pagination(context, style='default', neighbours=False):
    """
    Return the list of A tags with links to pages.
    """
    paginator = context['paginator']
    page_obj = paginator.current_page
    page_list = range(
        max(1, page_obj.number - defaults.PAGES_FROM_START),
        min(paginator.num_pages, page_obj.number + defaults.PAGES_TO_END) + 1)

    if not 1 in page_list:
        page_list.insert(0, 1)
        if not 2 in page_list:
            page_list.insert(1, '.')

    if not paginator.num_pages in page_list:
        if not paginator.num_pages - 1 in page_list:
            page_list.append('.')
        page_list.append(paginator.num_pages)

    get_params = ''

    try:
        request = context['request']
        requestpath = request.get_full_path()
        path, query = requestpath.split('?', 1)
        if '?page=' in '?' + query:
            get_params = ''
        elif '&page=' in query:
            get_params = query.split('&page=')[0].encode('utf-8')
        else:
            get_params = query.encode('utf-8')
    except Exception, e:
        print e

    if hasattr(paginator, 'base_url'):
        paginator_base_url = paginator.base_url
    else:
        paginator_base_url = ''
    base_url = paginator_base_url + (
        '?%s&' % get_params if get_params else '?')

    return {
        'base_url': base_url,
        'page_obj': page_obj,
        'page_list': page_list,
        'style': style,
        'paginator': paginator,
        'neighbours': neighbours
    }


@register.filter
def take(value, arg):
    return value[:arg]


@register.filter
def columns(data, cols):
    return [data[v:v + cols] for v in xrange(0, len(data), cols)]
