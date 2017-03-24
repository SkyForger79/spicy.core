spicy.core.profile
******************

Назначение
==================
spicy.core.profile является модулем spicy.core. Позволяет управлять учетными записями на сайте, настраивать механизмы регистрации и авторизации, поддерживает работу с социальными сетями, email-рассылкой, разделением прав доступа по группам. Позволяет распределять пользователей между несколькими сайтами посредством `django sites framework <https://djbook.ru/rel1.4/ref/contrib/sites.html>`_.

Аналоги
=======

* `django-registration-renux <https://github.com/macropin/django-registration>`_ 
* `django-registration <https://github.com/ubernostrum/django-registration>`_ 
* `django-allauth <https://github.com/pennersr/django-allauth>`_ 

Эти приложения требуют Django 1.8+, spicy.core.profile позволяет использовать Django 1.3-1.5 и реализует дополнительные возможности, которых нет в django-registration-renux и django-registration - интеграцию с соцсетями, разделение прав доступа.


Для администратора сайта
========================

Статусы пользователей
---------------------
По умолчанию новый пользователь, который регистрируется в системе, не имеет статуса. При этом на указанную почту отправляется активационная ссылка, при переходе по ней, присваивается статус Активный. Можно также включить режим ручной активации, в этом случае пользователь после регистрации будет иметь статус Забанен, и нужно будет активировать его вручную через админку.

Можно настраивать доступ пользователя к сайту с помощью статусов:

* активный - может просматривать публичные страницы сайта, оставлять комментарии, добавлять контент через интерфейс сайта; не имеет доступ в административную часть
* забанен - может просматривать публичные страницы; не может оставлять комментарии, добавлять контент через интерфейс; не имеет доступ в административную часть; рассматривается как анонимный пользователь.

Также каждому пользователю можно назначить 2 привелегированных статуса:

* персонал - пользователь имеет полный доступ к публичной части сайта; имеет доступ к административной части, ограниченный личными и групповыми правами 
* суперпользователь - имеет полный доступ к публичной и административной частям сайта

Управление правами доступа
--------------------------
Для разделения доступа к разделам могут быть использованы личные и групповые права. Они используются в SpicyCMS для ограничения доступа к модулям проекта в административной части. Но также могут быть использованы в публичной части, подробнее 
в `документации Django о правах пользователя <https://djbook.ru/rel1.4/topics/auth.html#django.contrib.auth.decorators.permission_required>`_.

Для каждого модуля SpicyCMS используется 3 типа прав:

* can add <Object> - пользователь может добавлять объекты, но не может видеть список
* can change <Object> - пользователь может реактировать объекты и видеть список
* can delete <Object> - пользователь может удалять объекты, но ему не доступен общий список (рекомендуется использовать совместно с can change <Object>)

Групповые и личные права объединяются для каждого пользователя. Так вы можете управлять доступом для нескольких пользователей через права группы и для каждого в отдельности выделять особые права, которые откроют доступ к разделам, не доступным другим членам группы.
У суперпользователя права не проверяются.


Для Django программиста
=======================

spicy.core.profile предоставляет абстрактный базовый класс для профиля пользователя ``models.AbstractProfile``, который наследуется от `Django auth.User <https://djbook.ru/rel1.4/topics/auth.html#users>`_ и связан с ним через ``OneToOneField(User, parent_link=True)``.

По умолчанию в проектах используется модель ``models.TestProfile``, унаследованная от ``AbstractProfile``. Чтобы в вашем приложении получить доступ к классу ``TestProfile`` используйте следующий код: ::

  # yourapp.*.py
  from spicy.core.profile import defaults as pf_defaults
  from spicy.utils import get_custom_model_class
  
  Profile = get_custom_model_class(pf_defaults.CUSTOM_USER_MODEL)

Делаем свою модель профайла
---------------------------
Вы можете использовать собственную модель профайла, для этого в settings.py укажите: ::

  CUSTOM_USER_MODEL = 'yourapp.models.CustomProfile'
  
