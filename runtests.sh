#!/bin/bash
set +x

DJANGO_SETTINGS_MODULE="spicy.core.profile.tests.settings" \
PYTHONPATH="${PYTHONPATH}:$(pwd)/src" \
python -m unittest discover
