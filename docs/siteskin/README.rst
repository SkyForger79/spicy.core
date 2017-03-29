spicy.core.siteskin
*******************

Модуль является частью spicy.core и предназначен для управления оформлением сайта посредством тем. 
Основной особенностью spicy.core.siteskin является то, что вы можете использовать как темы модулей, предоставляемые по умолчанию, так и переопределять их в своем приложении.

Такой механизм обеспечивается модульностью продукта SpicyCMS. Каждый модуль вмещает в себя набор необходимых шаблонов.
Если вы переопределите какой-либо из них в своем приложении, повторив структуру папок модуля, то будет использован  именно ваш шаблон, иначе - spicy.core.siteskin подгрузит интегрированный в модуль spicy.

Пример использования темы
=========================

* `Две темы <https://gitlab.com/spicycms.com/cms.chiefeditor/tree/feature/add-skins-folder/siteskins#%D0%98%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F-%D0%BF%D0%BE-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B5-%D1%81%D0%BA%D0%B8%D0%BD%D0%B0>`_, включенные по умолчанию в SpicyCMS Chief Editor {TODO заменить dev-ссылку на смерженный код}

* {TODO ссылка на настройки в CMS CE для Django программиста}

* {TODO ссылка на демо админки CMS CE, раздел Темы}

Для верстальщика
================

Переопределяем шаблон модуля SpicyCMS
-------------------------------------
Вы можете переопределить любой из предоставляемых по умолчанию шаблонов, для добавления своих стилей, js, изменения верстки.

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

{TODO шаблонные теги, переменные контекстного процессора, виджеты}

Для Django программиста
=======================
{TODO команды manage.py, шаблонные теги (бэкенд часть), контекстный процессор, виджеты}

Декораторы spicy.core.siteskin
------------------------------
{TODO}

Настройки settings.py
---------------------
Ниже приведены настройки модуля, которые вы можете переопределить в settings.py своего приложения.

Имя каталога с темами, по умолчанию ``../siteskins``: :: 

  THEMES_PATH = 'your/name/for/theme/folder'
  
Имя темы, используемой в админке по умолчанию, значение ``'current'``: ::

  DEFAULT_THEME = 'your_name'
  
Имя json-файла, описывающего темы, значение по умолчанию ``'spicy.theme'``: ::

  SPICY_THEME_FILE = 'your_name'
