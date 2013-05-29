from django.conf import settings


from . import defaults


def base(request):
    current_admin_base = 'spicy.core.admin/admin/base.html'
    if defaults.ADMIN_THEME is not None:
        current_admin_base = defaults.ADMIN_THEME + '/base.html'

    return {
        'current_admin_base': current_admin_base,
        'ADMIN_THEME': defaults.ADMIN_THEME,
        'ADMIN_APPS': defaults.ADMIN_APPS,
        'ADMIN_DASHBOARD_APPS': defaults.ADMIN_DASHBOARD_APPS,
        }

