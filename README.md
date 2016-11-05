[![Code Climate](https://codeclimate.com/github/spicycms/spicy.core/badges/gpa.svg)](https://codeclimate.com/github/spicycms/spicy.core)  [![Test Coverage](https://codeclimate.com/github/spicycms/spicy.core/badges/coverage.svg)](https://codeclimate.com/github/spicycms/spicy.core/coverage)

==========
Spicy docs
==========

Fixed version 1.2.0

Main and the one using case:

.. code-block:: sh
   `spicy -h`

TODO: write readme in plain text at least

Docs
----
TODO: write docs

Tools
-----

**virtualenvwrapper** (optional)
Makes work with virtual environments more comfort. Docs here: [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).
If use Debian-based OS, you can install it with:
```bash
sudo apt-get install -y virtualenvwrapper
```

Tests
-----
На данный момент тесты используют движок ```unittest```, рекомендуемвый разработчиками Django. Встроенные в Django классы для написания тестов, такие как ```django.test.TestCase``` внутри наследуются от ```unittest.TestCase```, но реализуют специализированную функцональность, например транзакционность обращений к БД в ходе тестов.

Исходя из того, что при разработке тестов необходимо часто вность изменения в кодовую базу, был выбран подход, при котором тесты запускаются для кода в каталоге ```src``` модуля ```spicy.core```, что не требует установки модуля в систему через ```python setup.py install``` после каждой внесенной правки, но требует добавления каталога ```src``` в ```PYTHONPATH```.

Необходимые для разработки ядра модули перечислены в ```requirements_dev.txt``` и, соответственно, устанавливаются командой:
```bash
pip install -r requirements_dev.txt
```

Команда запуска тестов со сбором статистики по покрытыю выглядит следующим образом:

```bash
DJANGO_SETTINGS_MODULE="spicy.core.profile.tests.settings" \
PYTHONPATH="${PYTHONPATH}:$(pwd)/src" \
python -m unittest discover
```


And you must remember
---------------------

People, who creates your software, in most cases are same to you are. So, you must know: in theory they could be murderers or maniacs, or, even a women. So, it's much better for **you** to write *good* code. You have been warned.
