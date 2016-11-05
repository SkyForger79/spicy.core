[![Build Status](https://travis-ci.org/spicycms/spicy.core.svg?branch=tests_fix)](https://travis-ci.org/spicycms/spicy.core) [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage) [![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core)


==========
SpicyCMF core documentation version 1.2.0
==========


TODO: write readme in plain text at least


Tools
-----

**virtualenvwrapper** (optional)
Makes work with virtual environments more comfort. Docs here: [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
If use Debian-based OS, you can install it with:

```bash
sudo apt-get install -y virtualenvwrapper
```

Команда для работы с проектами django/SpicyCMF. Позволяет деплоить проекты и создавать шаблонные.

```spicy -h```


Tests
-----

Настройте окружение под модуль spicy.core, если вы хотите заняться разработкой только этого модуля или протеситровать его.


```bash
virtualenv spicycore-env
source spicycore-env/bin/activate
pip install .
pip install -r requirements_dev.txt
```

Команда запуска тестов для локальной разработки в стиле TDD:

```bash
./runtests.sh
```

Эта команда будет каждый раз создавать тестовую базу данных и запускать тесты из директории `src`.
Таким образом программист может не делать приложение Django и тестировать базовую функциональность. расшрять ее и модифицировать
изменяя код и запуская тесты.


And you must remember
---------------------

People, who creates your software, in most cases are same to you are. So, you must know: in theory they could be murderers or maniacs, or, even a women. So, it's much better for **you** to write *good* code. You have been warned.
