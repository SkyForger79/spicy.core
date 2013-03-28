import datetime
import re
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.template import Library, Node, TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from spicy.core.siteskin import defaults

# XXX WTF is this???
#from siteskin.template import get_css_version

#from spicy.core.siteskin.models import ContentBlock
#from xtag.models import TagProviderModel

register = Library()


def choose_render_method(request, url, get_forwarding=False):
    if not url:
        return '<!-- NO URL GIVEN -->'

    if defaults.USE_RENDER_FROM_RESPONSE_LIKE_SSI:
        return get_render_from_response(request, url, get_forwarding=get_forwarding)

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


class SiteskinSSINode(Node):
    def __init__(self, slug, view, flat_url, get_forwarding=False):
        self.slug = slug
        self.view = view
        self.flat_url = flat_url
        self.get_forwarding = get_forwarding

    def render(self, context):
        slug = self.slug.resolve(context)

        get_forwarding = self.get_forwarding
        if not isinstance(get_forwarding, bool):
            get_forwarding = get_forwarding.resolve(context)

        view = ''
        if self.view:
            view = self.view.resolve(context)

        flat_url = self.flat_url
        if not type(flat_url) == bool:
            flat_url = bool(flat_url.resolve(context))

        cache_key = '%s:block:%s'%(defaults.CACHE_PREFIX, slug+'-%s-%s'%(flat_url, view))
        url = cache.get(cache_key)
        if not url:
            try:
                cblock = ContentBlock.objects.get(slug=slug)
            except ContentBlock.DoesNotExist:
                return '404: ContentBlock "%s" does not exist.'%slug
            except Exception, msg:
                return '500: %s'%msg

            url = cblock.get_render_url(view=view)
            cache.set(cache_key, url, defaults.CACHE_TIMEOUT)


        if flat_url:
            return url

        if 'request' in context:
            return choose_render_method(context['request'], url, get_forwarding=get_forwarding)
        else:
            return get_render_from_response(None, url, get_forwarding=get_forwarding)


@register.tag
def siteskin_ssi(parser, token):
    """
    siteskin_ssi contentblock-slug additional-view flat_url=False

    {% siteskin_ssi "news" %} load content-block using slug
    {% siteskin_ssi "news" True %} load content-block using slug and forward GET parameters to the ssi controller
    {% siteskin_ssi "news" False "rss" True %} render RSS view for "news" content-block, return flat URL

    """

    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (slug of contentblock object)" % bits[0])

    additional_view = None
    flat_url = False
    get_forwarding = False

    if len(bits) == 2:
        content_block_slug = parser.compile_filter(bits[1])

    elif len(bits) == 3:
        content_block_slug = parser.compile_filter(bits[1])
        get_forwarding = parser.compile_filter(bits[2])

    elif len(bits) == 4:
        content_block_slug = parser.compile_filter(bits[1])
        get_forwarding = parser.compile_filter(bits[2])
        additional_view = parser.compile_filter(bits[3])

    elif len(bits) == 5:
        content_block_slug = parser.compile_filter(bits[1])
        get_forwarding = parser.compile_filter(bits[2])
        additional_view = parser.compile_filter(bits[3])
        flat_url = parser.compile_filter(bits[4])

    elif len(bits) > 4:
        raise TemplateSyntaxError(
            "'%s' takes maximum two arguments"
            " (slug of contentblock object and additional view name)" % bits[0])

    return SiteskinSSINode(content_block_slug, additional_view,
                           flat_url, get_forwarding=get_forwarding)

# XXX WTF is this???
#@register.filter
#def css_version(default):
    #return get_css_version(default)


def get_render_from_response(request, url, get_forwarding=False):
    from django.test.client import Client, FakePayload

    path, query = url, ''

    if '?' in url:
        path, query = url.split('?', 1)

    if request and request.GET:
        if query:
            query += '&'
        query += '&'.join(['%s=%s'%(key, values) for key, values in request.GET.items()])

    if request:
        meta = dict(request.META, PATH_INFO=path, QUERY_STRING=query)
        if not get_forwarding:
            meta = dict(request.META, PATH_INFO=path, QUERY_STRING='')
    else:
        meta = dict(PATH_INFO=path)
        # this is because django 1.3 now checking wsgi.input attribute in request
        # https://code.djangoproject.com/changeset/14453
        meta['wsgi.input'] = FakePayload('')
    response = Client().request(**meta)

    if isinstance(response, HttpResponseRedirect):
        url = response['Location']
        host = request.get_host()
        if host in url:
            url = url.split(host)[1]
        else:
            raise HttpResponseBadRequest(
                'Cross domain includes not allowed! %s'%
                response['Location'])
        return get_render_from_response(request, url, get_forwarding=get_forwarding)

    content = response.content.decode('utf-8')
    # we can't use httplib2 because devserver doesn't allow threads and
    # deadlocks himself
    #from httplib2 import Http
    #url = request.build_absolute_uri(url)
    #response = Http().request(url)[1]
    return content


class GenericSSINode(Node):
    def __init__(self, url, get_forwarding=False):
        self.url = url
        self.get_forwarding = get_forwarding

    def render(self, context):
        url = self.url.resolve(context)

        get_forwarding = self.get_forwarding
        if self.get_forwarding:
            get_forwarding = self.get_forwarding.resolve(context)

        return choose_render_method(
            context['request'], url, get_forwarding=get_forwarding)


