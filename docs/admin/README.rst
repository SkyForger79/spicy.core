spicy.core.admin
****************

Назначение
==========
spicy.core.admin является модулем spicy.core, предназначен для отображения административной части приложения. Его отличие от стандартной админки Django заключается в том, что в совокупности с другими модулями SpicyCMS позволяет формировать интерфейс под нужды конечного пользователя - редактора сайта, администратора и т.д.

Аналоги
=======

* `Django admin <https://djbook.ru/rel1.4/ref/contrib/admin/index.html>`_
* `Django grappelli <https://github.com/sehmaschine/django-grappelli>`_

Django admin и Grappelli позволяют разработчику быстро настроить окружение администратора для разработки, но не дают возможность настроить интерфейс под нужды конечного пользователя админки. spicy.core.admin может быть использован с Django 1.3 - 1.5.

Для администратора сайта
========================
{TODO описать что можно сделать в разделе меню Настройки}

Для Django программиста
=======================
{TODO переопределение настроек, контекстный процессор, команды менеджмента }

Для верстальщика
================

Делаем свою страницу в админке
------------------------------
Благодаря модулю `spicy.core.siteskin <https://github.com/spicycms/spicy.core/tree/f29c955de7c8e920e5f0b9d9aaa231f0563c388f#spicycoresiteskin>`_ вы можете переопределить любой шаблон, который SpicyCMS использует для отображения админки. По умолчанию используются шаблоны из spicy.core.admin: ::

  spicy.core/src/spicy/core/admin/templates 
  └── spicy.core.admin                        Шаблоны оформления админки
      ├── admin
      │   ├── app
      │   │   ├── component
      │   │   │   ├── create_form.html
      │   │   │   └── edit_form.html
      │   │   ├── create.html
      │   │   ├── dashboard.html
      │   │   ├── delete.html
      │   │   ├── edit.html
      │   │   ├── list.html
      │   │   └── menu.html
      │   ├── application.html
      │   ├── base.html
      │   ├── dashboard.html
      │   ├── developer.html
      │   ├── formfield.html
      │   ├── login.html
      │   ├── logout.html
      │   ├── main_settings.html
      │   ├── managers.html
      │   ├── menu.html
      │   ├── pagination.html
      │   ├── robots_txt.html
      │   ├── sitemap.html
      │   ├── top_navbar.html
      │   └── wysiwyg.html
      └── public.admin.html
      
Если вы хотите добавить свои стили, js или полностью переделать шаблон, вы должны создать такую же структуру папок в вашем проекте и добавить новый файл с именем как у шаблона, кторый вы хотите заменить.

Например, вы хотите переопределить top_navbar.html. Для этого создайте следующую структуру папок в проекте: ::
 
  yourapp/templates
  └── spicy.core.admin                        
      └── admin
          └── top_navbar.html     # this is your custom template
          
Таким образом, для top_navbar.html будет использован ваш шаблон, а остальные будут взяты из spicy.core.admin.

Шаблонные теги spicy.core.admin
-----------------------------------------
Чтобы подключить шаблонные теги spicy.core.admin, добавьте в шаблон: ::
 
  {% load spicy_admin %}
  
Теперь вам будут доступны следующие теги ``app_menu``, ``app_dashboard``, ``appblock``, ``menu``, ``formfield``, ``apply``.

{% TODO проверить работу всех тегов %}

Тег ``app_menu`` позволяет получить контент меню для указанного приложения: ::

  {% for app in ADMIN_APPS %}
    {% app_menu request app %}
  {% endfor %}
  
Тег ``app_dashboard`` позволяет получить контент, который будет отображен на главном экране для указанного приложения: ::

  {% for app in ADMIN_APPS %}
    {% app_dashboard request app %}
  {% endfor %}
  
Переменная ``ADMIN_APPS`` предоставляется контекстным процессором spicy.core.admin

