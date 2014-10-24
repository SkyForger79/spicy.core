from . import defaults
from .conf import admin_apps_register


def path_with_port(request):

    try:

        if request.META.get('SERVER_PORT') and request.META.get('SERVER_PORT')\
                != '80':
            return 'http://' + request.get_host() + ':'\
                + request.META['SERVER_PORT'] + request.path
        else:
            return 'http://' + request.get_host() + request.path
    except:
        return ''


def host_with_port(request):

    try:

        if request.META.get('SERVER_PORT') and request.META.get('SERVER_PORT')\
                != '80':
            return 'http://' + request.get_host() + ':'\
                + request.META['SERVER_PORT']
        else:
            return 'http://' + request.get_host()

    except:
        return ''


def base(request):
    return {
        'ADMIN_APPS': sorted(
            admin_apps_register.values(),
            key=lambda x: x.order_number, reverse=False),
        'ADMIN_APPS_REGISTER': admin_apps_register,
        'ADMIN_DASHBOARD_APPS': defaults.ADMIN_DASHBOARD_APPS,
        'FULL_PATH_WITH_PORT': path_with_port(request),
        'HOST_WITH_PORT': host_with_port(request)

    }
