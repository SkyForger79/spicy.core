#!/bin/bash
set +x

virtualenv --no-site-packages spicycore-env
source spicycore-env/bin/activate
pip install .
pip install -r requirements_dev.txt

export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export DJANGO_SETTINGS_MODULE="spicy.tests.settings"

django-admin.py syncdb --noinput
coverage run --parallel-mode -m unittest discover

rm spicy_test.db
rm .coverage.*
rm -rf spicycore-env
