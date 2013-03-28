from datetime import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME

from spicy.core.service import api

#from extprofile import defaults as profile_defaults
#from presscenter import defaults as ps_defaults
#from rmanager import defaults as rm_defaults

from . import defaults


def base(request):
    sites = Site.objects.all()
    current = Site.objects.get_current()

    return {
        'current_site': current, 
        'sites': sites,     
        'current_base': defaults.SITESKIN + '/base.html',
        'current_admin_base': defaults.SITESKIN_ADMIN + '/base.html',
        'current_path': request.path, 

        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
               
        'SITESKIN': defaults.SITESKIN,
        'SITESKIN_ADMIN': defaults.SITESKIN_ADMIN,
        
        'ENABLE_BANNER_BLOCKS': defaults.ENABLE_BANNER_BLOCKS,
        'ENABLE_COUNTERS': defaults.ENABLE_COUNTERS,
        
        'DEBUG': settings.DEBUG,
        'now': datetime.now
        }


def boolean(request):
    """
    This if for ability to pass boolean arguments
    to templatetags.
    """
    return {
        'True': True,
        'False': False,
    }
