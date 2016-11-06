#!/bin/bash
set +x

virtualenv --no-site-packages spicycore-env
source spicycore-env/bin/activate
pip install .
pip install -r requirements_dev.txt

export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
export DJANGO_SETTINGS_MODULE="spicy.tests.settings"

django-admin.py syncdb --noinput
coverage run -m unittest discover #--parallel-mode


rm spicy_test.db
rm .coverage
rm .coverage.*
rm -rf spicycore-env
