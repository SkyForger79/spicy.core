import os
import tempfile
from django.contrib.auth import views
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.core.files.base import ContentFile
from spicy.utils.models import get_custom_model_class
from . import defaults

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)


def login(request):
    return views.login(
        request, template_name='spicy.core.admin/admin/login.html',
        extra_context={'redirect': request.GET.get('next')})


def logout(request):
    return views.logout(request,
                        template_name='spicy.core.admin/admin/logout.html')


def robots(request):
    robots = SettingsModel.on_site.get(pk__isnull=False)
    response = HttpResponse(robots.robots, mimetype='text/plain')
    return response


@ajax_request
def image_add(request):
    title = os.path.basename(request.GET['qqfile'])
    t_file = tempfile.NamedTemporaryFile(delete=False)
    t_file.write(request.raw_post_data)
    t_file.close()
    return {'success': True,
            'media_file': {'path': t_file.name, 'filename': title}}


