from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME

from spicy.core.service import api
from . import defaults


def base(request):
    sites = Site.objects.all()
    current = Site.objects.get_current()

    all_services = [
        (srv.name, unicode(srv.label))
        for srv in api.register.get_list()]
    content_services = [
        (srv.name, unicode(srv.label))
        for srv in api.register.get_list(stype='content')]

    current_admin_base = 'spicy.core.admin/admin/base.html'
    if defaults.ADMIN_SITESKIN is not None:
        current_admin_base = defaults.ADMIN_SITESKIN + '/base.html'

    return {
        'current_site': current,

        'current_admin_base': current_admin_base,
        'ADMIN_SITESKIN': defaults.ADMIN_SITESKIN,

        # BBB deprecated
        'current_base': 'base.html',
        'current_path': request.path,

        'sites': sites,

        'ALL_SERVICES': all_services,
        'CONTENT_SERVICES': content_services,
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
        'DEBUG': settings.DEBUG,

        # UTM params
        'utm_campaign': request.GET.get('utm_campaign'),
        'utm_source': request.GET.get('utm_source'),
        'utm_medium': request.GET.get('utm_medium'),
        'utm_content': request.GET.get('utm_content'),
        'utm_term': request.GET.get('utm_term'),
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
