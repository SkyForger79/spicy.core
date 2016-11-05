#!/bin/bash
set +x

export DJANGO_SETTINGS_MODULE="spicy.core.profile.tests.settings"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"


django-admin.py syncdb --noinput
coverage run --parallel-mode -m unittest discover
rm spicy_test.db

COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN coveralls
