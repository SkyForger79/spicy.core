spicy.core.siteskin
*******************

Модуль является частью spicy.core и предназначен для управления оформлением сайта посредством тем. 
Основной особенностью spicy.core.siteskin является то, что вы можете использовать как темы модулей, предоставляемые по умолчанию, так и переопределять их в своем приложении.

Такой механизм обеспечивается модульностью продукта SpicyCMS. Каждый модуль вмещает в себя набор необходимых шаблонов.
Если вы переопределите какой-либо из них в своем приложении, повторив структуру папок модуля, то будет использован  именно ваш шаблон, иначе - spicy.core.siteskin подгрузит интегрированный в модуль spicy.

Пример использования темы
=========================

* `Две темы <https://gitlab.com/spicycms.com/cms.chiefeditor/tree/develop/siteskins#%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B5-%D1%81%D0%BA%D0%B8%D0%BD%D0%B0>`_, включенные по умолчанию в SpicyCMS Chief Editor {TODO заменить dev-ссылку на смерженный код}

* {TODO ссылка на настройки в CMS CE для Django программиста}

* {TODO ссылка на демо админки CMS CE, раздел Темы}

Для верстальщика
================

Переопределяем шаблон модуля SpicyCMS
-------------------------------------
Вы можете переопределить любой из предоставляемых по умолчанию шаблонов, для добавления своих стилей, js, изменения верстки. Структуру шаблонов всех модулей, используемых в SpicyCMS вы можете найти `здесь <https://gitlab.com/spicycms.com/cms.chiefeditor/tree/master/siteskins#%D0%A1%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%B0-%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3%D0%BE%D0%B2-%D1%82%D0%B5%D0%BC-%D0%B4%D0%BB%D1%8F-%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D0%B5%D0%B9-spicycms-chief-editor>`_.

Например, вы хотите изменить файл страницы входа в систему - в модуле spicy.core.profile, который имеет приведенную ниже структуру. Для этого вам достаточно повторить в проекте структуру каталога до ``login.html``: ::

  your/app/template/folder
  └── spicy.core.profile
      └── login.html      # your custom login template
      
При этом spicy.core.siteskin использует ваш файл login.html, а другие шаблоны загрузит из spicy.core.profile. Аналогичным образом вы можете заменять любой шаблон, который SpicyCMS использует по умолчанию.

Структура шаблонов модуля `spicy.core.profile <../profile/README.rst>`_: ::

  spicy.core/src/spicy/core/profile/templates
  └── spicy.core.profile
      ├── activate.html
      ├── admin                             
      │   └── ... admin templates
      ├── edit.html
      ├── login.html
      ├── mail
      │   └── ... mail templates
      ├── passwd.html
      ├── profile.html
      ├── restore_password.html
      ├── set_email.html
      ├── signin.html
      ├── signup.html
      ├── social
      │   └── ... social templates
      ├── success_signup.html
      ├── user_agreement.html
      └── widgets
          ├── signin_form.html
          └── signup_form.html

Шаблонные теги spiy.core.siteskin
---------------------------------
spicy.core.siteskin предоставляет несколько тегов, которые ускоряют работу с частыми действиями в шаблонах - постраничный вывод объектов, вставка другого шаблона, для которого необходим предварительный рендеринг на сервере, фильтрация и вывод объектов напрямую в шаблоне. некоторые из тегов требуют дополнительные действия на серверной стороне - добавление переменных в контекст шаблона, подробнее в разделе `Настройка шаблонных тегов spicy.core.siteskin <./README.rst#Настройка-шаблонных-тегов-spicycoresiteskin>`_.

Для использования тегов, связанных с постраничным выводом - ``pagination``, ``sk_pagination``, ``paginate`` укажите в шаблоне: ::

  {% load pagination %}
  
Тег ``pagination`` реализует постраничный вывод объектов на странице. Используется верстка пажинатора из ``'spicy.core.admin/admin/pagination.html'``. C помощью ``paginator`` в контексте вы можете проверять, имеет ли текущая страница следующую, чтобы скрывать пажинатор. Пример использования: ::

  {% if paginator.current_page.has_next %}
    {% pagination %}
  {% endif %}
  


{TODO шаблонные теги, переменные контекстного процессора, виджеты}

Для Django программиста
=======================

Настройка шаблонных тегов spicy.core.siteskin
---------------------------------------------

Некоторые теги требуют добавления переменных в контекст шаблона, ниже приведена инструкция по их настройке.

Для работы тега ``pagination`` вы должны добавить в контекст шаблона переменную ``paginator`` - объект `django.core.paginator.Paginator <https://djbook.ru/rel1.4/topics/pagination.html#django.core.paginator.Paginator>`_.