И определите модель, которая будет использована. Необходимо указать ``Meta.abstract = False``, чтобы Django создала таблицу в базе данных. ::

  # yourapp.models.py
  from spicy.core.profile.models import AbstractProfile
 
  class CustomProfile(AbstractProfile):
    # your additional fields
    class Meta:
      abstract = False

Чтобы с новой моделью можно было работать из админки, необходимо переопределить формы, используемые по умолчанию, и указать их в настройках: ::  
  
  # yourapp.forms.py
  from spicy.core.profile import defaults as pf_defaults
  from spicy.utils import get_custom_model_class
  
  Profile = get_custom_model_class(pf_defaults.CUSTOM_USER_MODEL)
  
  class CreateCustomProfileForm(pr_forms.CreateProfileForm):
    #your additional fields  
    class Meta:
      model = Profile
      
  class EditCustomProfileForm(pr_forms.ProfileForm):
    #your additional fields  
    class Meta:
      model = Profile
      
  # settings.py
  ADMIN_CREATE_PROFILE_FORM = 'yourapp.forms.CreateCustomProfileForm'
  ADMIN_EDIT_PROFILE_FORM = 'yourapp.forms.EditCustomProfileForm'
  
Делаем свою форму восстановления пароля
---------------------------------------
RESTORE_PASSWORD_FORM
  
Управление регистрацией и авторизацией пользователя
---------------------------------------------------
SpicyCMS позволяет настроить регистрацию пользователя для каждого проекта. Например, указать допустимые символы для автогенерации пароля, срок жизни активационной ссылки и т.п. Это реализуется с помощью настроек settings.py. 

Указать допустимые символы для автоматической генерации пароля. По умолчанию используются ``[a-zA-Z2-9]`` ::

  ACCOUNT_ALLOWED_CHARS = 'your symbols as one string without spacing'
  
Максимальная длина username при регистрации нового пользователя. Используется когда в форме регистрации не задается username, в этом случае будет сгенерирован уникальный логин на основе введенного email. По умолчанию 100 символов ::

  USERNAME_MAX_LENGTH = 100 
  
Задать регулярное выражения для генерации активационного ключа. Используется при активации пользователя. По умолчанию ``[a-f0-9]{40}`` ::

  import re
  SHA1_RE = re.compile('your regex') 
  
Изменить время жизни активационной ссылки. По умолчанию 2 дня ::

  ACCOUNT_ACTIVATION_DAYS = 2
  
Запретить регистрацию в системе через публичную часть сайта. По умолчанию значение True - регистрация возможна ::

  REGISTRATION_ENABLED = False
  
