"""Test settings."""

import sys, os

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


INSTALLED_APPS = [
    # Dajngo admin
    'django.contrib.admin',

    # Django native apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',

    # spicy.core components
    'spicy.core.profile',
    'spicy.core.admin',
    'spicy.core.service',
    'spicy.core.siteskin',
    'spicy.core.simplepages',
    'spicy.core.rmanager',

    #
    'captcha',
    'django_nose',
]

ROOT_URLCONF = 'spicy.tests.urls'

SITE_ID = 1

SECRET_KEY = 'test secret key'

SERVICES = [
    'spicy.core.profile.services.ProfileService',
    'spicy.core.trash.services.TrashService',
]

# use specific example themes path for tests
SITESKINS_PATH = os.path.abspath('src/spicy/siteskin-examples')


TEMPLATE_LOADERS = (
    'spicy.core.siteskin.loaders.ThemeTemplateLoader',
    'django.template.loaders.app_directories.Loader',
    'spicy.core.siteskin.loaders.BackendTemplateLoader',
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(SITESKINS_PATH, STATIC_URL))

STATICFILES_FINDERS = (
    'spicy.core.siteskin.loaders.ThemeStaticFinder',
    'spicy.core.siteskin.loaders.AppDirectoriesFinder',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    
    'spicy.core.profile.middleware.AuthMiddleware',
    
    'django.middleware.doc.XViewMiddleware',
    
    # XXX is it required ??
    'spicy.core.siteskin.middleware.AjaxMiddleware',
    'spicy.core.siteskin.threadlocals.ThreadLocals', )

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
}

if DEBUG:
    MIDDLEWARE_CLASSES += (
        # Peofiler for developers
        'spicy.core.rmanager.middleware.ProfileMiddleware',
        # error with profile.Profile module
    )
