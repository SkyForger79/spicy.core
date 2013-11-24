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
@render_to('spicy.core.admin/admin/dashboard.html')
def dashboard(request):
    return {'services': api.register.get_list()}


@is_staff(required_perms=('admin.edit_settings',))
@render_to('spicy.core.admin/admin/settings.html', use_admin=True)
def edit_settings(request):
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
@render_to('spicy.core.admin/admin/developer.html', use_admin=True)
def developer(request):
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

