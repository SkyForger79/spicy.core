[![Build Status](https://travis-ci.org/spicycms/spicy.core.svg?branch=tests_fix)](https://travis-ci.org/spicycms/spicy.core) [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage) [![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core) [![Coverage Status](https://coveralls.io/repos/github/spicycms/spicy.core/badge.svg?branch=tests_fix)](https://coveralls.io/github/spicycms/spicy.core?branch=tests_fix)


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


### Концепция проекта Django приложения

Команда создает в текущей директории проект

spicy project <example-project-name> <path>


nginx.conf.spicy
uwsgi.conf.spicy


### Публикация Django приложения на сервер


## Fabric


## Docker


## Приложения включенные в spicy.core


### spicy.core.service


### spicy.core.profile


### spicy.core.admin


### spicy.core.siteskin


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
