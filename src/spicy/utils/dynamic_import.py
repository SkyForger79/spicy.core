import sys, traceback
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from spicy.utils.printing import print_text, print_error

def load_module(path, config='SERVICE'):
    module, attr = path.rsplit('.', -1)
    print module
    try:
        mod = import_module(module, attr)
        print 'ok', mod
        return getattr(mod, attr)

    except ImportError, e:
        print_text(traceback.format_exc())
        raise ImproperlyConfigured(
            'Error importing module %s: "%s"' % (module, e))
    except ValueError, e:
        print_text(traceback.format_exc())
        raise ImproperlyConfigured(
            'Error importing module. Is %s a correctly defined list or tuple?'
            % config)
