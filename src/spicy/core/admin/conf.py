import functools
import importlib
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.functional import SimpleLazyObject, new_method_proxy
from django.utils.translation import ugettext_lazy as _
from spicy.utils.printing import print_info
from . import defaults


class AdminLink(object):
    url_ns = None
    label = None

    def __init__(self, url_ns, label):
        self.url_ns = url_ns
        self.label = label

    @property
    def url(self):
        if isinstance(self.url_ns, tuple):
            if len(self.url_ns) > 1:
                return reverse(self.url_ns[0], args=self.url_ns[1:])
            return reverse(self.url_ns[0])

        elif isinstance(self.url_ns, basestring):
            return reverse(self.url_ns, args=[])
        raise TypeError


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
    perms = Perms(view=[], write=[], manage=[])

    def __init__(self):
        pass

    def edit_url(self, args=[0,]):        
        try:
            return reverse(self.name + ':admin:edit', args=args)
        except NoReverseMatch:
            if settings.DEBUG:
                print_info('AppAdmin [{0}] has no admin:edit url'.format(self.name))
        

    # uncomment only in the working admin app module
    #@render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    # uncomment only in the working admin app module
    #@render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


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
