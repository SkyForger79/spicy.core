import os
import urllib
from django import http
from django.conf import settings
from django.db import transaction
from django.test.client import Client, FakePayload
from spicy.utils.models import get_custom_model_class
from . import defaults


@transaction.commit_on_success
def get_siteskin_settings():
    # TODO make cache wrapper
    SiteskinModel = get_custom_model_class(defaults.SITESKIN_SETTINGS_MODEL)
    instance, _ = SiteskinModel.objects.get_or_create(site_id=settings.SITE_ID)
    return instance


def get_themes_from_path(path, version=None):
    """
    look in for ``spicy.theme`` file inside all subdirectories in the defined
    ``path``

    param path: abs path with spicy.* themes
    param version: hash key (revision key for product)

    spicy.ecom>=asdaLKJD823123kjsadSDaslkasd
    spicy.light==asdkasdlkj1231lkh23jkhadasd
    spicy.media<=asdkjalhskd1239123lkjadssda
    """
    themes = []
    try:
        #for theme in os.path.walk(path, get_theme_dir, None):
        for theme in os.listdir(path):
            theme_path = os.path.join(defaults.THEMES_PATH, theme)
            if os.path.isdir(theme_path):
                if defaults.SPICY_THEME_FILE in os.listdir(theme_path):
                    # TODO
                    # check theme version compatibility

                    themes.append((theme_path, theme))
    except OSError:
        pass

    return themes


def get_siteskin_themes():
    return get_themes_from_path(defaults.THEMES_PATH)


def get_render_from_response(request, url, get_forwarding=False):
    path, query = url, ''

    if '?' in url:
        path, query = url.split('?', 1)
        query = query.encode('utf-8')

    if request and request.GET:

        try:
            requestpath = request.get_full_path()
            path2, query2 = requestpath.split('?', 1)
            query2 = query2.encode('utf-8')
            if query:
                query += '&' + query2
            else:
                query = query2
        except:
            pass

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

    params_dict.update([
        (k.encode('utf-8'), v.encode('utf-8')) for (k, v) in
        request.GET.iteritems()])
    params_str = urllib.urlencode(params_dict)

    if get_forwarding and params_str:
        return u'<!--#include virtual="%s?%s" -->' % (path, params_str)
    return u'<!--#include virtual="%s" -->' % path
