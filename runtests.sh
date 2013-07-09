#!/bin/bash
set +x

function section() {
    length=80
    printf -v line '%*s' "$length"
    echo ${line// /=}
    echo -e "$1"
    echo ${line// /=}
}

section "Running all tests in failfast mode"
# run ALL tests in --failfast, --verbose ultrahardcore mode
#python -m spicy.spicyunittest discover -f -v -s "spicy/tests"
#section "Running spicy.core.profile tests in failfast mode"
#python -m spicy.spicyunittest discover -f -v -s "spicy/core/profile/tests"

#DJANGO_SETTINGS_MODULE="spicy.core.profile.tests.settings" \
# django-admin.py test spicy.tests.test_spicy --noinput
DJANGO_SETTINGS_MODULE="spicy.core.profile.tests.settings" \
 django-admin.py test spicy.core.profile.tests.test_models --noinput
