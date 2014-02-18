from django.contrib.auth import views
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to
from django.http import HttpResponse
from spicy.utils.models import get_custom_model_class
from . import defaults

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)

def login(request):
    return views.login(
        request, template_name='spicy.core.admin/admin/login.html')


def logout(request):
    return views.logout(request, template_name='spicy.core.admin/admin/logout.html')


def robots(request):
    robots = SettingsModel.on_site.get(pk__isnull=False)
    response = HttpResponse(robots.robots, mimetype='text/plain')
    return response
