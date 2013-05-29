from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from spicy.core.service.utils import auto_adapt_to_methods


def _check_perms(user, required_perms):
    if '.' in required_perms:
        return user.has_perm(required_perms)
    else:
        return user.has_module_perms(required_perms)


def is_staff(function=None, required_perms=(),
             redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.

    Required perms can a string with module name, individual permission,
    multiple permissions (list/tuple) or a list/tuple with multiple
    permissions. In the later case, access is granted if any of permissions
    list grants access to the user.
    """
    def is_staff_and_has_perms(user):
        if user.is_authenticated() and user.is_active and user.is_staff:
            if user.is_superuser:
                return True

            if isinstance(required_perms, basestring):
                # 'qwf' / 'zxc.vbb'
                return _check_perms(user, required_perms)
            elif (
                isinstance(required_perms, (list, tuple)) and
                required_perms and
                isinstance(required_perms[0], (list, tuple))):
                # ('foo.bar', 'qwe.ars'), ('zxc',)
                return any(
                    all(_check_perms(user, perm) for perm in perms)
                    for perms in required_perms)
            else:
                # ('ars.stdt', 'zxc.cvb')
                return all(_check_perms(user, perm) for perm in required_perms)

    actual_decorator = auto_adapt_to_methods(user_passes_test(
        lambda u: is_staff_and_has_perms(u),
            login_url='/admin/login/',
        redirect_field_name=redirect_field_name))
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
