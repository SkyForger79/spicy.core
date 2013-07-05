# -*- coding: utf-8 -*-
import base64
import hashlib
import os
import pytils
import re
import sys
from . import defaults
from datetime import datetime
from django import http
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _
from math import ceil

MESSAGES = {'success': _('Changes were successfully saved.'),
            'error': _('Please, correct the errors below.')}


def make_cache_key(request=None, path=None):
    path = request.get_full_path() if request else path
    if hasattr(request, 'geos'):
        from maps.utils import get_geos_coords
        path += ':%s,%s' % get_geos_coords(request.geos)
    return path
    #params = [request.get_full_path()]
    #if hasattr(request, 'geos'):
    #    from maps.utils import get_geos_coords
    #    params.append(','.join(map(str(get_geos_coords(request.geos)))))
    #params = hashlib.sha512(''.join(map(str, params))).hexdigest()
    #return ':'.join([defaults.CACHE_PREFIX, params])


def log(msg):
    print '@@ LOG @ %s: %s' % (datetime.now(), msg)


RU_ALPHABET = [
    u'А', u'Б', u'В', u'Г', u'Д', u'Е', u'Ё',
    u'Ж', u'З', u'И', u'Й', u'К', u'Л', u'М',
    u'Н', u'О', u'П', u'Р', u'С', u'Т', u'У',
    u'Ф', u'Х', u'Ц', u'Ч', u'Ш', u'Щ', u'Ъ',
    u'Ы', u'Ь', u'Э', u'Ю', u'Я',
]

EN_ALPHABET = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

KNOWN_CHARS = (
    (')(', 'H'),
    ('}{', 'H'),
    (')I(', 'J'),
    ('}I{', 'J'),
    (')|(', 'J'),
    ('}|{', 'J'),
    ('$', 's'),
    ('*', 'X'),
    (' ', '-'),
    ('#', 'H'),
    ('@', 'a'),
    ('.', '_'),
    (':', '_'),
    (';', '_'),
    ('&', '_and_'),
    ('?', '_'),
    ('^', '_'),
    ('`', '_'),
    ('~', '_'),
    ('!', 'I'),
    ('%', '_'),
    (')', '_'),
    ('(', '_'),
    ('}', '_'),
    ('{', '_'),
    ('+', '_'),
    ('>', '_'),
    ('<', '_'),
    ('[', ''),
    (']', ''),
    ('"', '_'),
    ('\'', ''),
    ('\\', ''),
    (',', '_'),
    ('=', '-'),
    ('|', '_'),
    ('/', '_'),
    ('_', '_'),
    ('-', '-'),
    ('-_', '-'),
    ('_-', '-'),
    #('--', '-'),
    #('__', '_'),
    )

MONTHS = (
    _("January"), _("February"), _("March"), _("April"), _("May"), _("June"),
    _("July"), _("August"), _("September"), _("October"), _("November"),
    _("December"))


def make_slug(title):
    try:
        title = title.decode('utf-8')
    except:
        title = title.encode('utf-8').decode('utf-8')

    try:
        title = pytils.translit.translify(title)
    except:
        title = pytils.translit.slugify(title)

    for from_ch, to_ch in KNOWN_CHARS:
        title = title.replace(from_ch, to_ch)
        title = title.strip(from_ch)

    return title.lower()

DEFAULT_FILTERS = [
    ('search_text', ''),
]

def chunks(data, num_cols):
    col_length = int(ceil(len(data) / float(num_cols)))
    for i in xrange(0, num_cols):
        yield data[i * col_length : (i + 1) * col_length]


class NavigationFilter:
    def __init__(self, request, accepting_filters=DEFAULT_FILTERS,
                 default_order=None, force_filter=None):
        self.request = request
        self.querydict = request.GET

        self.order = None

        self.filter = ''

        if 'filter' in request.GET:
            self.filter = request.GET['filter']
        if force_filter:
            self.filter = force_filter

        for filter, default in accepting_filters:
            setattr(self, filter, request.GET.get(filter, default))

        self.page = request.GET.get('page', 1)

        self.field = request.GET.get('field', default_order)
        fields = self.field.split(' ') if self.field else None
        self.order_q = request.GET.get('order', 'asc')
        if fields and self.order_q:
            direction = '-' if self.order_q.lower() == 'desc' else ''
            self.order = [direction + field for field in fields]

    def get_queryset_with_paginator(
        self, model, base_url=None, search_query=None,
        obj_per_page=defaults.OBJECTS_PER_PAGE, manager='objects',
        result_manager='objects', distinct=False):

        base_url = base_url or self.request.path

        model_manager = getattr(model, manager)
        model_qset = model_manager.values_list('id', flat=True)

        # XXX: check usage
        if type(search_query) is dict:
            queryset = model_qset.filter(**search_query)

        elif type(search_query) is tuple:
            queryset = model_qset.filter(*search_query[0], **search_query[1])

        elif callable(search_query): # XXX
            queryset = search_query(model_qset)

        elif search_query is not None:
            queryset = model_qset.filter(search_query)

        else:
            queryset = model_qset.all()

        if self.order:
            queryset = queryset.order_by(*self.order)

        if distinct:
            queryset = queryset.distinct()

        paginator = Paginator(
            queryset, obj_per_page)
        try:

            page = paginator.page(self.page)
        except InvalidPage:
            raise http.Http404(unicode(_('Page %s does not exist.' % self.page)))
            # Django that can't throw exceptions other than 404.

        result_qset = getattr(
            model, result_manager).filter(
            id__in=tuple(page.object_list))
        if self.order:
            result_qset = result_qset.order_by(*self.order) # 1082

        # XXX
        page.object_list = result_qset

        paginator.current_page = page
        paginator.current_object_list = result_qset

        paginator.base_url = base_url

        return paginator


class cached_property(object):
    '''
    Turns decorated method into caching property (method is called once on
    first access to property).
    '''
    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result

CDATA_RE = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]')
cdata = lambda s: '<![CDATA[%s]]>' % CDATA_RE.sub(
    ' ', s).replace(']]>', ']]]]><![CDATA[>')
# Expand ]]> to an escaped version that doesn't end CDATA block. We could
# escape quoutes and tags in inserted data, but using CDATA is faster.


def make_message(message, status=''):
    if not message:
        return ''

    message = smart_str('|'.join((message, status)))
    encoded = base64.encodestring(message)[:-2]
    code = hashlib.md5(encoded + settings.SECRET_KEY).hexdigest()
    return 'message=%s&code=%s' % (encoded, code)


def check_message(request):
    encoded = request.GET.get('message')
    code = request.GET.get('code')
    if (not (encoded and code) or
        len(encoded) > defaults.MAX_MESSAGE_STRING_LENGTH):
        return

    expected_code = hashlib.md5(encoded + settings.SECRET_KEY).hexdigest()
    if code != expected_code:
        return

    return base64.decodestring(encoded + '==\n').split('|')

def strip_invalid_chars(data, extra=u'', verbose=False):
    """
    Remove characters that break XML parsers.

    This is meant to clean weird shit that occasionally appears in text, probably
    because M$ Word was used.
    """
    remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]' % extra)
    data, count = remove_re.subn('', data)
    if count:
        plur = ((count > 1) and u's') or u''
        if verbose:
            sys.stderr.write('Removed %s character%s.\n' % (count, plur))
            sys.stdout.write(data)
    return data


def get_templates(
    path, title_func=lambda template: template,
    filter_func=lambda template: True):
    try:
        templates = [
           (template, template) for template in os.listdir(path)
           if filter_func(template)]
        templates.sort()
        return templates
    except OSError:
        return []