@register.tag
def generic_ssi(parser, token):
    """
    {% generic_ssi "/doc-list/contentblock/1/" %} - render content-block using absolute URL path to app.

    """

    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes twoe arguments maximum "
                                  " (path to a view [GET forwarding false|true])" % bits[0])
    url = parser.compile_filter(bits[1])

    get_forwarding = False
    if len(bits) == 3:
        get_forwarding = parser.compile_filter(bits[2])

    return GenericSSINode(url, get_forwarding=get_forwarding)


class RenderFromResponseNode(Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        url = self.url.resolve(context)
        return get_render_from_response(
            context['request'], url)


@register.tag
def render_response(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])

    return RenderFromResponseNode(
        parser.compile_filter(bits[1]))


@register.tag
def captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)

class CaptureasNode(Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


@register.filter
def editable_by(value, arg):
    if arg.has_perm('xtag.all_pub_points'):
        return True
    elif not value:
        return False
    elif not hasattr(value, 'pub_points'):
        return True
    else:
        return arg.can_access_pub_points(
            (prov.tag if isinstance(prov, TagProviderModel) else
             prov.consumer)
            for prov in value.pub_points)

@register.filter
@stringfilter
def colorize_diff(value):
    """
    Colorize diff like hgweb does ;-)
    """
    return mark_safe(
        u'\n'.join(
            '<span%s>%s</span>' % (
                (' style="color:#cc0000;"' if line.startswith('-') else
                (' style="color:#008800;"' if line.startswith('+') else
                 (' style="color:#990099;"' if line.startswith('@') else ''))),
                conditional_escape(line)) for line in value.splitlines()))


@register.filter
@stringfilter
def last_path_bit(value):
    return [bit for bit in value.split('/')[::-1] if bit][0]


@register.filter
def next_week(value):
    return value + datetime.timedelta(7)


@register.filter
def startswith(value, arg):
    if not value:
        return False
    return value.startswith(arg)


@register.filter
def inc(value):
    return value + 1


@register.filter
def to_list(value):
    return list(value)


@register.filter
def get(value, arg):
    return value[arg]

class InsertBlockNode(SiteskinSSINode):
    def __init__(self, block_name, text, position, size):
        """
        Insert content block contents to text after specific position.
        """
        self.text = text
        self.position = position
        self.size = size
        super(InsertBlockNode, self).__init__(block_name, None, False)

    def render(self, context):
        text = self.text.resolve(context)
        if not defaults.ENABLE_INSERT_BLOCK:
            return text

        position = self.position.resolve(context)
        size = self.size.resolve(context)
        text_len = len(text)

        if text_len <= position + size:
            return text
            # Text too short, return text as is.
        else:
            regex = re.compile('.*?</\s*?p>', re.DOTALL|re.IGNORECASE)
            forbidden_regex = re.compile(
                '.*?<(img|h\d)(\s*?.*?)?>', re.DOTALL|re.IGNORECASE)
            paragraphs = [text[:position]]
            text_end = text[position:]
            chars_left = size
            insert_position = None
            buffered_paragraphs_length = 0
            buffered_paragraphs = []

            for bit in regex.finditer(text_end):
                start, end = bit.span()
                if insert_position is None:
                    insert_position = position + end
                    paragraphs.append(text[position:insert_position])
                    continue
                if chars_left <= 0:
                    # Yes, there's enough chars after insert position. Show the
                    # content block.
                    break

                paragraph_length = end - start
                paragraph = text[
                    insert_position + buffered_paragraphs_length :
                    insert_position + buffered_paragraphs_length + paragraph_length]

                buffered_paragraphs_length += paragraph_length
                buffered_paragraphs.append(paragraph)

                if forbidden_regex.match(paragraph):
                    # Forbidden tags inside paragraph, move forward insert
                    # position.
                    chars_left = size
                    insert_position = insert_position + buffered_paragraphs_length
                    buffered_paragraphs_length = 0
                    paragraphs.extend(buffered_paragraphs)
                    buffered_paragraphs = []
                else:
                    # Plain text paragraph, decrease remaining chars counter.
                    chars_left -= paragraph_length
            else:
                return text

            cb_text = super(InsertBlockNode, self).render(context)
            paragraphs.append(cb_text)
            paragraphs.append(text[insert_position:])
            for p in paragraphs:
                return u''.join(paragraphs)


@register.tag
def insert_block(parser, token):
    """
    Insert content block by name into text string after specified position.

    Usage:
    {% insert_block <name> into <text> after <position> [size <size>] %}
    i.e.
    {% insert_block "foo" into doc.rendered_body after 1000 size 200 %}
    """
    try:
        bits = token.split_contents()
        if len(bits) == 6:
            tag_name, block_name, _into, text, _after, position = bits
            _size = 'size'
            size = unicode(defaults.INSERT_BLOCK_DEFAULT_SIZE)
        elif len(bits) == 8:
            tag_name, block_name, _into, text, _after, position, _size, size = \
                bits
        else:
            raise ValueError
        if not _into == 'into' and _after == 'after' and _size == 'size':
            raise ValueError
    except ValueError:
        raise TemplateSyntaxError(
            "Invalid format, use {% insert_block <name> into <text> after "
            "<position> size <size>%}")

    return InsertBlockNode(
        parser.compile_filter(block_name), parser.compile_filter(text),
        parser.compile_filter(position), parser.compile_filter(size))


@register.filter
def is_even(value):
    return value % 2 == 0


@register.filter
def head(value):
    if value:
        return value.split('.', 1)[0].split('-', 1)[0].split('_', 1)[0]
