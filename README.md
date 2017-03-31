[![Build Status](https://travis-ci.org/spicycms/spicy.core.svg?branch=tests_fix)](https://travis-ci.org/spicycms/spicy.core) [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage) [![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core) [![Coverage Status](https://coveralls.io/repos/github/spicycms/spicy.core/badge.svg?branch=tests_fix)](https://coveralls.io/github/spicycms/spicy.core?branch=tests_fix) [![Dependency Status](https://gemnasium.com/badges/github.com/spicycms/spicy.core.svg)](https://gemnasium.com/github.com/spicycms/spicy.core)


SpicyCMF core documentation version 1.2.0
=========================================
{TODO исправить ссылки с dev-веток на смерженный код документации}


## Проблемы при разработке приложений на Django


* *Дублирование*

	При написании более-менее объемного проекта Django часто возникает проблема дублирования кода. Особенно, если несколько django-приложений реализуют схожую однако не идентичную функциональность. Спасительным решением являются абстракции

* *Необходимость переписывать ранее написанные модули, чтобы адаптировать их к новым задачам*

	На более-менее протяженном отрезке времени у разработчика накапливается свой наборов приложений для решения задач.
	Управление и адаптация однотипныe наборов приложений для джанго приложения, применение манки-патчей (абстракции для расширения кода модулей)
	и отслеживание кросс-импорта становятся очень ресурсоемкой задачей.

* *Необходимость адаптирования админки под бизнес процессы*

* *Управление релизами и отладка сложных приложений*

* *Отсутствие стандарта по расширению модулей django (абстракции)*

	Необходимость вручную модернизировать код приложений на Django, если были использованы сторонние модули и модифицирован их код для интеграции.

* *Обеспечение понятного и удобного инструмента разработки/дизайна для исполнителя любой роли*

	Механизм шаблонов Django, не расчитан на использование дизайнерами/верстальщиками/контент-редактора без доп. знания Django.

	Нет возможности быстро разделить работы на frontend / backend для простых приложений с HTML страницами. 
	Тема помогает разделить роли webmaster от python-developer и делать для сайтов несколько разных версий отображения, меняя их на лету  и тестируя их эффективность без риска сломать все приложение и необходимости приклекать программиста для восстановления старого отображения сайта.


{ToDo} Simplepages - ссылка

В SpicyCMS эти проблемы решены с помощью сервис-ориентированной архитектуры. Главный модуль [spicy.core](docs#Документация-spicycore) и [модули SpicyCMS](https://github.com/spicycms) устраняют проблемы, позволяя ускорить процесс разработки и адаптировать приложения под бизнес процессы.


### Концепция приложения-модуля для Django

Команда создает в текущей директории приложение 

spicy app <example-app-name> <path>


Структура файлов и папок приложения:

```
defaults.py
services.py
urls.py
admin.py
views.py

templates
```


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


## Fabric {TODO}


## Docker {TODO}


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
