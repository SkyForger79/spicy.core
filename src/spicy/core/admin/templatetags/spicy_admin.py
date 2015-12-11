# coding: utf-8
from django import template
from django.conf import settings
from django.template.loader_tags import BlockNode
from django.core.urlresolvers import reverse
from spicy.core.admin import conf

register = template.Library()


@register.simple_tag
def app_menu(request, app, *args, **kwargs):
    return app.menu(request, app, *args, **kwargs).content


@register.simple_tag
def app_dashboard(request, app, *args, **kwargs):
    return app.dashboard(request, app, *args, **kwargs).content


class AppBlockNode(BlockNode):
    def __init__(self, name, app, nodelist, parent=None):
        self.app = template.Variable(app)
        super(AppBlockNode, self).__init__(name, nodelist, parent)

    def __repr__(self):
        return "<AppBlock Node: %s. Contents: %r>" % (
            self.name, self.nodelist)

    def render(self, context):
        app = self.app.resolve(context)
        if app in settings.INSTALLED_APPS:
            return super(AppBlockNode, self).render(context)
        else:
            return u''


@register.tag('appblock')
def do_appblock(parser, token):
    """
    Define a block that can be overridden by child templates.
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError(
            "'%s' tag takes only one argument" % bits[0])
    block_name = bits[1]
    block_app = bits[2]

    # Keep track of the names of AppBlockNodes found in this template, so we
    # can check for duplication.
    try:
        if block_name in parser.__loaded_blocks:
            raise template.TemplateSyntaxError(
                "'%s' tag with name '%s' appears more than once" % (
                    bits[0], block_name))
        parser.__loaded_blocks.append(block_name)
    except AttributeError:  # parser.__loaded_blocks isn't a list yet
        parser.__loaded_blocks = [block_name]
    nodelist = parser.parse(('endappblock',))

    # This check is kept for backwards-compatibility. See #3100.
    endblock = parser.next_token()
    acceptable_endblocks = ('endappblock', 'endappblock %s' % block_name)
    if endblock.contents not in acceptable_endblocks:
        parser.invalid_block_tag(endblock, 'endappblock', acceptable_endblocks)

    return AppBlockNode(block_name, block_app, nodelist)


@register.filter
def installed_app(value):
    return value in settings.INSTALLED_APPS


@register.simple_tag
def menu(
        request, url_path, title, li_style='', extra_style='', get='',
        url_params=''):
    from spicy import utils
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


@register.inclusion_tag(
    'spicy.core.admin/admin/formfield.html', takes_context=True)
def formfield(
        context, title, form, field_name='', type='li-text',
        preview_link=False, classes='', id='', ajax_url='',
        data_url='', from_field=''):
    label = title
    field = None
    if field_name:
        field = form[field_name]
        label = field.label_tag(title or field.label)

    try:
        consumer_type = (
            getattr(form, '__class__') or form.form
        ).Meta.model.__name__.lower()
    except AttributeError:
        consumer_type = None

    return dict(
        title=title, form=form, type=type, field=field, label=label,
        preview_link=preview_link, classes=classes, id=id, ajax_url=ajax_url,
        data_url=data_url, from_field=from_field, consumer_type=consumer_type)


@register.filter
def check_perms(user, arg):
    if isinstance(arg, conf.AdminLink):
        return conf.check_perms(user, arg.perms)
    elif isinstance(arg, conf.AdminAppBase):
        return arg.any_perms(user)
    else:
        return user.has_perm(arg)


@register.simple_tag(takes_context=True)
def apply(context, func, arg, result_var):
    func_parts = func.rsplit('.', 1)
    mod = func_parts[:-1]
    func_attr = func_parts[-1]
    if mod:
        func = getattr(template.Variable(mod[0]).resolve(context), func_attr)
    else:
        func = context.get(func_attr)

    if not func:
        return u''
    try:
        result = func(arg)
        context[result_var] = result
    except:
        pass

    return u''
