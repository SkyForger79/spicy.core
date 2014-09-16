import os, tempfile
from django.contrib.auth import views
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from spicy.mediacenter import defaults as mc_defaults
from django.core.files.base import ContentFile
from spicy.utils.models import get_custom_model_class
from . import defaults
from redmine import Redmine

SettingsModel = get_custom_model_class(defaults.ADMIN_SETTINGS_MODEL)
Library = get_custom_model_class(mc_defaults.CUSTOM_LIBRARY_MODEL)
Media = get_custom_model_class(mc_defaults.CUSTOM_MEDIA_MODEL)
File = get_custom_model_class(mc_defaults.CUSTOM_FILE_MODEL)

def login(request):
    return views.login(
        request, template_name='spicy.core.admin/admin/login.html', extra_context={'redirect':request.GET.get('next')})


def logout(request):
    return views.logout(request, template_name='spicy.core.admin/admin/logout.html')


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
    return {'success': True, 'media_file': {'path': t_file.name, 'filename': title}}


@ajax_request
def export_to_redmine(request):
    if request.method == 'POST':
        redmine_settings = SettingsModel.on_site.get(pk__isnull=False)
        subject = request.POST.get('subject')
        desc = request.POST.get('description')
        try:
            redmine = Redmine(
                redmine_settings.redmine_tracker_url,
                username=redmine_settings.redmine_username,
                password=redmine_settings.redmine_password)
            path_files = request.POST.getlist('path_files[]')[0].split(',')
            name_files = request.POST.getlist('name_files[]')[0].split(',')
            uploads = []
            if path_files[0] and name_files[0]:
                for x in xrange(len(path_files)):
                    uploads.append({'path': path_files[x],'filename': name_files[x]})
            issue = redmine.issue.create(
                project_id=redmine_settings.redmine_project,
                subject=unicode(subject), description=unicode(desc), uploads=uploads)
            success = 'ok'
            messages = issue.id
        except:
            success = 'false'
            messages = ''
        for x in xrange(len(path_files)):
            if os.path.isfile(path_files[x]):
                os.remove(path_files[x])
    else:
        success = 'false'
        messages = ''
    return {'success': success, 'messages': messages,}
