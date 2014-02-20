from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils.models import get_custom_model_class
from spicy.core.profile.decorators import is_staff

from .conf import AdminAppBase, AdminLink, Perms
from . import defaults, forms, utils
from django.contrib.sites.models import Site

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)


class AdminApp(AdminAppBase):
    name = 'spicyadmin'
    label = _('Admin')
    order_number = 10

    menu_items = (
        AdminLink('spicyadmin:admin:index', _('Dashboard')),
        AdminLink('spicyadmin:admin:settings', _('Settings')),
    )
    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff
@render_to('spicy.core.admin/admin/dashboard.html', use_admin=True)
def dashboard(request):
    return {'services': api.register.get_list()}

@is_staff
@render_to('spicy.core.admin/admin/robots_txt.html', use_admin=True)
def robots_txt(request):
    robots, _created = SettingsModel.on_site.get_or_create(pk__isnull=False)
    site = Site.objects.get_current()
    message = ''
    if request.method == 'POST':
        form = forms.RobotsForm(request.POST, instance=robots)
        sform = forms.SiteForm(request.POST, instance=site)
        if form.is_valid() and sform.is_valid():
            form.save()
            sform.save()
            message = 'Success'
    else:
        form = forms.RobotsForm(instance=robots)
        sform = forms.SiteForm(instance=site)
    return {'services': api.register.get_list(), 'form': form, 'sform': sform}

@is_staff
@render_to('spicy.core.admin/admin/main_settings.html', use_admin=True)
def main_settings(request):
    return {'services': api.register.get_list()}

@is_staff
@render_to('spicy.core.admin/admin/sitemap.html', use_admin=True)
def sitemap(request):
    return {'services': api.register.get_list()}


@is_staff(required_perms=('admin.edit_settings',))
@render_to('spicy.core.admin/admin/managers.html', use_admin=True)
def managers(request):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    messages = []
    instance = utils.get_admin_settings()
    
    if request.method == 'POST':        
        form = forms.SettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        else:
            messages.append(form.errors.as_text())
    else:
        form = forms.SettingsForm(instance=instance)

    return {
        'form': form,
        'messages': messages,
    }


@is_staff(required_perms=('admin.edit_settings',))
@render_to('spicy.core.admin/admin/application.html', use_admin=True)
def application(request):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    messages = []
    instance = utils.get_admin_settings()
    
    if request.method == 'POST':        
        form = forms.ApplicationForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        else:
            messages.append(form.errors.as_text())
    else:
        form = forms.ApplicationForm(instance=instance)

    apps = []
    return {
        'form': form,
        'apps': apps,
        'messages': messages,
    }


@is_staff(required_perms=('admin.edit_settings',))
@render_to('spicy.core.admin/admin/developer.html', use_admin=True)
def developer(request):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    messages = []
    instance = utils.get_admin_settings()
    
    if request.method == 'POST':        
        form = forms.DeveloperForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        else:
            messages.append(form.errors.as_text())
    else:
        form = forms.DeveloperForm(instance=instance)

    return {
        'form': form,
        'messages': messages,
    }

