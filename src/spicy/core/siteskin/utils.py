from django import http
from django.test.client import Client, FakePayload
from spicy.core.siteskin import defaults
from . import defaults


def get_render_from_response(request, url, get_forwarding=False):

    path, query = url, ''

    if '?' in url:
        path, query = url.split('?', 1)

    if request and request.GET:
        if query:
            query += '&'
        query += '&'.join([
            '%s=%s' % (key, values) for key, values in request.GET.items()])

    if request:
        meta = dict(request.META, PATH_INFO=path, QUERY_STRING=query)
        if not get_forwarding:
            meta = dict(request.META, PATH_INFO=path, QUERY_STRING='')
    else:
        meta = dict(PATH_INFO=path)
        # this is because django 1.3 now checking wsgi.input attribute in
        # request https://code.djangoproject.com/changeset/14453
        meta['wsgi.input'] = FakePayload('')  # XXX maybe not needed since 1.4?
    response = Client().request(**meta)

    if isinstance(response, http.HttpResponseRedirect):
        url = response['Location']
        host = request.get_host()
        if host in url:
            url = url.split(host)[1]
        else:
            raise http.HttpResponseBadRequest(
                'Cross domain includes not allowed! %s' % response['Location'])
        return get_render_from_response(
            request, url, get_forwarding=get_forwarding)

    return response.content.decode('utf-8')


def choose_render_method(request, url, get_forwarding=False):
    if not url:
        return '<!-- NO URL GIVEN -->'

    if defaults.USE_RENDER_FROM_RESPONSE_LIKE_SSI:
        return get_render_from_response(
            request, url, get_forwarding=get_forwarding)

    if '?' in url:
        path, get_params = url.split('?', 1)
    else:
        path, get_params = url, ''

    params_dict = {}
    if get_params:
        for item in get_params.split('&'):
            key, value = item.split('=', 1)
            params_dict[key] = value

    params_dict.update(request.GET.iteritems())
    params = params_dict.items()
    params.sort()
    params_str = '&'.join('='.join(item) for item in params)

    if get_forwarding and params_str:
        return u'<!--#include virtual="%s?%s" -->' % (path, params_str)
    return u'<!--#include virtual="%s" -->' % path
