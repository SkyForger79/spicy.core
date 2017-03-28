spicy.core.siteskin
*******************

Модуль является частью spicy.core и предназначен для управления оформлением сайта посредством тем. 
Основной особенностью spicy.core.siteskin является то, что вы можете использовать как темы модулей, предоставляемые по умолчанию, так и переопределять их в своем приложении.

Такой механизм обеспечивается модульностью продукта SpicyCMS. Каждый модуль вмещает в себя набор необходимых шаблонов.
Если вы переопределите какой-либо из них в своем приложении, повторив структуру папок модуля, то будет использован  именно ваш шаблон, иначе - spicy.core.siteskin подгрузит интегрированный в модуль spicy.

Структура каталога темы
========================

Минимально необходимая структура каталога темы выглядит так: ::

  ├── static            Используемые темой файлы статики (CSS-стили, JS-скрипты, иконка сайта favicon.ico)
  │   ├── css
  │   ├── favicon.ico
  │   └── js
  ├── templates		  Шаблоны django
  │   └── index.html  
  ├── readme.md
  └── spicy.theme      Файл описания в формате JSON

Кроме файлов формата .html, являющихся шаблонами django, используются также файлы .txt, которые являются частями шаблонов django. 
Такие файлы используются для конфигурации заголовка письма активации пользователя или заголовка отчета  

Поля spicy.theme
================
spicy.core.siteskin предоставляет возможность управлять темами из интерфейса администрирования. Вы можете определить отображение каждой темы в админке с помощью файла spicy.theme: ::

  // spicy.theme
  "theme_name" : 'mini_theme'	: Отображаемое имя темы     
  "theme_description"	        : Описание темы
  "author"		        : Автор
  "author_link"		        : Ссылка на автора
  "theme_link" 		        : Ссылка на тему
  "theme_thumbnail_link"	: Ссылка на картинку-превью темы
  "version" 			: Версии продукта, совместимые с данной темой

Структура каталогов модулей SpicyCMS
====================================
Вы можете переопределить любой из приведенных ниже шаблонов, для добавления своих стилей, js, изменения верстки.

Например, вы хотите изменить файл страницы входа в систему - в модуле spicy.core.profile, который имеет `такую структуру <./README.rst>`_.

Модуль spicy.categories: ::

  spicy.categories/src/spicy/categories/templates  
  └── spicy.categories
      └── admin
          └── menu.html                   Шаблон оформления пункта Категории админ.панели


Модуль spicy.core.profile: ::

  spicy.core/src/spicy/core/profile/templates
  └── spicy.core.profile
      ├── activate.html
      ├── admin                           Шаблоны оформления пункта Профили админ.панели     
      │   ├── blacklisted_ips.html        
      │   ├── create_group.html
      │   ├── create.html
      │   ├── dashboard.html
      │   ├── delete_group.html
      │   ├── edit.html
      │   ├── edit_media.html
      │   ├── groups.html
      │   ├── list.html
      │   ├── menu.html
      │   └── parts
      │       ├── edit_profile_form.html
      │       └── edit_profile_tabs.html
      ├── edit.html
      ├── login.html
      ├── mail
      │   ├── activation_email.html
      │   ├── activation_email_subject.txt
      │   ├── activation_email.txt
      │   ├── banned_email.html
      │   ├── banned_email.txt
      │   ├── banned_subject.txt
      │   ├── forgotten_password_email.html
      │   ├── forgotten_password_email.txt
      │   ├── forgotten_password_subject.txt
      │   ├── hello_email.html
      │   ├── hello_email.txt
      │   ├── hello_subject.txt
      │   ├── notify_managers_email.txt
      │   ├── notify_managers_subject.txt
      │   ├── passwd_email.html
      │   ├── passwd_email.txt
      │   ├── passwd_subject.txt
      │   ├── set_email_email.html
      │   ├── set_email_email.txt
      │   └── set_email_subject.txt
      ├── passwd.html
      ├── profile.html
      ├── restore_password.html
      ├── set_email.html
      ├── signin.html
      ├── signup.html
      ├── social
      │   ├── networks.html
      │   ├── new_user.html
      │   └── signin.html
      ├── success_signup.html
      ├── user_agreement.html
      └── widgets
          ├── signin_form.html
        └── signup_form.html

Модуль spicy.core.admin: ::

  spicy.core/src/spicy/core/admin/templates 
  └── spicy.core.admin                        Шаблоны оформления админки
      ├── admin
      │   ├── app
      │   │   ├── component
      │   │   │   ├── create_form.html
      │   │   │   └── edit_form.html
      │   │   ├── create.html
      │   │   ├── dashboard.html
      │   │   ├── delete.html
      │   │   ├── edit.html
      │   │   ├── list.html
      │   │   └── menu.html
      │   ├── application.html
      │   ├── base.html
      │   ├── dashboard.html
      │   ├── developer.html
      │   ├── formfield.html
      │   ├── login.html
      │   ├── logout.html
      │   ├── main_settings.html
      │   ├── managers.html
      │   ├── menu.html
      │   ├── pagination.html
      │   ├── robots_txt.html
      │   ├── sitemap.html
      │   ├── top_navbar.html
      │   └── wysiwyg.html
      └── public.admin.html