Тег ``appblock`` позволяет указать блок, который может быть переопределен в дочернем шаблоне при наследовании: ::

  {% appblock block_name block_app %}
    {# your code that will be applied for app specified as block_app #} 
  {% endappblock %}
  
Тег ``menu`` позволяет сгенерировать ссылку в любом шаблоне, через которую в обработчик могут быть переданы дополнительные аргументы. Поддерживает стилизацию ссылки через html-аттрибут ``class``. В общем виде выглядит: ::

  {% menu request url_as_string title_for_link li_class 
    inner_a_class get_params_as_string params_for_url  %}
    
Например, вы хотите сгенерировать ссылку на страницу всех пользователей, которая имеет строковый адрес ``'webapp:public:profiles'``. Обработчик может принимать дополнителььный GET-параметр ``sort_by``, сортируя список по укаазанному полю. Тогда ваш тег может выглядеть так: ::

  {% menu request 'webapp:public:profiles' 'Link to all profiles' 'sort_by=date_joined' %}
  
Будет сгенерирован такой html: ::

  <li class=" activated">
    <a href="your/profile/list/url/?sort_by=date_joined" class="ui-corner-left">Link to all profiles</a>
  </li>
  
При переходе по этой ссылке обработчик вернет список профилей пользователей, отсортированных по дате добавления.

Тег ``formfield`` позволяет сгенерировать поле ввода для формы. Благодаря ``formfield``, вам не придется для каждой страницы админки вручную переопределять стили элементов форм, вы можете один раз стилизовать их в файле ``yourapp/templates/spicy.core.admin/admin/formfield.html`` и использовать в любом шаблоне. 

Этот механизм позволяет использовать `модельные формы Django <https://djbook.ru/rel1.4/topics/forms/modelforms.html#modelform>`_ и при этом с легкостью изменять их стили, без редактирования Python кода.

Синтаксис тега: ::

  {% formfield input_placeholder form field_name type preview_link classes id ajax_url data_url from_field %}
  
Некоторые из настроек могут быть не применимы для определенных типов полей, например, ``placeholder`` для ``<select>``. Если вы укажите ее, то ошибки не произойдет, просто настройка не будет использована.

По умолчанию значение для ``type`` равно ``li-text`` - все поля ввода создаются как ``<input type="text">``. 

Настройка ``preview_link`` добавляет иконку-ссылку для просмотра объекта на сайте. Может быть полезно на страницах редактирования объектов, например, редактирование профиля: ::

  {% formfield "" form "username" "li-text" True %}
  
Будет сформирована ссылка на профиль редактируемого пользователя рядом с полем ввода username: ::

  <li class="input">
    <label for="id_username">Username</label>
    <input type="text" name="username" placeholder="" value="form_value" id="id_username">
    <a href="/link/to/user/profile" target="blank">
      <i class="icon-eye-open icon-2x"></i> 
    </a>
  </li>

Настройки ``input_placeholder``, ``classes`` и ``id`` добавляют соответствующие аттрибуты в html-тег.

Настройка ``ajax_url``, ``data_url`` применимы только к полям с типом ``li-select2``, они включают автокомплитер. Подробнее в `документации select2 <https://select2.github.io/>`_.

Настройка ``from_field`` применима только к полю с типом ``li-slug``. Она позволяет указать, из какого поля будет формироваться slug объекта.

Минимальный набор параметров для работы тега - пустой ``context``, ``form`` и ``field_name``. Например, такой вызов: ::

  {% formfield "" form "username" %}
  
Сформирует поле для ввода имени пользователя, используя форму ``form``: ::

  <li class="input">
    <label for="id_username">Username</label>
    <input type="text" name="username" placeholder="" value="form_value" id="id_username">
  </li>
 
Тег ``apply`` применяет функцию к аргументу и добавляет результат выполнения в контекст текущего шаблона: ::

  {% apply function arg result_name %}

Результат будет доступен в шаблоне по имени ``result_name``.

Теги ``apply`` и ``formfield``,  имеют доступ к контексту текущего шаблона, подробнее в `документации Django о шаблонных тегах <https://djbook.ru/rel1.4/howto/custom-template-tags.html#simple-tags>`_.
  

Шаблонные фильтры spicy.core.admin
----------------------------------
Предоставлены два фильтра - ``installed_app`` и ``check_perms``. Чтобы использовать их в шаблоне, подключите: ::

  {% load spicy_admin %}
  
Фильтр ``installed_app`` проверяет, установлено ли приложение в ``settings.INSTALLED_APP``: ::

  {% if 'app_name'|installed_app %}
    {# your code if True #}
  {% else %}    
    {# you code if False #}
  {% endif %}

Фильтр ``check_perms`` проверяет права пользователя на доступ к приложению SpicyCMS ``conf.AdminAppBase``, ссылке ``conf.AdminLink`` или любому типу объектов через `права Django <https://django.readthedocs.io/en/1.4.X/topics/auth.html#permissions>`_: ::

  {% if user|check_perms:permission %}
    {# your code if True #}
  {% else %}
    {# you code if False #}
  {% endif %}
  
Переменные контекста spicy.core.admin
-------------------------------------
Установленные в проекте приложения, имеющие модуль для админки: ::

  {{ ADMIN_APPS }}
  
Приложения, которые настроены для отображения в админке на главной странице: ::

  {{ ADMIN_DASHBOARD_APPS }} 
  
Полный текущий URL, с протоколом и портом: ::

  {{ FULL_PATH_WITH_PORT }}
  
Текущий URL, с протоколом, но без порта: ::

  {{ HOST_WITH_PORT }}
