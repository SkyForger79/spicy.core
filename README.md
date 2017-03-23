[![Build Status](https://travis-ci.org/spicycms/spicy.core.svg?branch=tests_fix)](https://travis-ci.org/spicycms/spicy.core) [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage) [![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core) [![Coverage Status](https://coveralls.io/repos/github/spicycms/spicy.core/badge.svg?branch=tests_fix)](https://coveralls.io/github/spicycms/spicy.core?branch=tests_fix) [![Dependency Status](https://gemnasium.com/badges/github.com/spicycms/spicy.core.svg)](https://gemnasium.com/github.com/spicycms/spicy.core)


==========
SpicyCMF core documentation version 1.2.0
==========


## Проблемы при разработке приложений на Django

Опиисание проблемы дублирования кода (абстракции для расширения - стандарт)
однотипных наборов приложений для джанго приложения и манки патчи (бастракции для расширения кода модулей)
кросс-импорта
адаптирования админки под бизнес процессы
управление релизами и дебагигн сложных приложений
Отсутсвие стандарта по расширению модулей django (абстракции)
Необходимость вручную модернизировать код приложений на Django, если были использованы стороннии модули и модифицирован их код для интеграции
Нет возможности быстро разделить работы на frontend / backend для простых приложений с HTML страницами. Тема помогает отделить работы webmaster от python-developer и делать для сайтов несколько разных версий отображения, меняя их на лету  итестирую их эффективность без риска сломать все приложение и необходимыости приклекать программиста для восстановления старого отображения сайта
Simplepages - 

### Концепция приложения-модуля для Django

Команда создает в текущей директории приложение 

spicy app <example-app-name> <path>


Структура файлов и папок приложения

defaults.py
services.py
urls.py
admin.py
views.py

templates


### ВАЖНО setup.py и MANIFEST.in

recursive-include src/spicy/core/admin/locale *
recursive-include src/spicy/core/admin/static *
recursive-include src/spicy/core/admin/templates *


Для spicy модуля нужно обязательно делать файл манифест,
чтобы устанавливались статичные файлы модуля python.

Это важно для templates, ``static``, ``locale`` и ``fixtures``



### Концепция проекта Django приложения

Команда создает в текущей директории проект

spicy project <example-project-name> <path>


nginx.conf.spicy
uwsgi.conf.spicy


### Концепция шаблонов сайтов для Django приложений

TODO v2.0

spicy create siteskin [<cmf-type>:default cms-chief-editor] <siteskin-name> <path>


### Публикация Django приложения на сервер


## Fabric


## Docker


## Приложения включенные в spicy.core


### spicy.core.service

Концепция сервисов решает проблему макаранного кода или кросс-импортов между различными приложениями, где нужно
сделать ForeignKey связь или m2m отношение. Сервис может предоставлять любой Django модуль, декларировать типы связей и методы предоставления сервиса.
Сам сервис является в таком случаем классом с методами обработки типичных забросов для обратки связей с заказчиками сервиса (Consumer)

Interface

Service

Provider

Cunsumer



### spicy.core.profile


### spicy.core.admin


### spicy.core.siteskin

Модуль Siteskin является частью модуля spicy.core и предназначен для управления оформлением сайта посредством тем. 
Основной особенностью тем spicy.core.siteskin является то, что они могут хранить полный набор файлов для оформления, или же минимальный набор файлов шаблонов.


Такой механизм обеспечивается модульностью продукта SpicyCMS.Каждый модуль spiсy вмещает в себя набор необходимых файлов.
В случае, если выбранная тема из каталога THEME_PATH не включает в себя нужных файлов, они берутся из интегрированных в модули spicy.

**Структура каталога темы**

Минимально необходимая структура каталога темы выглядит так:
```
├── static            Используемые темой файлы статики (CSS-стили, JS-скрипты, иконка сайта favicon.ico)
│   ├── css
│   ├── favicon.ico
│   ├── js
│   └── plugins  
├── templates		  Шаблоны django
│   └── index.html  
├── readme.md
└── spicy.theme      Файл описания в формате JSON
```
**Поля spicy.theme**

"theme_name" : 'mini_theme'	: Отображаемое имя темы     
"theme_description"			: Описание темы
"author"					:  Автор
"author_link"				: Ссылка на автора
"theme_link" 				: Ссылка на тему'   
"theme_thumbnail_link"		: Ссылка на картинку-превью темы
"version" 					: Версии продукта, совместимые с данной темой


Ниже описана структура каталогов с файлами оформления, включенными в состав модулей.

#### spicy.categories ####

```
spicy.categories/src/spicy/categories/templates  
└── spicy.categories
    └── admin
        └── menu.html
```

#### spicy.core.profile ####

```
spicy.core/src/spicy/core/profile/templates
└── spicy.core.profile
    ├── activate.html
    ├── admin
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
```

#### spicy.core.admin ####

```
spicy.core/src/spicy/core/admin/templates
└── spicy.core.admin
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
```

#### spicy.core.trash ####

```
spicy.core/src/spicy/core/trash/templates
└── spicy.core.trash
    └── admin
        ├── list.html
        └── menu.html
```

#### spicy.core.simplepages ####

```
spicy.core/src/spicy/core/simplepages/templates
└── spicy.core.simplepages
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
```

#### spicy.core.siteskin ####

```
spicy.core/src/spicy/core/siteskin/templates
└── spicy.core.siteskin
    └── admin
        ├── edit.html
        └── menu.html
```

#### spicy.core.service.templates ####

```
spicy.core/src/spicy/core/service/templates
├── service
│   └── admin
│       └── dashboard.html
└── spicy.core.service
    └── admin
        ├── dashboard.html
        └── service_preview.html
```

#### spicy.core ####

```
spicy.core/src/spicy/siteskin-examples/current/templates 
└── base.html
```

#### spicy.document ####

```
spicy.document/src/spicy/document/templates
└── spicy.document
    ├── admin
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
```

#### spicy.feedback ####

```
spicy.feedback/src/spicy/feedback/templates
└── spicy.feedback
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
```

#### spicy.history ####

```
spicy.history/src/spicy/history/templates
└── spicy.history
    └── admin
        ├── action.html
        ├── actions.html
        ├── diff.html
        ├── list.html
        └── menu.html
```

#### spicy.menu ####

```
spicy.menu/src/spicy/menu/templates 
└── spicy.menu
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
```

#### Переменные настройки, касающиеся модуля Siteskin ####


####







### spicy.core.simplepages


### spicy.core.trash


### spicy.core.rmanager


### spicy.utils / rename helpers & snipets


### spicy.templates / rename project-templates




Tests
-----


Команда запуска тестов для локальной разработки в стиле TDD:

```bash
./runtests.sh
```

Эта команда будет каждый раз создавать тестовую базу данных и окружение из файла `setup.py`, запускать тесты из директории `src`.
Таким образом программист может не делать приложение Django и тестировать базовую функциональность модуля.
Расшрять ее и модифицировать изменяя код, и запуская тесты.


And you must remember
---------------------

People, who creates your software, in most cases are same to you are. So, you must know: in theory they could be murderers or maniacs, or, even a women. So, it's much better for **you** to write *good* code. You have been warned.
