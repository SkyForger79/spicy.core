from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME


from . import defaults


def base(request):
    sites = Site.objects.all()
    current = Site.objects.get_current()

    current_admin_base = 'spicy.core.admin/admin/base.html'
    if defaults.SITESKIN_ADMIN is not None:
        current_admin_base = defaults.SITESKIN_ADMIN + '/base.html'

    return {
        'current_site': current,
        'sites': sites,
        'current_base': defaults.SITESKIN + '/base.html',
        'current_admin_base': current_admin_base,
        'current_path': request.path,
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
        'SITESKIN': defaults.SITESKIN,
        'SITESKIN_ADMIN': defaults.SITESKIN_ADMIN,
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