Декораторы spicy.core.siteskin
------------------------------
spicy.core.siteskin предоставляет декораторы, облегчающие работу со темами - ``render_to``, ``ajax_request``, ``multi_view``. Их удобство в том, что разработчик освобождается от написания типичного кода для создания и возврата объекта ответа, настроек кэширования: ::

  # typical views.py
  from django.shortcuts import render
  
  def your_view(*args, **kwargs):
    # logic here
    template = 'path/to/template.html'
    context = dict(param1=value, param2=value, ...)
    response = render(request, template, context)
    return response
  
Вместо этого ваши вью будут возвращать словарь, который декоратор ``render_to`` передаст <./#>`_ в указанный шаблон. Также каждый декоратор имеет дополнительные аргументы, позволяющие настраивать кэширование, загрузчики, которые будут использованы для поиска шаблона и т.д. (подробнее в `Общие аргументы декораторов <./README.rst#Общие-аргументы-декораторов>`_). Пример использования: ::

  # yourapp.views.py
  from spicy.core.siteskin.decorators import render_to
  
  @render_to(template_name, # additional args)
  def your_view(request):
    # logic here
    context = dict(param1=value, param2=value, ...)
    return context
    
Обязательным аргументом декоратора является ``template_name`` - имя шаблона, куда будет передан контекст.

Декоратор ``multi_view`` работает аналогично с ``render_to``, но позволяет указывать шаблон в ходе выполнения обработчика. Это может быть полезно, если выбор шаблона происходит по какому-либо условию. Чтобы использовать шаблон, вы должны добавить его в возвращаемый контекст по ключу ``'template'``: ::

  # yourapp.views.py
  from spicy.core.siteskin.decorators import multi_view
  
  @multi_view(# additional args)
  def your_view(request):
    # logic here
    if condition:
      template = 'path/to/true/template.html'
    else:
      template = 'path/to/false/template.html'
    context = dict(template=template, param1=value, param2=value, ...)
    return context

Декоратор ``ajax_request`` возвращает ``HttpResponse`` с ``mimetype = 'application/json'``. Ваш обработчик должен передать словарь-контекст, который будет упакован в json и вернется клиенту. Пример использования: ::

  # yourapp.views.py
  from spicy.core.siteskin.decorators import ajax_request
  
  @ajax_request(# additional args)
  def your_view(request):
    # logic here
    context = dict(param1=value, param2=value, ...)
    return context
  
   
Общие аргументы декораторов
---------------------------
Декораторы реализованы как наследники базового класса ``spicy.core.siteskin.decorators.ViewInterface``, поэтому каждый из них может принимать аргументы, позволяющие настривать дополнительные возможности, например, кэширование. Перечисленные ниже аргументы необязательны.
    
При передаче в декоратор ``use_siteskin=True`` будут использованы загрузчики шаблонов, указанные в ``settings.TEMPLATE_LOADERS``, значение по умолчанию - ``False``.

Аргумент ``use_admin=True`` позволяет указать, что поиск шаблона должен происходить в admin-директориях, т.е. к пути файла будет добавлен префикс ``/admin/``.
    
Аргумент ``use_cache`` управляет кэшированием результата обработчика, значение по умолчанию - ``False``.

Аргумент ``cache_timeout`` задает время хранения кэша, значение по умолчанию - 300 секунд.

Команды manage.py
-----------------

::
  Usage: manage.py collectstatic [options]


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
  --noinput             Do NOT prompt the user for input of any kind.
  --no-post-process     Do NOT post process collected files.
  -i PATTERN, --ignore=PATTERN
                        Ignore files or directories matching this glob-style
                        pattern. Use multiple times to ignore more.
  -n, --dry-run         Do everything except modify the filesystem.
  -c, --clear           Clear the existing files using the storage before
                        trying to copy or link the original file.
  -l, --link            Create a symbolic link to each file instead of
                        copying.
  --no-default-ignore   Don't ignore the common private glob-style patterns
                        'CVS', '.*' and '*~'.
  --version             show program's version number and exit
  -h, --help            show this help message and exit

{todo: чем отличается от штатного???, потестить работу }


create_sitemap 

::
  Usage: manage.py create_sitemap [options] 

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
  --limit=LIMIT         Limit number of objects
  --nomedia             Disable media data generation
  --prefix=PREFIX       Sitemap name prefix
  --version             show program's version number and exit
  -h, --help            show this help message and exit


{TODO шаблонные теги (бэкенд часть), контекстный процессор, виджеты}

Настройки settings.py
---------------------
Ниже приведены настройки модуля, которые вы можете переопределить в settings.py своего приложения.

Имя каталога с темами, по умолчанию ``../siteskins``: :: 

  THEMES_PATH = 'your/name/for/theme/folder'
  
Имя темы, используемой в админке по умолчанию, значение ``'current'``: ::

  DEFAULT_THEME = 'your_name'
  
Имя json-файла, описывающего темы, значение по умолчанию ``'spicy.theme'``: ::

  SPICY_THEME_FILE = 'your_name'