Модуль spicy.core.trash: ::

  spicy.core/src/spicy/core/trash/templates
  └── spicy.core.trash                        Шаблоны оформления пункта Trash(Корзина) админ.панели
      └── admin
          ├── list.html
          └── menu.html

Модуль spicy.core.simplepages: ::

  spicy.core/src/spicy/core/simplepages/templates
  └── spicy.core.simplepages                  Шаблоны оформления пункта Страницы админ.панели
      ├── admin
      │   ├── component
      │   │   ├── create_form.html
      │   │   ├── edit_form.html
      │   │   └── edit_tabs.html
      │   ├── create.html
      │   ├── edit.html
      │   ├── edit_seo.html
      │   ├── find.html
      │   ├── index.html
      │   └── menu.html
      ├── default.html
      └── simplepages
          ├── errors.403.html
          ├── errors.404.html
          └── errors.500.html

Модуль spicy.core.siteskin: ::

  spicy.core/src/spicy/core/siteskin/templates 
  └── spicy.core.siteskin                     Шаблоны оформления пункта Страницы админ.панели
      └── admin
          ├── edit.html
          └── menu.html


Модуль spicy.core.service.templates: ::

  spicy.core/src/spicy/core/service/templates
  ├── service
  │   └── admin
  │       └── dashboard.html
  └── spicy.core.service
      └── admin
          ├── dashboard.html
          └── service_preview.html

Модуль spicy.core: ::

  spicy.core/src/spicy/siteskin-examples/current/templates 
  └── base.html                               Пример базового шаблона

Модуль spicy.document: ::

  spicy.document/src/spicy/document/templates 
  └── spicy.document
      ├── admin                               Шаблоны оформления пункта Документы админ.панели
      │   ├── component
      │   │   └── create_form.html
      │   ├── create.html
      │   ├── dashboard.html
      │   ├── documents_list.html
      │   ├── edit.html
      │   ├── edit_media.html
      │   ├── edit_photo_includes.html
      │   ├── history.html
      │   ├── list.html
      │   ├── menu.html
      │   ├── parts
      │   │   ├── documents_list.html
      │   │   ├── edit_document_form.html
      │   │   └── edit_document_tabs.html
      │   ├── service_create.html
      │   ├── service_doc_list.html
      │   └── service_document.html
      └── document.html

Модуль spicy.feedback: ::

  spicy.feedback/src/spicy/feedback/templates
  └── spicy.feedback                          Шаблоны оформления пункта Обратная связь админ.панели
      ├── admin
      │   ├── edit_calc.html
      │   ├── edit.html
      │   ├── edit_pattern.html
      │   ├── edit_pattern_media.html
      │   ├── list.html
      │   ├── menu.html
      │   ├── parts
      │   │   ├── email_form.html
      │   │   ├── feedback_tabs.html
      │   │   └── pattern_tabs.html
      │   └── patterns.html
      ├── mail
      │   ├── report_email_body.txt
      │   ├── report_email_subject.txt
      │   └── report_email.txt
      ├── patterns
      │   └── default.html
      └── sms
          └── report.txt

Модуль spicy.history: ::

  spicy.history/src/spicy/history/templates
  └── spicy.history                           Шаблоны оформления пункта История правок админ.панели
      └── admin
          ├── action.html
          ├── actions.html
          ├── diff.html
          ├── list.html
          └── menu.html

Модуль spicy.menu: ::

  spicy.menu/src/spicy/menu/templates     
  └── spicy.menu                             Шаблоны оформления пункта Меню админ.панели
      └── admin
          ├── autocomplete.html
          ├── autocomplete_static.html
          ├── create-ajax.html
          ├── delete-menu.html
          ├── edit-ajax.html
          ├── edit.html
          ├── list_entry.html
          ├── list_tree.html
          ├── menu.html
          └── preview.html


Настройки settings.py
=====================
Ниже приведены настройки модуля, которые вы можете переопределить в settings.py своего приложения.

Имя каталога с темами, по умолчанию ``../siteskins``::: 

  THEMES_PATH = 'your/name/for/theme/folder'
  
Имя темы, используемой в админке по умолчанию, значение ``'current'``: ::

  DEFAULT_THEME = 'your_name'
  
Имя json-файла, описывающего темы, значение по умолчанию ``'spicy.theme'``: ::

  SPICY_THEME_FILE = 'your_name'
