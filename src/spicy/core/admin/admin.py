from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to
from spicy.utils.models import get_custom_model_class
from . import conf, defaults, forms, utils


SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)


class AdminApp(conf.AdminAppBase):
    name = 'spicyadmin'
    label = _('Admin')
    order_number = 10

    menu_items = (
        conf.AdminLink(
            'spicyadmin:admin:settings', _('Metrics, meta & Extra JS'),
            icon_class='icon-cogs', perms='admin.change_settings'),
        conf.AdminLink(
            'spicyadmin:admin:robots', _('Setup robots.txt'),
            icon_class='icon-asterisk', perms='admin.change_settings'),
        conf.AdminLink(
            'spicyadmin:admin:sitemap', _('Sitemap.xml'),
            icon_class='icon-sitemap', perms='admin.change_settings'),
        conf.AdminLink(
            'spicyadmin:admin:managers', _('Manager\'s emails'),
            icon_class='icon-envelope',
            perms='admin.change_manager_settings'),
        conf.AdminLink(
            'spicyadmin:admin:application', _('Applications'),
            icon_class='icon-cloud-download', perms='admin.view_apps'),
        conf.AdminLink(
            'spicyadmin:admin:developer', _('Developer tools'),
            icon_class='icon-user-md'),
    )

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
            for link in admin_app.dashboard_links:
                if conf.check_perms(request.user, link.perms):
                    dashboard_links.append(link)
        if admin_app.dashboard_lists:
            for list in admin_app.dashboard_lists:
                if conf.check_perms(request.user, list.perms):
                    dashboard_lists.append(list)
    spicy_settings, _created = SettingsModel.on_site.get_or_create(
        pk__isnull=False)
    return {
        'dashboard_links': dashboard_links, 'dashboard_lists': dashboard_lists,
        'sites': sites, 'spicy_settings': spicy_settings}


@is_staff(required_perms='admin.change_settings')
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
        sform.fields['name'].label = _('Display name')
        sform.fields['domain'].label = _('Domain name')
    return {'form': form, 'sform': sform}


@is_staff(required_perms='admin.change_settings')
@render_to('spicy.core.admin/admin/main_settings.html', use_admin=True)
def main_settings(request):
    spicy_settings, _created = SettingsModel.on_site.get_or_create(
        pk__isnull=False)
    if request.method == 'POST':
        form = forms.MetricsForm(request.POST, instance=spicy_settings)
        if form.is_valid():
            spicy_settings = form.save()
            form = forms.MetricsForm(instance=spicy_settings)
    else:
        form = forms.MetricsForm(instance=spicy_settings)
    return {'form': form}


@is_staff(required_perms='admin.change_settings')
@render_to('spicy.core.admin/admin/sitemap.html', use_admin=True)
def sitemap(request):
    return {'services': api.register.get_list()}


@is_staff(required_perms='admin.chang_managers_settings')
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
            messages = 'Success'
        else:
            messages.append(form.errors.as_text())
    else:
        form = forms.SettingsForm(instance=instance)

    return {'form': form, 'messages': messages}


@is_staff(required_perms=('admin.view_apps',))
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


@is_staff(required_perms=('admin.XXX',))
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
