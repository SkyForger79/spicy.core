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

TEST = 'test' in sys.argv

if TEST:
    # in-memory SQLite used for testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

else:
    DATABASES = {
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #     'NAME': 'spicycms',
        #     'USER': 'postgres',
        #     'PASSWORD': 'postgres',
        #     'HOST': 'localhost',
        #     'PORT': '5432',
        #     },
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'spicy.db',
            'TEST_NAME': 'test_spicy.db',
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
    'django_nose',
]

ROOT_URLCONF = 'spicy.core.profile.tests.dummy_root_urls'

SITE_ID = 1

SECRET_KEY = 'test secret key'
