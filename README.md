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

####Custom User Profile
В этом разделе описана последовательность действий с примером кода, которая позволит создать кастомную модель профайла.
Например, вы хотите добавить поля skype и sms_notification к модели пользователя. Для этого необходимо:

1) запустить проект со схемой данных для базового профайла

* в бд вы получаете таблицу test_profile, без дополнительных полей
* в коде класс-модель profile.TestProfile, без дополнительных полей

2) создать новую ветку в проекте (apps.webapp), перейти на нее и расширить модель профайла нужными полями

<pre>
class CustomProfile(AbstractProfile):
    sms_notification = models.BooleanField(_('Use SMS notification'), blank=True, default=False)
    skype = models.CharField(_('Skype'), max_length=255, blank=True, null=True)

    class Meta:
        abstract = False
        db_table = 'test_profile'
</pre>

3) добавить в settings.py настройку новой модели профайла

<pre>CUSTOM_USER_MODEL = 'webapp.CustomProfile'</pre>

* в бд остается таблица test_profile, без дополнительных полей
* в коде начинает использоваться класс-модель CustomProfile, с расширенным набором полей

4) сделать патч таблицы профайла tet_profile - добавить новые поля модели (внутри контейнера db)

<pre>
begin;
alter table test_profile add column sms_notification boolean default False;
alter table test_profile add column skype varchar(255);
commit;
</pre>

* в бд таблица test_profile расширена полями
* в коде используется расширенный класс пользователя webapp.CustomProfile

5) сделать патч системных таблиц Django - заменить на уровне бд customprofile на test_profile, чтобы сохранить старые данные пользователей (внутри контейнера db)

<pre>
begin;
SELECT django_content_type.id into test_id FROM django_content_type WHERE app_label = 'profile' AND model = 'testprofile';
SELECT django_content_type.id into custom_id FROM django_content_type WHERE app_label = 'webapp' AND model = 'customprofile';

update auth_permission set content_type_id = (select * from test_id) where content_type_id = (select * from custom_id);
delete from django_content_type where id = (select * from custom_id);
update django_content_type set app_label = 'webapp', model = 'customprofile' where id=(select * from test_id);


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