Эта директива не запрещает регистрацию напрямую, но она позволяет скрыть блоки регистрации в шаблонах авторизации и регистрации, добавляя переменную REGISTRATION_ENABLED в их контекст: ::

  # your overwritten spicy.core.profile/signup.html 
  # or/and spicy.core.profile/login.html
  ...
  {% if REGISTRATION_ENABLED %}
    {# display signup form #}
  {% else %}
    {# display 'sorry, registration is not available' #}
  {% endif %}

Настроить ручную активацию пользователей. По умолчанию после регистрации пользователь может сам активировать учетную запись, перейдя по ссылке, отправленной на почту. Можно включить ручную активацию через админку. Значение по умолчанию False ::

  MANUAL_ACTIVATION = True

Отключить уведомление менеджеров о регистрации нового пользователя. По умолчанию значение True - менеджерам приходят сообщения при регистрации новых учетных записей ::

  NOTIFY_MANAGERS = False

Включить использоание капчи при регистрации и входе пользователя, смене пароля, задании email пользователя через интерфейс сайта. По умолчанию значение True - капча включена ::

  USE_CAPTCHA = False
  
Включить логирование попыток входа в систему. По умолчанию значение False - логирование выключено ::

  LOGIN_WARNING = True

Настроить защиту аккаунтов от подбора паролей
---------------------------------------------
SpicyCMS позволяет отлавливать попытки подбора логинов и паролей. По умолчанию это поведение отключено - значение False, но вы можете активировать с помощью настройки ``BRUTEFORCE_CHECK`` ::
  
  BRUTEFORCE_CHECK = True
  
Система будет отлавливать попытки авторизации пользователя, и при количестве попыток, большем 5, будет показана капча. При количестве попыток больше 20, запретит вход с этого IP, посчитав его попыткой взлома аккаунта.  

Делаем свою модель для связи пользователя и группы
------------------------------------------------------------------------------
По умолчанию для связи пользователя с группой используется модель ``spicy.core.profile.models.PermissionProviderModel``, которая по FK ссылается на учетную запись и на грруппу. Вы можете переопределить саму модель связи и также переопределить модель группы, используемой по умолчанию - `Django auth.Group <https://djbook.ru/rel1.4/topics/auth.html#django.contrib.auth.models.Group>`_.

Для того, чтобы переопределить модель связи пользователь-группа, укажите в settings.py: ::

  CUSTOM_PERMISSION_PROVIDER_MODEL = 'yourapp.models.CustomRepmissionProviderModel'
  
И определите саму модель в проекте, унаследовав ее от ``ProviderModel``: ::

  # yourapp.models.py
  from spicy.core.profile import defaults as pf_defaults
  from spicy.core.service.models import ProviderModel
  
  class CustomRepmissionProviderModel(ProviderModel):
    profile = models.ForeignKey(defaults.CUSTOM_USER_MODEL, null=False, blank=False)  # this is required field
    role = models.ForeignKey(defaults.CUSTOM_ROLE_MODEL, null=False, blank=False)     # this is required field 
    # your additional fields
    
    class Meta:
      unique_together = 'profile', 'consumer_id', 'consumer_type' # required option
      # your additional options
  
Аналогично вы можете переопределить модель группы. Укажите в settings.py: ::

  CUSTOM_ROLE_MODEL = 'yourapp.models.CustomGroup'
  
И определите модель: ::

  # yourapp.models.py
  from django.contrib.auth.models import Group
  
  class CustomGroup(Group):
    # your additional fields
    
Команды manage.py
-----------------

Добавление группы нескольким пользователям ::

  {TODO починить вызов Profile}

Группа должна быть указана по id, логины пользователей - в файле, каждый логин с новой строки. Указание флага ``--test`` позволет активировать пользователей, без указания статус пользователей не изменяется.

Смена пароля для пользователя `django.contrib.auth <https://djbook.ru/rel1.4/topics/auth.html>`_ с указанным email - команда ``changepassword``::

  Usage: manage.py changepassword [options] 

  Options:
    -v VERBOSITY, --verbosity=VERBOSITY
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
    --settings=SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
    --pythonpath=PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
    --traceback           Print traceback on exception
    --database=DATABASE   Specifies the database to use. Default is "default".
    --version             show program's version number and exit
    -h, --help            show this help message and exit

Удалить из базы данных профили пользователей, с истекшим сроком - команда ``cleanup_expired_profiles`` ::

  {TODO починить вызов Profile}

Создание суперпользователя, учитывается возможность переопределения модели профиля - команда ``createsuperuser`` ::

  Usage: manage.py createsuperuser [options] 

  Options:
    -v VERBOSITY, --verbosity=VERBOSITY
                          Verbosity level; 0=minimal output, 1=normal output,
                          2=verbose output, 3=very verbose output
    --settings=SETTINGS   The Python path to a settings module, e.g.
                          "myproject.settings.main". If this isn't provided, the
                          DJANGO_SETTINGS_MODULE environment variable will be
                          used.
    --pythonpath=PYTHONPATH
                          A directory to add to the Python path, e.g.
                          "/home/djangoprojects/myproject".
    --traceback           Print traceback on exception
    --email=EMAIL         Specifies the email address for the superuser.
    --noinput             Tells Django to NOT prompt the user for input of any
                          kind. You must use --email with --noinput, and
                          superusers created with --noinput will not be able to
                          log in until they're given a valid password.
    --version             show program's version number and exit
    -h, --help            show this help message and exit

  
{TODO} декораторы, контекстные процессоры


Для верстальщика
===============
{TODO} Описать возможности переопределения шаблонов по умолчанию, переменные контекстных процессоров


