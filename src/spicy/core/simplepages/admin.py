import os
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from spicy.core.admin import defaults as admin_defaults
from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to
from spicy import utils
from . import defaults, forms


SimplePage = utils.get_custom_model_class(defaults.SIMPLE_PAGE_MODEL)


class AdminApp(AdminAppBase):
    name = 'simplepages'
    label = _('Simple Pages')
    order_number = 10

    menu_items = (
        AdminLink('simplepages:admin:create', _('Create simple page')),
        AdminLink('simplepages:admin:index', _('All simple pages')),
        AdminLink('simplepages:admin:find', _('Update from templates')),
    )

    create = AdminLink('simplepages:admin:create', _('Create simple page'),)

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='simplepages')
@render_to('index.html', use_admin=True)
def index(request):
    """
    List all simple pages.
    """
    nav = utils.NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(
        SimplePage, reverse('simplepages:admin:index'),
        obj_per_page=admin_defaults.ADMIN_OBJECTS_PER_PAGE)
    objects_list = paginator.current_page.object_list

    return {'nav': nav, 'objects_list': objects_list, 'paginator': paginator}


@is_staff(required_perms='simplepages.add_defaultsimplepage')
@render_to('find.html', use_admin=True)
def find(request):
    """
    Find new simple pages.
    """
    base_dir = "spicy.core.simplepages/simplepages"
    templates = utils.find_templates(base_dir, name_tuples=False)
    found = []
    existing = []
    site = Site.objects.get_current()
    extensions = 'html', 'txt'
    for filepath in templates:
        ext = filepath.rsplit('.', 1)[-1]
        if ext not in extensions:
            continue

        filename = filepath.rsplit('/simplepages/', 1)[-1]
        if filename.endswith('.html'):
            filename = filename[:-5]

        splitted = filename.rsplit('.')
        if ext != 'html':
            splitted = splitted[:-2] + ['.'.join(splitted[-2:])]
        basename = '.'.join(splitted)
        baseurl = '/'.join(splitted)
        url = ('/{0}/' if ext == 'html' else '/{0}').format(baseurl)
        content = file(filepath).read()
        page, is_created = SimplePage.objects.get_or_create(
            title=basename, url=url,
            template_name=os.path.join(base_dir, filename),
            defaults={'content': content})
        if is_created:
            page.sites = [site]
            found.append(page)
        else:
            existing.append(page)
            page.content = content
            page.save()
    return {'found': found, 'existing': existing}


@is_staff(required_perms='simplepages.add_defaultsimplepage')
@render_to('create.html', use_admin=True)
def create(request):
    """
    Create a new simple page.
    """
    message = None
    if request.method == 'POST':
        form = forms.SimplePageForm(request.POST)
        if form.is_valid():
            page = form.save()
            return HttpResponseRedirect(
                reverse('simplepages:admin:edit', args=[page.pk]))
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.SimplePageForm()
    return {'form': form, 'message': message}


@is_staff(required_perms='simplepages.add_defaultsimplepage')
@render_to('edit.html', use_admin=True)
def edit(request, simplepage_id):
    """
    Create a new simple page.
    """
    page = get_object_or_404(SimplePage, pk=simplepage_id)
    message = None
    if request.method == 'POST':
        form = forms.SimplePageForm(request.POST, instance=page)
        if form.is_valid():
            page = form.save()
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.SimplePageForm(instance=page)
    return {'form': form, 'message': message}


@is_staff(required_perms='simplepages.delete_defaultsimplepage')
@render_to('delete.html', use_admin=True)
def delete(request, simplepage_id):
    page = get_object_or_404(SimplePage, pk=simplepage_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            page.delete()
            return HttpResponseRedirect(reverse('simplepages:admin:index'))
    return {'instance': page}
