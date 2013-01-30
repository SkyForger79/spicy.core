import sys
from . import defaults
from datetime import datetime as dt
from django import http
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.views.decorators.csrf import csrf_protect
from django.core.management.color import color_style
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to


style = color_style()


def page_not_found(request, template_name='%s/404.html' % defaults.SITESKIN):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """

    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR('handler404: %s %s %s %s\n'%(dt.now(), request.GET, request.POST, request.get_full_path())))

    t = loader.get_template(template_name) # You need to create a 404.html template.
    return http.HttpResponseNotFound(t.render(RequestContext(request, {'request_path': request.path})))


def forbidden(request, template_name='%s/403.html' % defaults.SITESKIN):
    """
    Default 404 handler.

    Templates: `404.html`
    Context:
        request_path
            The path of the requested URL (e.g., '/app/pages/bad_page/')
    """

    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR('handler403: %s %s %s %s\n'%(dt.now(), request.GET, request.POST, request.get_full_path())))

    t = loader.get_template(template_name) # You need to create a 403.html template.
    return http.HttpResponseNotFound(t.render(RequestContext(request, {'request_path': request.path})))


def server_error(request, template_name='%s/500.html' % defaults.SITESKIN):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    if defaults.DEBUG_ERROR_PAGES:
        sys.stderr.write(style.ERROR('handler505: %s %s %s %s\n'%(dt.now(), request.GET, request.POST, request.get_full_path())))

    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({})))


"""
Example of universal rubric rendering
"""

def render(request, template, **kwargs):
    print kwargs
    page = kwargs.pop('page', None)
    template = defaults.SITESKIN + '/' + (
        ('index/flatpages/' +  (page.template_name or 'default.html'))
        if (page and page.content and page.content != 'autocreated')
        else template)
    return render_to_response(
        template, {'page_slug': page.title if page else None},
        context_instance=RequestContext(request), **kwargs)



"""
For rubrics from dynamic content blocks
"""

class BlockElement:
   def __init__(self, block, prev):
      self.instance = block
      self.prev = prev


#XXX may be will not work with cache_page
@csrf_protect
@render_to('pub_point.html', use_siteskin=True)
def pub_point(request, pub_point):
   """
   Dynamic publication point
   you can build page from content-blocks using pub-point relation.
   """
   try:
      pub_point = api.register['xtag'].get_tag(
         pub_point, vocabulary='pub_point')
   except:
      raise http.Http404
   
   prev = None
   content_blocks = list()

   block_provider = api.register['siteskin'].get_provider(pub_point)
   for block in block_provider.get_instances(pub_point):
      content_blocks.append(BlockElement(block, prev))
      prev = block

   return {'pub_point': pub_point, 'content_blocks': content_blocks}



def write_to_uilog(request):
   from siteskin.forms import UILogForm
   message = 'error'
   form = UILogForm()
   if request.method == 'POST':
      form = UILogForm(request.POST)
      if form.is_valid():
         form.save()
         message = 'ok'
   return http.HttpResponse(message)
