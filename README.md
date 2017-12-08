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

Site skin - it's


| Variable | Default | Description |
| -------- | ------- | ----------- |
| SITESKINS_PATH         | ../siteskins     | The path for folder containing site skins directories |


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
