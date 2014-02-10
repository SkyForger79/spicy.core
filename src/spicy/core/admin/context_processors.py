from . import defaults
from .conf import admin_apps_register


def base(request):
    return {
        'ADMIN_APPS': sorted(
            admin_apps_register.values(),
            key=lambda x: x.order_number, reverse=False),
        'ADMIN_APPS_REGISTER': admin_apps_register,
        'ADMIN_DASHBOARD_APPS': defaults.ADMIN_DASHBOARD_APPS,
        }

