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
python -m spicy.spicyunittest discover -f -v -s "src/spicy/tests"
