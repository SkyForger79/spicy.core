"""Test settings."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# TEST_RUNNER = 'spicy.spicyunittest.SpicyTextTestRunner'
NOSE_ARGS = [
    # '--nocapture',
    # '--with-coverage',
    # '--cover-html',
    # '--cover-html-dir=cover',
    # '--cover-package=spicy',
]

# NOSE_PLUGINS = [
#
# ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'spicy_test.db',
    }
}

AUTHENTICATION_BACKENDS = (
    'spicy.core.profile.auth_backends.CustomUserModelBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/signin/'
REGISTRATION_OPEN = True

INSTALLED_APPS = (
     # Django native apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Spicy core components
    'spicy.core.profile',
    'spicy.core.trash',
    'spicy.core.admin',
    'spicy.core.service',
    'spicy.core.siteskin',
    'spicy.core.simplepages',
)

ROOT_URLCONF = 'spicy.tests.urls'

SITE_ID = 1

SECRET_KEY = 'test secret key'

SERVICES = (
    # 'spicy.core.profile.services.ProfileService',
    # 'spicy.core.trash.services.TrashService',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'spicy.core.siteskin.loaders.ThemeTemplateLoader',
    'spicy.core.siteskin.loaders.BackendTemplateLoader',
)

STATIC_URL = 'static'

STATICFILES_FINDERS = (
    'spicy.core.siteskin.loaders.ThemeStaticFinder',
    'spicy.core.siteskin.loaders.AppDirectoriesFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',

    'spicy.core.profile.context_processors.auth',
    'spicy.core.siteskin.context_processors.base',
    'spicy.core.admin.context_processors.base',

    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'spicy.core.siteskin.middleware.AjaxMiddleware',
    'spicy.core.siteskin.threadlocals.ThreadLocals',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# if DEBUG:
#     MIDDLEWARE_CLASSES += (
#         'spicy.core.rmanager.middleware.ProfileMiddleware',
#     )
