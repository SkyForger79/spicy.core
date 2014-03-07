from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from spicy.core.profile import defaults as p_defaults
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.simplepages import defaults as sp_defaults
from spicy.core.siteskin.decorators import render_to
from spicy.presscenter import defaults as d_defaults
from spicy.utils.models import get_custom_model_class
from . import conf, defaults, forms, utils


SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)
DocumentModel = get_custom_model_class(d_defaults.CUSTOM_DOCUMENT_MODEL)
Profile = get_custom_model_class(p_defaults.CUSTOM_USER_MODEL)
SimplePage = get_custom_model_class(sp_defaults.SIMPLE_PAGE_MODEL)


class AdminApp(conf.AdminAppBase):
    name = 'spicyadmin'
    label = _('Admin')
    order_number = 10

    menu_items = (
        conf.AdminLink('spicyadmin:admin:index', _('Dashboard')),
        conf.AdminLink('spicyadmin:admin:settings', _('Settings')),
    )
    perms = conf.Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff
@render_to('spicy.core.admin/admin/dashboard.html', use_admin=True)
def dashboard(request):
    sites = Site.objects.all()
    dashboard_links = []
    dashboard_lists = []
    for admin_app in conf.admin_apps_register.values():
        if admin_app.dashboard_links:
            dashboard_links.extend(admin_app.dashboard_links)
        if admin_app.dashboard_lists:
            dashboard_lists.extend(admin_app.dashboard_lists)
    #profiles = Profile.on_site.select_related().order_by(
    #    '-id','-date_joined')
    #simple_pages = SimplePage.on_site.select_related().order_by('-id')
    return {
        'dashboard_links': dashboard_links, 'dashboard_lists': dashboard_lists,
        'sites': sites}


@is_staff
@render_to('spicy.core.admin/admin/robots_txt.html', use_admin=True)
def robots_txt(request):
    robots, _created = SettingsModel.on_site.get_or_create(pk__isnull=False)
    site = Site.objects.get_current()
    if request.method == 'POST':
        form = forms.RobotsForm(request.POST, instance=robots)
        sform = forms.SiteForm(request.POST, instance=site)
        if form.is_valid() and sform.is_valid():
            form.save()
            sform.save()
    else:
        form = forms.RobotsForm(instance=robots)
        sform = forms.SiteForm(instance=site)
    return {'form': form, 'sform': sform}


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

    return {'form': form, 'messages': messages}


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
    return {'form': form, 'apps': apps, 'messages': messages}


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

    return {'form': form, 'messages': messages}
