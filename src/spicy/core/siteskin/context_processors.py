from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME

from spicy.core.service import api
from . import defaults


def base(request):
    sites = Site.objects.all()
    current = Site.objects.get_current()

    siteskin_base = defaults.SITESKIN + '/base.html'
    all_services = [
        (srv.name, unicode(srv.label))
        for srv in api.register.get_list()]
    content_services = [
        (srv.name, unicode(srv.label))
        for srv in api.register.get_list(stype='content')]


    return {
        'current_site': current,
        'sites': sites,
        'ALL_SERVICES': all_services,
        'CONTENT_SERVICES': content_services,
        'current_base': siteskin_base.strip('/'),
        'current_path': request.path,
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
        'SITESKIN': defaults.SITESKIN,
        'DEBUG': settings.DEBUG,
        }


def boolean(request):
    """
    This if for ability to pass boolean arguments
    to templatetags.
    """
    return {
        'True': True,
        'False': False
    }
