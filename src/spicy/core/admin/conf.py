import functools
import importlib
import operator
import urllib
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Q
from django.utils.functional import SimpleLazyObject, new_method_proxy
from django.utils.translation import ugettext_lazy as _
from spicy.utils.printing import print_info
from . import defaults


class AdminLink(object):
    url_ns = None
    label = None

    def __init__(
            self, url_ns, label, counter=None, icon_class='icon-edit',
            perms=None, params=None):
        self.url_ns = url_ns
        self.label = label
        self.counter = counter
        self.icon_class = icon_class
        self.perms = perms
        self.params = None

    @property
    def url(self):
        if isinstance(self.url_ns, tuple):
            if len(self.url_ns) > 1:
                return reverse(
                    self.url_ns[0], args=self.url_ns[1:]) + self.get_params()
            return reverse(self.url_ns[0]) + self.get_params()

        elif isinstance(self.url_ns, basestring):
            return reverse(self.url_ns, args=[]) + self.get_params()
        raise TypeError

    def get_counter(self, user):
        return self.counter(user) if callable(self.counter) else self.counter

    def get_params(self):
        if self.params:
            return '?' + urllib.urlencode(self.params)
        else:
            return ''


def check_perms(user, perms=None):
    if perms is None:
        return True
    elif isinstance(perms, bool):
        return perms
    elif isinstance(perms, basestring):
        return user.has_perm(perms)
    else:
        return functools.reduce(
            lambda perm1, perm2: (
                operator.and_ if perms.connector == Q.AND else operator.or_
            )(check_perms(user, perm1), check_perms(user, perm2)),
            perms.children)


class DashboardList(object):
    def __init__(
            self, title, edit_url, queryset, date_field=None, perms=None):
        self.title = title
        self.edit_url = edit_url
        self.queryset = queryset
        self.date_field = date_field
        self.perms = perms

    def get_data(self, user):
        queryset = (
            self.queryset(user) if callable(self.queryset) else self.queryset)
        for obj in queryset[:defaults.DASHBOARD_LISTS_LENGTH]:
            yield {
                'object': obj,
                'date': getattr(
                    obj, self.date_field) if self.date_field else None,
                'edit_url': reverse(self.edit_url, args=[obj.pk])}


# TODO delete this useless class?
class Perms(object):
    def __init__(self, view=None, write=None, manage=None):
        self._view = view
        self._write = write
        self._manage = manage

    def check(self):
        pass

    def view(self):
        return True

    def write(self):
        return True

    def manage(self):
        return True


class AdminAppBase(object):
    """
    menu_items = (
        AdminLink('mediacenter:admin:create', _('Create library')),
        AdminLink('mediacenter:admin:index', _('All libraries')),
        )

    create = AdminLink('mediacenter:admin:create', _('Create library'),)
    """
    order_number = 0
    name = 'admin'
    label = _('Admin')

    menu_items = tuple()

    create = None
    dashboard_links = None
    dashboard_lists = None

    def edit_url(self, args=[0]):
        try:
            return reverse(self.name + ':admin:edit', args=args)
        except NoReverseMatch:
            if settings.DEBUG:
                print_info(
                    'AppAdmin [{0}] has no admin:edit url'.format(self.name))

    def menu(self, request, *args, **kwargs):
        raise NotImplementedError()

    def dashboard(self, request, *args, **kwargs):
        raise NotImplementedError()

    def any_perms(self, user):
        for link in self.menu_items:
            if check_perms(user, link.perms):
                return True
        else:
            return False


def _find_modules(admin_apps=True, spicy_app=False):
    _register = {}
    for app_name in settings.INSTALLED_APPS:
        app_import_name = app_name
        
        #if spicy_app:
        #    if not 'spicy.' in app_name:
        #        continue

        if admin_apps:
            app_import_name += '.admin'
        try:
            app_mod = importlib.import_module(app_import_name)
            _register[app_name] = (
                getattr(app_mod, 'AdminApp')() if admin_apps else app_mod)

            if defaults.DEBUG_ADMIN and admin_apps:
                print_info('Use Spicy AdminApp for: {0}'.format(app_name))
        except (ImportError, AttributeError):
            if defaults.DEBUG_ADMIN and admin_apps:
                print_info('Can not find AdminApp for: {0}'.format(app_name))
    return _register


class BackportedSimpleLazyObject(SimpleLazyObject):
    """
    This class is not needed in django 1.5 - just use SimpleLazyObject instead.
    """
    # Dictionary methods support
    @new_method_proxy
    def __getitem__(self, key):
        return self[key]

    @new_method_proxy
    def __setitem__(self, key, value):
        self[key] = value

    @new_method_proxy
    def __delitem__(self, key):
        del self[key]

admin_apps_register = BackportedSimpleLazyObject(_find_modules)
app_modules_register = BackportedSimpleLazyObject(
    functools.partial(_find_modules, admin_apps=False))
