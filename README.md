[![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core)  [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage)

==========
Spicy docs
==========

Fixed version 1.2.0

Main and the one using case:

.. code-block:: sh
   `spicy -h`

TODO: write readme in plain text at least

Features at a glance
====================

- Support for Django >= 1.3 <= 1.5.12
- Python 2.7 support

How to Use
==========

Get the code
------------

Getting the code for the latest stable release use 'pip'. ::

   git+https://gitlab.com/spicycms.com/spicy.core.git@1.2.0#egg=spicy
   

Install in your project
-----------------------

your project's settings. ::

    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/signin/'
    REGISTRATION_OPEN = True

    LOGIN_URL = '/signin/'
    LOGIN_REDIRECT_URL = '/'

    AUTHENTICATION_BACKENDS = (
        'spicy.core.profile.auth_backends.CustomUserModelBackend',
    )

    SERVICES = (
        'spicy.core.profile.services.ProfileService',
        'spicy.core.trash.services.TrashService',
    ) 

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
        'spicy.core.trash',
        'spicy.core.admin',
        'spicy.core.service',
        'spicy.core.siteskin',
        'spicy.core.simplepages',
    )

    STATICFILES_FINDERS = (
        'spicy.core.siteskin.loaders.ThemeStaticFinder',
        'spicy.core.siteskin.loaders.AppDirectoriesFinder',
    )
    
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
    
    MIDDLEWARE_CLASSES = (
        'spicy.core.siteskin.middleware.AjaxMiddleware',
        'spicy.core.siteskin.threadlocals.ThreadLocals',
    )
    
    if DEBUG:
    MIDDLEWARE_CLASSES += (
        # for developers
        'spicy.core.rmanager.middleware.ProfileMiddleware',
    )


    
   
Docs
----
TODO: write docs
TODO: custom User Profile, forms create and edit templates
TODO: use API service
TODO: base templates for admin panel and formfield
TODO: templates tag and filter

Tools
-----
TODO: add used tools


And you must remember
---------------------

People, who creates your software, in most cases are same to you are. So, you must know: in theory they could be murderers or maniacs, or, even a women. So, it's much better for **you** to write *good* code. You have been warned.
