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

Шаблонные теги и фильтры spicy.core.admin
-----------------------------------------
Чтобы подключить шаблонные теги spicy.core.admin, добавьте в шаблон: ::
 
  {% load spicy_admin %}
  
Теперь вам будут доступны следующие теги ``app_menu``, ``app_dashboard``, ``appblock``, ``menu``, ``formfield``, ``apply`` и фильтры ``installed_app``, ``check_perms``.

{% TODO проверить работу всех тегов %}

Тег ``app_menu`` позволяет получить контент меню для указанного приложения: ::

  {% app_menu request app_name %}
  
Тег ``app_dashboard`` позволяет получить контент, который будет отображен на главном экране для указанного приложения: ::

  {% app_dashboard request app_name %}
  
{TODO tag appblock %}: ::

  example of appblock tag
  






 
{TODO переменные контекстного процессора, шаблонные теги}
