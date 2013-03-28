#!/bin/sh

ENV = '/var/www/envs/spicy_example'

echo Creating environment
virtualenv --no-site-packages -p python2.7 

echo Install PIP inside virtual environment $ENV
$ENV/bin/easy_install pip

echo Installing dependencies

source $ENV'/bin/activate'
pip install -r ./pipreq.txt
