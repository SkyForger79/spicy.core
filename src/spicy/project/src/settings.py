import os, sys

from django import template

# debug color styles
from django.core.management.color import color_style

style = color_style()

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Moscow'

#LANGUAGES = (
#    ('ru_ru', _('Russian')),
#    ('en_us', _('English')),
#)

LANGUAGE_CODE = 'ru'
USE_I18N = True
USE_L10N = True

PROJECT_ROOT = os.path.abspath('.')

DEBUG = True
SITE_ID = 1
SITESKIN = 'example.com'

MEDIACENTER_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIACENTER_URL = '/media-root/'

SERVER_EMAIL = 'no-reply@example.com'
DEFAULT_FROM_EMAIL = 'no-reply@example.com'
EMAIL_HOST='localhost'
EMAIL_PORT='25'
#EMAIL_HOST_PASSWORD=''
#EMAIL_HOST_USER='support'
#EMAIL_BACKEND

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_NOISE_FUNCTIONS = tuple()#('captcha.helpers.noise_arcs','captcha.helpers.noise_dots',)

CACHE_PREFIX = '%s-' % SITESKIN
CACHE_BACKEND = 'locmem://'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

#SECRET_KEY = 'sdfk(klasdfj;;;asdfklklsdafopiasdfkl;l;asdf0-90*$%=9klsdj90'
LOGIN_URL = '/signin/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'spicy.core.profile.auth_backends.CustomUserModelBackend',
)


_ = lambda x: x


TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
    )


REPOSITORY_TYPE = 'hg'
APP_SOURCE_PATH = 'src/'
ADDITIONAL_PYTHON_PATH = 'dev_apps/'

sys.path.insert(0, os.path.join(PROJECT_ROOT, APP_SOURCE_PATH))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ADDITIONAL_PYTHON_PATH))

# app don't see spicy in the dev_apps directory before importing local config
#from spicy.core.service.default import * # OBJECTS_PER_PAGE or VERSIONS ???
#from spicy.apps.presscenter.defaults import *
#from spicy.apps.mediacenter.defaults import *
#from spicy.core.siteskin.defaults import *
#from spicy.core.profile.defaults import *
# TODO auto import for default settings
#from spicy.apps.feedback.defaults import *


# local configuration imports
try:
    from config import *

    # XXX conflict or sys path dublicate is possible
    sys.path.insert(0, os.path.join(PROJECT_ROOT, APP_SOURCE_PATH))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, ADDITIONAL_PYTHON_PATH))

except ImportError, msg:
    print msg
    raise ImportError, style.ERROR('Using default config settings, check "config" directory.\n')

MEDIA_ROOT = os.path.abspath(PROJECT_ROOT + MEDIA_ROOT)

# rmanager imports
import src._version
VERSION = src._version.version.short()


SERVICES = (
    #'spicy.apps.mediacenter.services.MediaService',
    'spicy.core.profile.services.ExtProfileService',

    #'spicy.apps.trash.services.TrashService',    
    #'spicy.apps.history.services.HistoryService',
    )


from django.utils.translation import ugettext_lazy as _

MESSAGES = {'success': _('Changes were successfully saved.'),
            'error': _('Please, correct the errors below.')}

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale'), )

TEST_RUNNER = 'django_nose.runner.NoseTestSuiteRunner'
NOSE_ARGS = ['-v', '--with-color']

ROOT_URLCONF = 'src.urls'


TEMPLATE_LOADERS = (
    #'siteskin.template.loaders.SiteLoader',

    'django.template.loaders.filesystem.Loader',

    #'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)
template.add_to_builtins('django.templatetags.i18n')

TEMPLATE_CONTEXT_PROCESSORS = (
    'spicy.core.profile.context_processors.auth', # ???   
    'spicy.core.siteskin.context_processors.base', # ???   

    #'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',

    )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.locale.LocaleMiddleware', - don't use it =)
    'django.middleware.common.CommonMiddleware',

    'spicy.core.profile.middleware.AuthMiddleware',

    'django.middleware.doc.XViewMiddleware',

    # XXX is it required ??
    #'spicy.core.siteskin.middleware.AjaxMiddleware',
    #'spicy.core.siteskin.threadlocals.ThreadLocals',
)

if DEBUG:
    MIDDLEWARE_CLASSES += (

        # for developers 
        'spicy.core.rmanager.middleware.ProfileMiddleware', # error with profile.Profile module
        'spicy.core.rmanager.middleware.CallgraphMiddleware', # error with profile.Profile module
        )


INSTALLED_APPS = [
     # Django native apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    
    # Core components    
    'spicy.core.service',
    'spicy.core.siteskin', 
    #'spicy.apps.presscenter',
    #'spicy.apps.mediacenter',
    #'spicy.core.profile',

    #'spicy.apps.feedback',
    #'spicy.apps.categories',    
    #'spicy.apps.labels',
    #'spicy.apps.comments',
    #'spicy.apps.polls',

    'account',

    # additional requirements party apps
    'sorl.thumbnail',
    'django_nose',
    'captcha',
    'pytils',

    # TODO Make system info in the 'rmanager'
    # mamcache, DESIGN_VERSION and etc..., or aggregate versions 
    # from the components
    'spicy.core.rmanager',
]


# Hack for adding extra apps in local config.
try:
    INSTALLED_APPS.extend(EXTRA_APPS)
except NameError:
    pass



