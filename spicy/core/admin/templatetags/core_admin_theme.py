# coding: utf-8
from django import template
from django.conf import settings
from django.template.loader_tags import BlockNode


register = template.Library()


# class AppBlockNode(BlockNode):
#     def __init__(self, name, app, nodelist, parent=None):
#         self.app = template.Variable(app)
#         super(AppBlockNode, self).__init__(name, nodelist, parent)
#
#     def __repr__(self):
#         return "<AppBlock Node: %s. Contents: %r>" % (
#             self.name, self.nodelist)
#
#     def render(self, context):
#         app = self.app.resolve(context)
#         if app in settings.INSTALLED_APPS:
#             return super(AppBlockNode, self).render(context)
#         else:
#             return u''
#
#
# @register.tag('appblock')
# def do_appblock(parser, token):
#     """
#     Define a block that can be overridden by child templates.
#     """
#     bits = token.contents.split()
#     if len(bits) != 3:
#         raise TemplateSyntaxError("'%s' tag takes only one argument" % bits[0])
#     block_name = bits[1]
#     block_app = bits[2]
#     # Keep track of the names of AppBlockNodes found in this template, so we can
#     # check for duplication.
#     try:
#         if block_name in parser.__loaded_blocks:
#             raise TemplateSyntaxError("'%s' tag with name '%s' appears more than once" % (bits[0], block_name))
#         parser.__loaded_blocks.append(block_name)
#     except AttributeError: # parser.__loaded_blocks isn't a list yet
#         parser.__loaded_blocks = [block_name]
#     nodelist = parser.parse(('endappblock',))
#
#     # This check is kept for backwards-compatibility. See #3100.
#     endblock = parser.next_token()
#     acceptable_endblocks = ('endappblock', 'endappblock %s' % block_name)
#     if endblock.contents not in acceptable_endblocks:
#         parser.invalid_block_tag(endblock, 'endappblock', acceptable_endblocks)
#
#     return AppBlockNode(block_name, block_app, nodelist)
#
# @register.filter
# def installed_app(value):
#     return value in settings.INSTALLED_APPS
#
#
# @register.simple_tag
# def menu(request, url_path, title, li_style='', extra_style='', get='', url_params=''):
#
#     if url_path:
#         if url_params:
#             url = reverse(url_path, args=str(url_params).split(','))
#         else:
#             url = reverse(url_path)
#     else:
#         url = request.path
#
#     if get:
#         url += '?' + get
#
#     path = request.path + '?' + request.META['QUERY_STRING']
#     if path.rstrip('?') == url:
#         li_style = li_style + ' ' + 'activated'
#         content = '<a href="%s" class="ui-corner-left">%s</a>'%(url, unicode(title))
#     else:
#         content = '<a href="%s" %s>%s</a>'%(url, mk_style(extra_style), unicode(title))
#
#     return '<li %(class)s>%(content)s</li>'%{
#         'class': mk_style(li_style), 'content': content}
#
#
# @register.inclusion_tag('spicy.core.admin/admin/formfield.html', takes_context=True)
# def formfield(context, title, form, field_name='', type='li'):
#     label = title
#     field = None
#     if field_name:
#         field = form[field_name]
#         label = field.label_tag(title or field.label)
#
#     return dict(title=title, form=form, type=type, field=field, label=label)

# @register.filter('fieldtype')
# def fieldtype(obj):
#     """Helper for form rendering.
#
#     Returns name of field for conditional form building
#
#     """
#     return obj.__class__.__name__
