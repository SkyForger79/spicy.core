"""Test settings."""
import sys

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

    # Core components
    'spicy.core.profile',
    'spicy.core.admin',
    'spicy.core.service',
    'spicy.core.siteskin',
    'spicy.core.simplepages',
    'spicy.core.rmanager',
    'django_nose',
]

ROOT_URLCONF = 'spicy.tests.dummy_root_urls'

SITE_ID = 1

SECRET_KEY = 'test secret key'

SERVICES = [

]
