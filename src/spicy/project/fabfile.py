import os
import sys
from fabric.api import *
from fabric.contrib.files import exists


PROJECT_ROOT = os.path.abspath('.')
sys.path.insert(0, PROJECT_ROOT)
REMOTE_USER = 'nginx'
REMOTE_APP_DIR = '/var/www/apps/'
REMOTE_APP_NAME = 'example.com'
cfgfilelist = 'local.py', 'database.py'

env.hosts = ['development']

def copy_config(app=REMOTE_APP_NAME):
    path = os.path.join(REMOTE_APP_DIR, app, 'config/')
    with cd(path):
        for filename in cfgfilelist:
            if not exists(filename):
                sudo('cp ' + filename + '.defaults ' + filename)

def check_target_dirs(app=REMOTE_APP_NAME):
    path = os.path.join(REMOTE_APP_DIR, app)
    if not exists(path):
        sudo('mkdir -m ug=rwx,o= ' + path, user=REMOTE_USER);
#    if not exists(MEDIACENTER_ROOT):
#        sudo('mkdir '+MEDIACENTER_ROOT,user=REMOTE_USER)

def upload_sources(app=REMOTE_APP_NAME):
    local(
        'hg archive -t tgz -p \'.\' -X \'{*.pyc,config/local.py,'
        'config/database.py,fabfile.py}\' ./src.tgz')
    path = os.path.join(REMOTE_APP_DIR, app)
    put('src.tgz', path)
    with cd(path):
        sudo('tar -mxzf src.tgz', user=REMOTE_USER)
        run('rm src.tgz')
    local('rm src.tgz')

def restart_app(app=REMOTE_APP_NAME):
    sudo('/etc/init.d/wsgi-%s restart' % app)

def deploy_src(app=REMOTE_APP_NAME):
    print "Deploying '%s' sources to %s" % (app, env.host)
    check_target_dirs(app)
    upload_sources(app)
    copy_config(app)
    restart_app(app)

