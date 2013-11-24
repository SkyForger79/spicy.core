from django.conf import settings

from spicy.utils.printing import print_info
from . import defaults
from .conf import admin_apps_register

def base(request):
    return {
        'ADMIN_APPS': sorted(admin_apps_register.values(), key=lambda x: x.order_number, reverse=False),
        'ADMIN_DASHBOARD_APPS': defaults.ADMIN_DASHBOARD_APPS,
        }

