# -*- coding: utf-8 -*-
import os
import pytils
import re
import sys
from django.utils.translation import ugettext_lazy as _


# XXX title_func unused
# This is broken, use find_templates from utils.templates!
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


def make_cache_key(request=None, path=None):
    return path or request.get_full_path()

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


def strip_invalid_chars(data, extra=u'', verbose=False):
    """
    Remove characters that break XML parsers.

    This is meant to clean weird shit that occasionally appears in text,
    probably because M$ Word was used.
    """
    remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]' % extra)
    data, count = remove_re.subn('', data)
    if count:
        plur = ((count > 1) and u's') or u''
        if verbose:
            sys.stderr.write('Removed %s character%s.\n' % (count, plur))
            sys.stdout.write(data)
    return data


__all__ = (
    'get_templates', 'make_cache_key', 'RU_ALPHABET', 'EN_ALPHABET',
    'KNOWN_CHARS', 'MONTHS', 'make_slug', 'cached_property', 'CDATA_RE',
    'cdata', 'strip_invalid_chars')
