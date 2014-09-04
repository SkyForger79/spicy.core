import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from spicy.core.siteskin import utils


register = template.Library()


class GenericSSINode(template.Node):
    def __init__(self, url, get_forwarding=False):
        self.url = url
        self.get_forwarding = get_forwarding

    def render(self, context):
        url = self.url.resolve(context)
        return utils.choose_render_method(
            context['request'], url, get_forwarding=self.get_forwarding)


@register.tag
def generic_ssi(parser, token):
    """
    {% generic_ssi "/doc-list/contentblock/1/" %} - render content-block using
        absolute URL path to app.

    {% generic_ssi "/doc-list/contentblock/1/" True %} - same, with GET
    forwarding enabled.
    """

    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "'%s' takes two arguments maximum (path to a view [GET "
            "forwarding false|true])" % bits[0])
    url = parser.compile_filter(bits[1])

    get_forwarding = False
    if len(bits) == 3:
        get_forwarding = parser.compile_filter(bits[2])

    return GenericSSINode(url, get_forwarding=get_forwarding)


class RenderFromResponseNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        url = self.url.resolve(context)
        return utils.get_render_from_response(
            context['request'], url)


@register.tag
def render_response(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError(
            "'%s' takes at least one argument (path to a view)" % bits[0])

    return RenderFromResponseNode(parser.compile_filter(bits[1]))


@register.tag
def captureas(parser, token):
    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ''


@register.filter
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
    return value.get(arg)


@register.filter
def is_even(value):
    return value % 2 == 0


@register.filter
def head(value):
    if value:
        return value.split('.', 1)[0].split('-', 1)[0].split('_', 1)[0]
