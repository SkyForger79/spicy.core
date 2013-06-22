# coding: utf-8
"""SpicyTools command handler implementation

SPICY_BUILD_DIR = '.spicy-build'
SPICY_REQ_FILE = 'requirements.txt'

SPICY_APPS_SERVER_USER = 'nginx'

SPICY_APPS_SERVER = ''
SPICY_SERVER_DOCS_PATH = '/var/www/sites'
SPICY_SERVER_APP_PATH = '/var/www/apps'
SPICY_SERVER_ENV_PATH = '/var/www/envs'
SPICY_SERVER_STATIC_PATH = '/var/ftp/static'


"""
import string
import errno
import shutil
from spicy import version as spicy_version

import os
import sys
import argparse
import subprocess
import traceback
import configparser
import getpass 
import codecs
import re

from datetime import datetime as dt

from fabric.colors import *
from fabric.context_managers import lcd, cd, settings, prefix, shell_env, hide
from fabric.api import local, env, sudo, put, run
from fabric.decorators import with_settings
from fabric.contrib.files import exists

from jinja2 import Template
from jinja2.exceptions import UndefinedError

# some in place helpers definitions
write_err = sys.stderr.write
write_std = sys.stdin.write

outwr = sys.stdout.write
errwr = sys.stderr.write

print_ok = lambda x: outwr(green('> {0}\n'.format(x)))
print_info = lambda x: outwr(yellow('> {0}\n'.format(x)))
print_warn = lambda x: outwr(red('> {0}\n'.format(x)))
print_err = lambda x: errwr(red('> {0}\n'.format(x)))
print_done = lambda x: errwr(magenta('> {0}\n'.format(x)))
raw_input_cyan = lambda x: raw_input(cyan('> {0}\n'.format(x)))

SPICY_BUILD_DIR = 'spicy-build'
SPICY_REQ_FILE = 'requirements.txt'

SPICY_PROJECT_CONFIG_FILE = 'spicy.conf'
SPICY_CONFIG_TEMPLATE_POSTFIX = '.spicy'
SPICY_APP_CRON_CONFIG = os.environ.get('SPICY_APP_CRON_CONFIG', 'crontab.conf')

SPICY_APPS_SERVER_USER = 'nginx'
SPICY_APPS_SERVER_GROUP = 'nginx'


SPICY_SERVER_REQUIREMENTS = {
    'nginx': '1.4.0',
    'uwsgi': '1.4.9',
    'virtualenv': '1.7.1.2',
    'python': '2.7',
    }

SPICY_SERVER_TMP_PATH = os.environ.get('SPICY_SERVER_TMP_PATH', '/tmp')
SPICY_SERVER_APPS_ENV_PATH = os.environ.get('SPICY_SERVER_APPS_ENV_PATH', '/var/www/envs')
SPICY_SERVER_APPS_PATH = os.environ.get('SPICY_SERVER_APPS_PATH', '/var/www/apps')

SPICY_SERVER_SITES_PATH = os.environ.get('SPICY_SERVER_SITES_PATH', '/var/www/sites')

SPICY_SERVER_STATIC_PATH = os.environ.get('SPICY_SERVER_STATIC_PATH', '/var/ftp/static')
SPICY_SERVER_MEDIA_PATH = os.environ.get('SPICY_SERVER_MEDIA_PATH', '/var/www/media')

SPICY_SERVER_RUN_PATH = os.environ.get('SPICY_SERVER_RUN_PATH', '/var/run/www')
SPICY_SERVER_LOG_PATH = os.environ.get('SPICY_SERVER_LOG_PATH', '/var/log/www')


def is_package(pkg_path):
    """Check if relpath points correct package dir.

    As correct, as we want, and we want to see there:

    * `setup.py` file, which returns proper appname
    * `src` dir
    * `docs` dir
    * TODO: i think, now dir `src` is more nested than it could

    TODO: add check for package is being exactly `spicy`
    subpackage (most common way is `setup.py --name` call combining `startswith`)

    Parameters
    ----------
    pkg_path : str
        Relative path to expected package.

    Returns
    -------
    result : bool
        Why does i wrote dat line? Standard, mofuckers, dunno bout dat?

    """

    criterions = [
        'setup.py',
        'src',
        'docs',
    ]

    packdir = os.path.join(pkg_path)

    # checking routine
    for pth in criterions:
        check_path = os.path.join(packdir, pth)
        print_info('{0}> {1} checking'.format('-' * 4, check_path))
        if not os.path.exists(check_path):
            print_err('{0}> {1} failed to check if exists.'.format('-' * 8, pth))
            return False

    # it seems we have passed all checks and won. HATERS GONNA HATE ^^
    return True


def sscp(appname, user, args):
    """I don't wont to initialize Fabric environment at all.

    And it's So, just wrap `scp` system command. Feel da unixway

    """
    # cmd_str = 'scp -P {port} {app}/docs/_build/html {user}@{host}:{path}'.format(
    #     port=args.port if args.port else 22,
    #     app=appname,
    #     user=user,
    #     host=args.host,
    #     path=args.path)

    cmd_list = [
        'scp',
        '-r',
        '-P {0}'.format(args.port if args.port else 22),
        '{0}/docs/_build/html/'.format(appname),
        '{0}@{1}:{2}/{3}'.format(user, args.host, args.path, appname)
    ]

    print_info('scp would be runned with dat line:')
    print_info(cmd_list)

    """Suppress terminal output from `scp`.

    Using subprocess.PIPE, if you're not reading from the pipe,
    could cause your program to block if it generates a lot of output.
    via. http://stackoverflow.com/questions/10251391/suppressing-output-in-python-subprocess-call"""
    devnull = open('/dev/null', 'w')
    # result = subprocess.call(cmd_list, stdout=devnull, stderr=devnull)
    result = subprocess.call(cmd_list)

    if result != 0:
        #: If `scp` return success
        return False

    return True


def handle_build_docs(args):
    """`build-docs` command handler.

    Returns
    -------
    None

    """
    app_list = []
    user = str()

    if not args.user:
        user = os.getlogin()
        print_info('option --user ommited, so using system user ({})'.format(green(user)))
    else:
        user = args.user

    app_list = args.apps.split(',')

    for app in app_list:
        print_info('Starting to build docs for {}'.format(green(app)))

        pkg_abs = os.path.abspath(app)
        print_info('Searching in {}'.format(blue(pkg_abs)))
        if not is_package(pkg_abs):
            return print_err('{} is not a package'.format(green(app)))

        if not os.path.exists('{}/docs'.format(app)):
            return print_err('Application {} does not exist'.format(green(app)))

        else:
            # in docs subdir
            with lcd('./{}/docs'.format(app)):
                local('make gettext; make html;', capture=False)
            # back to pwd of command was run
            sscp(app, user, args)


def handle_create_project(ns):
    raise NotImplementedError()


def handle_create_app(ns):
    spicy_pkg_root_dir = os.path.dirname(__file__)
    spicy_app_tpl_root = os.path.join(spicy_pkg_root_dir)
    source_app_dir = os.path.join(spicy_pkg_root_dir, 'app')

    #: provide more context vars here
    template_ctx=dict(
        APPNAME=ns.appname.lower(), #: would be 'appname' in templates
        APPNAME_CLASS=ns.appname.capitalize(), #: would be 'Appname'
        APP_DESCRIPTION=ns.description
    )

    print_info('Source for new app:\n**** {}'.format(source_app_dir))

    print_info('Creating app catalog')
    dest_app_dir = os.path.join(os.getcwd(), ns.appname)

    print_info('Copying source app to dest'.format(dest_app_dir))
    print_info('{0} -> {1}'.format(cyan(source_app_dir), cyan(dest_app_dir)))

    try:
        shutil.copytree(source_app_dir, dest_app_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dest_app_dir):

            while True:
                proceed = raw_input('Overwrite existing app catalog ({})? y\\n: '.format(
                    ns.appname))
                if proceed in ['n','N']:
                    print_info('Cancel')
                    return

                if proceed not in ['y','Y']:
                    print_warn('Press y, Y, n or N')
                    continue

                if proceed in ['y', 'Y']:
                    print_warn('Overwriting')
                    shutil.rmtree(dest_app_dir)
                    shutil.copytree(source_app_dir, dest_app_dir)
                    break

    print_info('Processing new app')
    for path, subdirs, files in os.walk(dest_app_dir):
        for name in files:
            file_with_path = os.path.join(path, name)
            file_dir = os.path.dirname(file_with_path)

            if file_with_path.endswith(('.py',)):
                """Post-copying processing (template rendering)"""
                template_str = open(file_with_path, 'r').read()
                if template_str:
                    print_info('Processing now: {}'.format(green(file_with_path)))

                template = string.Template(template_str)
                #: using safe substituting, it's not throwing exceptions
                result_str = template.safe_substitute(template_ctx)
                fh = open(file_with_path, 'w+')
                fh.write(result_str)
                fh.close()


class VersionError(Exception):
    pass


class ConfigError(Exception):
    pass


class ApplicationNotFound(Exception):
    pass


class ServerError(Exception):
    pass


class Application(object):
    name = None

    version_label = None
    revision_id = None

    abspath = os.path.abspath('.')
    build_path = os.path.abspath('.')
    remote_path = None

    uwsgi_initd = '/etc/init.d/uwsgi.{version_label}-{app_name}'
    uwsgi_conf = '/etc/conf.d/uwsgi.{version_label}-{app_name}'
    nginx_conf = '/etc/nginx/vhosts.d/{version_label}-{app_name}.conf'

    def __init__(self, app_str, deployer):
        """
        :param app_str: Application string example: `foo=version-tag-label` equal to `bar=3.0.3`
        :param deployer: 


        """                    
        
        try:
            self.name, self.version_label, self.revision_id =\
                deployer._vc.get_app_version(app_str)
        except TypeError, e:
            print(traceback.format_exc())
            print_err('Check applications direcories. You current PWD is: {0}'.format(
                    os.path.abspath('.')))

        self.abspath = os.path.join(os.path.abspath('.'), self.name)

        self.build_path = os.path.join(os.path.abspath(SPICY_BUILD_DIR), self.name)
        self.req_file = os.path.join(self.build_path, SPICY_REQ_FILE)
        
        self.remote_path = os.path.join(os.path.abspath(deployer.remote_apps_path), self.name)        

        for attr in ('uwsgi_conf', 'uwsgi_initd', 'nginx_conf'):
            setattr(self, attr, getattr(self, attr).format(
                    version_label=deployer.version_label,
                    app_name=self.name
                    ))

    @property
    def rev_id(self):
        return self.revision_id

    @with_settings(sudo_user='root')
    def update_nginx(self):
        if exists(self.nginx_conf):
            sudo('rm {0}'.format(self.nginx_conf))

        sudo('ln -s {0} {1}'.format(
                os.path.join(self.remote_path, 'nginx.conf'), self.nginx_conf))
        print_ok('[done] Create Nginx vhost for app: {0}'.format(self.name))
            
    @with_settings(sudo_user='root')
    def update_uwsgi(self):
        if exists(self.uwsgi_conf):
            sudo('rm {0}'.format(self.uwsgi_conf))

        if exists(self.uwsgi_initd):
            sudo('rm {0}'.format(self.uwsgi_initd))

        sudo('ln -s {0} {1}'.format(
                os.path.join(self.remote_path, 'uwsgi.conf'), self.uwsgi_conf))
        sudo('ln -s {0} {1}'.format(
                '/etc/init.d/uwsgi', self.uwsgi_initd))
        print_ok('[done] Create uwsgi configs for app: {0}'.format(self.name))

    def restart(self):
        if self.is_webapp():
            sudo('{0} restart'.format(self.uwsgi_initd), user='root')

        if self.is_daemon():
            with cd(self.remote_path):
                sudo('./restart.sh')
            
    def is_daemon(self):
        if exists(os.path.join(self.remote_path, 'restart.sh')):
            return True
        return False

    def is_webapp(self):
        if exists(os.path.join(self.remote_path, 'nginx.conf')) \
                and exists(os.path.join(self.remote_path, 'uwsgi.conf')):
            return True
        return False
    
    def has_cron_tasks(self):
        if exists(os.path.join(self.remote_path, SPICY_APP_CRON_CONFIG)):
            return True
        return False

    def __str__(self):
        return self.name
    __unicode__ = __str__


class VersionControlBase(object):
    default_branch = 'default'
    cmd_tags = None
    cmd_build_archive = None
    cmd_revision_by_branch = None
    cmd_branch_by_revision = None

    
    def create_build(self, app):
        """Creating application ``build copy`` using defined revision label.
        
        :param app:
        :type class ``Application``

        :return: None
        """
        with lcd(app.abspath):
            local(self.cmd_build_archive % dict(
                    revision_id=app.revision_id, app_build_path=app.build_path))        

    def get_app_version(
        self, app_str, app_path=os.path.abspath('.')):
        """
        :param app_str: Application string and version code  example: 

        1) Using tag label
         foo=version-tag-label
         bar=3.0.3
         
        2) Using branch/origin
        foo@branch-name
        bar@default

        3) default definition used branch/origin @default
        `foo` is equal to `foo@default`

        4) Concrete revision hash
        foo#42079195ebd5f8134e47c71b9d7d97575fa7b416
        
        """
        if '=' in app_str:                        
            app_name, version_label = app_str.split('=')
            revision_id = self.get_revision_by_tag(
                app_name, version_label, app_path)

        elif '@' in app_str:
            app_name, branch_name = app_str.split('@')
            version_label = branch_name
            revision_id = self.get_revision_by_branch(
                app_name, branch_name, app_path)

        elif '#' in app_str:
            app_name, revision_id = app_str.split('#')
            version_label = self.get_branch_by_revision(
                app_name, revision_id, app_path)
        else:
            # use default branch last commit
            app_name = app_str
            version_label = self.default_branch
            revision_id = self.get_revision_by_branch(
                app_name, self.default_branch, app_path)

        return app_name, version_label, revision_id
        #print_err('Error while parsing app versions from string: %s'%app_str)
        #raise VersionError

    def get_branch_by_revision_id(self, app_name, revision_id, app_path):
        with lcd(os.path.join(os.path.abspath('.'), app_name)):
            branch_name = local(self.cmd_branch_by_revision % dict(revision_id=revision_id), capture=True)
            if not branch_name:
                print_err('Can not find revision data for application [{0}].\n' \
                              'Try to run deployer from dirrectory above current. $cd .. '.format(app_name))
                raise VersionError
            return branch_name

    def get_revision_by_branch(self, app_name, branch_name, app_path):              
        with lcd(os.path.join(os.path.abspath('.'), app_name)):
            revision_id = local(self.cmd_revision_by_branch % dict(branch_name=branch_name), capture=True)
            if not revision_id:
                print_err('Can not find revision data for application [{0}].\n' \
                              'Try to run deployer from dirrectory above current. $cd .. '.format(app_name))
                raise VersionError
            return revision_id

    def get_revision_by_tag(self, app_name, tag_name, app_path):              
        """Parse revision id from version control utility using  defined version label/tag.

        :param app_name:
        :param tag_name:
        :type class ``Application``

        return: revision id hash code 
        """
        raise NotImplementerError


class HgVersionControl(VersionControlBase):
    cmd_tags = 'hg tags'
    cmd_build_archive = 'hg archive -r %(revision_id)s %(app_build_path)s'

    cmd_revision_by_branch = "hg head -r %(branch_name)s --template '{node}'"
    cmd_branch_by_revision = "hg head -r %(revision_id)s --template '{branch}'"

    default_branch = 'default'

    def get_revision_by_tag(self, app_name, tag_name):                  
        with lcd(os.path.join(os.path.abspath('.'), app_name)):
            tags = local(self.cmd_tags, capture=True)
            if not tags:
                print_err('Can not find revision data for application [{0}].\n' \
                              'Try to run deployer from dirrectory above current. $cd .. '.format(app_name))
                raise VersionError

            for tagline in tags.splitlines():
                if tagline.startswith(tag_name):
                    return tagline.strip(tag_name).strip().split(':')[1]
            raise VersionError('Can not find defined tag label: {}'.format(tag_name))


VERSION_CONTROL_MAP = {
    'hg': HgVersionControl,
    #'git'
}

class Server(object):
    """Server configuration data Informer
    
    :ivar project_dirs: Directories on the remote server for project directories
    :ivar server_dirs: Directories on the server for the applicatooins files:
        PID files, log files etc. Directories where you can find a lot of files 
        from differend applications.

    """
    project_dirs = ('tmp', 'env_path', 'apps_path', 'sites_path',
                           'media_path', 'static_path')
    server_dirs = ('run_path', 'log_path',)

    host = None
    ip = None
    tmp = SPICY_SERVER_TMP_PATH

    env_path = SPICY_SERVER_APPS_ENV_PATH
    apps_path = SPICY_SERVER_APPS_PATH

    static_path = SPICY_SERVER_STATIC_PATH
    media_path = SPICY_SERVER_MEDIA_PATH

    sites_path = SPICY_SERVER_SITES_PATH

    run_path = SPICY_SERVER_RUN_PATH
    log_path = SPICY_SERVER_LOG_PATH
    
    user = SPICY_APPS_SERVER_USER
    group = SPICY_APPS_SERVER_GROUP

    requirements = SPICY_SERVER_REQUIREMENTS

    def __init__(self, host, config=None):        
        host_info = local('host {0}'.format(str(host.strip())), capture=True)        
        try:
            self.ip = host_info.splitlines()[0].split('has address')[1].strip()
        except Exception, e:
            print_err('Can not get server ip address')            
            print(traceback.format_exc())
            raise ServerError
        
        env.host_string = host
        self.host = host
        self.config = config
                            
        self.req_dirs = list(set(self.project_dirs)|set(self.server_dirs))

        # init required attributes and overwrite values using config
        self._required_dirs = map(self.get_option, self.req_dirs)

    def get_option(self, option):
        """Get attributes from current ``Server`` instance
        or overwrite using config options.
        """
        if self.config is not None:
            if option in self.config:
                
                setattr(self, option, self.config[option])
                return self.config[option]

        if hasattr(self, option):
            return getattr(self, option)
        
    def configure(self):
        """Configure server directories for correct deployment process.
        create dirs if does not exists.
        """
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            
            for path in self._required_dirs:
                if exists(path):
                    print_info('[{0}] Path exists: {1}'.format(
                            self.host, path))
                else:
                    sudo('mkdir -m ug=rwx,o= {0}'.format(path))
                    print_ok('[{0}] Creating remote directory: {1}'.format(
                            self.host, path))
        print_done('[done] {0}:{1} server configuration completed.'.format(self.host, self.ip))
        

class Database(object):
    name = ''
    user = ''
    host = '127.0.0.1'
    password = ''
    fixture = None

    def __init__(self, config=None):
        self.config = config 

        if self.config is not None:
            try:
                self.name=config['database']
                self.user=config['database_user']                
                self.password=config['database_password']
                self.fixture=self.get_fixture()

            except KeyError:
                print_err('Can not configure database settings. Check spicy.conf file.')

            try:
                self.host=config['database_host']
            except KeyError:
                pass

    def get_fixture(self):
        if 'database_fixture' in self.config:
            if os.path.exists(self.config['database_fixture']):
                return self.config['database_fixture']
        print_info('Can not get database fixture.')
        
    def create(self):
        raise NotImplementedError

    def restore_from_fixture(self):
        raise NotImplementedError
        
        
class ProjectDeployer(object):
    # TODO version label from 'deploy version_label_param + host'
    # its not flexible but more usefull
    version_label = None
    server = None
    database = Database()
    config = None
    apps = []
    static_apps = []

    def __init__(self, server, version_label, apps_string, 
                 static_string=None, version_control_util='hg', config=None, force=False):
        """
        :param server: remote server instance
        :type class ``Server``

        :param version_label: Project version label
        :type str

        :param apps_string: Example: foo=3.0.1,bar,zoo=2.1.3a
        :
        :param version_control_util: Default `hg`
        :type version_control_util str

        """        
        self.version_label = version_label
        self.server = server
        self.config = config
        self.force = force
        self.database = Database(config=config)

        self._local_tmp = os.path.join(os.path.abspath('.'), SPICY_BUILD_DIR)
        self.local_req_file = os.path.join(self._local_tmp, SPICY_REQ_FILE)

        self.server.configure()
        self.remote_tmp = os.path.join(self.server.tmp, SPICY_BUILD_DIR, self.version_label)
        self.remote_req_file = os.path.join(self.remote_tmp, SPICY_REQ_FILE)
        
        # create `remote_SERVER_PATHS` for current project
        for path_attr in self.server.req_dirs:
            attr_name = 'remote_' + path_attr
            if not hasattr(self, attr_name):
                setattr(self, attr_name,
                        os.path.join(
                        getattr(self.server, path_attr), self.version_label))
        print_ok('[done] Create directories variables for remote server. {0}'.format(
                ', '.join(self.server.req_dirs)))
        
        if config is not None:
            if 'use_custom_env' in config:
                self.remote_env_path = config['env_path']
                print_info('Overwire ENV_PATH, using custom env path from config: {0}'.format(self.remote_env_path))
            
        print_err('# TODO create remote dirs.')
        
        with settings(
            hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
            self._vc = VERSION_CONTROL_MAP[version_control_util]()
            self.apps = self._get_apps(apps_string)

            if static_string is not None:
                self.static_apps = self._get_apps(static_string)
    
            if os.path.exists(self._local_tmp):
                local('rm -rf %s' % self._local_tmp)
            local('mkdir -m ug=rwx,o= %s' % self._local_tmp)
            print_ok('[done] Make local build directory: %s' % self._local_tmp)

            # creating application ``build copy`` using defined revision label.
        # and use this ``build copy`` for requirements.txt generation, configure app. templates etc...
        for app in self.apps:
            self._vc.create_build(app)

        for app in self.static_apps:
            self._vc.create_build(app)

        self._generate_common_reqfile()
        
    def _get_apps(self, apps_string):
        """
        Parse app string to dict with app, revision number items.
        
        foo=3.0.1 or bar=any_label used to define version of application to build.
        Depend of version control utility retrun Revision useng label or tag `3.0.1`, `any label`
        If version not defined using `tip` or current revision.
        
        :param apps_string: = foo=3.0.1,bar,zoo=2.1.3a
        :type str
                
        :return: list of objects ``Application``
        """
        return map(lambda app_str: Application(
                app_str, self), apps_string.split(','))

    def _generate_common_reqfile(self):
        """Project requirements file generator using all applications

        return: local agregated requirements.txt file from all applications.
        """        
        data = []
        for app_index, app in enumerate(self.apps):
            if not os.path.exists(app.build_path):
                print_err('Application [%s] not found.' % app)
                raise ApplicationNotFound

            if os.path.exists(app.req_file):
                req_app_fd = open(app.req_file)
                print_info('[in progress] %s -> %s' % (app.req_file, self.local_req_file))

                app_reqs = []
                for req in req_app_fd.readlines():
                    req = req.strip()
                    if not req:
                        continue

                    tmp = re.split('>=|=<|=>|<=|==', req)
                    if len(tmp) == 2:
                        rmod, rmod_version = tmp
                    elif len(tmp) == 1:
                        rmod = tmp[0]
                    else:
                        print_err('Can not parse %s version error: %s' % (app.req_file, req))
                        raise VersionError

                    for module in data:
                        module = module.strip()
                        if module.startswith(rmod) and module != req:
                            print_err(
                                '[warning] While prepare requirements sequence mistmach version detected: '
                                '[%s] %s != [%s] %s' % (
                                    ','.join([str(a_) for a_ in self.apps[:app_index]]), module, app, req))
                            print_info('Don\'t forget commit changes before next deployment build.')
                            raise VersionError

                        elif module.startswith(rmod) and module == req:
                            print_info('Equal requirements [%s]: %s' % (
                            ','.join([str(a_) for a_ in self.apps[:app_index + 1]]), module))
                            break
                    else:
                        app_reqs.append(req)

                data.extend(app_reqs)
                print_ok('[done] %s in the application [%s] has been prepared.' % (SPICY_REQ_FILE, app))
            else:
                print_info('Application [%s] hasn\'t %s file.' % (app, SPICY_REQ_FILE))

        req_file_fd = open(self.local_req_file, 'a')
        req_file_fd.writelines('\n'.join(data))
        req_file_fd.close()
        print_done('[done] Common %s file generation completed.' % (SPICY_REQ_FILE))

        return self.local_req_file

    def build_remote_env(self):
        """Build remote enviroment using common for all applications requirements.

        Builder use native `virtualenv` utility. 
        """
        print_info('[in progress] Upgrade remote enviroment: {0}'.format(self.remote_env_path))
        put(self.local_req_file, self.remote_req_file)

        with shell_env(HOME=self.server.env_path, WORKON_HOME=self.server.env_path):        
            if not exists(self.remote_env_path):
                # TODO use native virtualenv or wrapper

                sudo('virtualenv --no-site-packages -p python{0} {1}'.format(
                        SPICY_SERVER_REQUIREMENTS['python'], self.remote_env_path))            
                with cd(self.remote_env_path):        
                    sudo('./bin/easy_install pip')
            
                # env wrapper
                #sudo('mkvirtualenv -r %s %s'%(self.remote_req_file, self.version_label))
                    
            with cd(self.remote_env_path):        
                with prefix('source {0}/bin/activate'.format(self.remote_env_path)):               
                    sudo('./bin/pip install -r {0} --upgrade'.format(self.remote_req_file))
    
            # wrapper
            #with prefix('workon %s'%self.version_label):
            #    sudo('pip install -r %s --upgrade'%self.remote_req_file)        

    def _copy_archive(self, path, apps):
        if exists(path):
            overwrite = self.force
            while not self.force:
                proceed = raw_input_cyan('Overwrite existing project catalog: {0}:{1}? y\\n: '.format(
                    self.server.host, path))
                if proceed in ['n', 'N']:
                    print_info('Cancel')
                    return

                if proceed not in ['y', 'Y']:
                    print_warn('Press y, Y, n or N')
                    continue

                if proceed in ['y', 'Y']:
                    overwrite = True
                    break

            if overwrite:
                print_info('Overwriting: {0}'.format(path))
                sudo('rm -rf {0}'.format(path))

        sudo('mkdir -m ug=rwx,o= {0}'.format(path))

        arch_name = '{0}-{1}.tar.bz2'.format(
            self.version_label, '-'.join(['{0}.{1}'.format(a_, a_.rev_id) for a_ in apps]))
        with lcd(self._local_tmp):
            local('tar cfj {0} {1}'.format(arch_name, ' '.join([str(a_) for a_ in apps])))
            put(arch_name, path)
            local('rm {0}'.format(arch_name))
            
        with cd(path): # and settings(hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True)
            sudo('tar -xmpf {0}/{1}'.format(path, arch_name))

    def install_server_static(self):
        self._copy_archive(self.remote_static_path, self.static_apps)          
        print_done('Static files has been uploaded.')

    def install_server_apps(self):
        """
        Copy project to the remote server. Create web applications, 
        application and all default config files from templates if original files doesnot exists.
        
        If application already installed, check diference between oroginal config files and current
        templates from ``build`` directory.

        Create LOG_DIRS, RUN_DIR, /etc/init.d/ symlinks

        # TODO configure remote nginx server for /var/www/apps/*/nginx.conf -!!!
        """
                  
        self._copy_archive(self.remote_apps_path, self.apps)          

        for app in self.apps:
            if app.is_webapp():                                
                app.update_nginx()                    
                app.update_uwsgi()
                
                with cd(app.remote_path):
                    if exists('manage.py'):
                        sudo('chmod 755 manage.py')
                    print_info('Change mode for executable files.: {0}/manage.py'.format(app.remote_path))

                sudo('/etc/init.d/nginx reload', user='root')
            
            if app.has_cron_tasks():
                print_err('[done] Configure crontab for app: {0}'.format(app.name))
                # todo cron config
                pass
            
            if app.is_daemon():
                with cd(app.remote_path):
                    sudo('chmod 755 restart.sh')
                    print_info('Change mode for executable files.: {0}/restart.sh'.format(app.remote_path))

        print_done('[done] Project has been installed successful.')

    def configure_templates(self):
        """Look in for `*.spicy` template files in the application directory recursively using subdirs.        
        Config templates use Janja2 template syntax.        
        """        
        for app in self.apps:
            for path, subdirs, files in os.walk(app.build_path):
                for file in files:
                    if file.endswith(SPICY_CONFIG_TEMPLATE_POSTFIX):
                        file_path = os.path.join(path, file)

                        fd = codecs.open(file_path, encoding='utf-8')                        
                        template = Template(fd.read())
                        fd.close()
                        
                        # BUG with 'ini.spicy'.rstrip('.spicy')
                        config = file_path.rstrip('spicy').rstrip('.') 

                        try:
                            data = template.render(spicy=self, app=app)
                        except UndefinedError, e:
                            print_err('Invalid template syntax in the config: {0}'.format(
                                    os.path.join(
                                        app.abspath, 
                                        file_path.split(app.build_path + '/')[1]
                                        ),
                                    ))
                            print(traceback.format_exc())
                            raise ConfigError(e)

                        fd = codecs.open(config, 'w', encoding='utf-8')
                        fd.write(data)
                        fd.close()

                        with settings(
                                hide('warnings', 'running', 'stdout', 'stderr'), warn_only=True):
                            local('rm {0}'.format(file_path))
                        print_ok('[done] Config has been rendered: {0}'.format(config))
        print_done('[done] All config files has been configured successful.')
    
    def restart_apps(self):        
        for app in self.apps:
            app.restart()            
            print_info('restart app: {0}'.format(app))

    def __call__(self, env_path=None, buildenv=False, 
                 createdb=False, syncdb=False):
        """Main deploy alg.
        """
        if env_path is not None:
            print_info('Overwire ENV_PATH, using custom env path from command line: {0}'.format(env_path))
            self.remote_env_path = env_path
            self.server.env_path = env_path
            self.server.configure()

        self.configure_templates()

        if bool(buildenv):
            self.build_remote_env()        

        self.install_server_apps()        
        self.install_server_static()
                    
        if createdb:
            self.database.create()

        if syncdb:
            self.sync_database()
                    
        self.restart_apps()
        print_done('Congratulation! Deploy completed.')


def handle_deploy(ns):
    if ns.port:
        env.port = ns.port

    if ns.user:
        env.user = ns.user    
    env.sudo_user = ns.sudo_user

    config = configparser.ConfigParser()
    config.read(SPICY_PROJECT_CONFIG_FILE)

    server_config = None
    if 'server' in config:
        server_config = config['server']

    if ns.xconfiglabel:
        try:
            project_config = config[ns.versionlabel]
        except KeyError:
            print_err('Check for spicy.conf file. Cannot find ``{}`` configuration.'.format(ns.versionlabel))
            sys.exit(-1)
            
        # overwrite server config using project values if exists
        for opt in project_config:
            server_config[opt] = project_config[opt]

        server = Server(project_config['host'], config=server_config)
        
        deployer = ProjectDeployer(
            server, project_config['version_label'], 
            
            # TODO ?? overwrite or exception
            project_config['apps'],
            static_string=project_config['static'], 
            config=project_config,
            force=ns.force)

        deployer(env_path=ns.envpath, buildenv=ns.buildenv, 
                 createdb=ns.createdb, syncdb=ns.syncdb)

        sys.exit(0)
    
    hosts = []
    if ns.hosts is not None:
        hosts = ns.hosts.split(',')

    for host in hosts:        
        server = Server(host, config=server_config)
        deployer = ProjectDeployer(
            server, ns.versionlabel, ns.apps, static_string=ns.static)

        deployer(env_path=ns.envpath, buildenv=ns.buildenv, 
                 createdb=ns.createdb, syncdb=ns.syncdb)
    else:
        print_info('Use spicy.conf and -x option or define deployment args manually, see --help for details.')


parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version',
                    version=spicy_version.__version__, default=False)

subparsers = parser.add_subparsers(
    title='SpicyTool commands',
    description="""You can run each command with
 key `-h` for addition options
 and parameters description""",
    help='List of script commands')

build_docs_parser = subparsers.add_parser('build-docs', help="""TODO: write help""")
build_docs_parser.add_argument('-a', '--apps', action='store')
build_docs_parser.add_argument('-H', '--host', action='store', required=True)
build_docs_parser.add_argument('-P', '--port', action='store', required=False)
build_docs_parser.add_argument('-u', '--user', action='store')
build_docs_parser.add_argument('-p', '--path', action='store', required=True)
build_docs_parser.set_defaults(func=handle_build_docs)

create_app_parser = subparsers.add_parser('create-app', help="""Create Django/Spicy application with abstract models and services using common template.
Do not forget declare youe services and applistion in the settings file.""")
create_app_parser.add_argument('appname', action='store')
create_app_parser.add_argument('-w', '--webapp', action='store', required=True, default='webapp', help="Define Web application name.")
create_app_parser.set_defaults(func=handle_create_app)

create_project_parser = subparsers.add_parser('create-project', help="""Create Spicy project from template.""")
create_project_parser.add_argument('projectname', action='store')
create_project_parser.set_defaults(func=handle_create_project)

deploy_parser = subparsers.add_parser(
    'deploy', help="""Advanced deployer build remote enviroment and application""")
deploy_parser.add_argument('versionlabel', action='store')
deploy_parser.add_argument('-H', '--hosts', action='store', default=None, help="remote hosts")
deploy_parser.add_argument('-P', '--port', action='store', default=None, help='SSH port')

deploy_parser.add_argument('-su', '--sudo_user', action='store', default=SPICY_APPS_SERVER_USER, help='Remote server user with access for APPS and ENV. ``nginx`` for example.')
deploy_parser.add_argument('-sg', '--sudo_group', action='store', default=SPICY_APPS_SERVER_GROUP, help='Group for deploy: ``nginx`` for example.')

deploy_parser.add_argument('-a', '--apps', action='store', default=None, help="List fo apps or current app(current directory by default './' )")
deploy_parser.add_argument('-s', '--static', action='store', default=None, help='Static APPS templates and JS/CSS/HTML web apps.')

deploy_parser.add_argument('-e', '--envpath', action='store', default=None, help='Define custom remote virtual enviroment path.')
deploy_parser.add_argument('-b', '--buildenv', action='store_true', default=False, help='Build custom enviroment using {0} insise each app.'.format(SPICY_REQ_FILE))

# TODO
deploy_parser.add_argument('-d', '--createdb', action='store_true', default=False, help='Create database. Use fixture for initial database sheme if defined in the config file.')
deploy_parser.add_argument('-D', '--syncdb', action='store_true', default=False, help='Syncdb in the django projects.')

deploy_parser.add_argument('-x', '--xconfiglabel', action='store_true', default=False, help='Use configuration file and defined project label. {0}'.format(SPICY_PROJECT_CONFIG_FILE))

deploy_parser.add_argument('-u', '--user', action='store', default=os.getlogin(), help='Server SSH user with sudo access.')
deploy_parser.add_argument('-f', '--force', action='store_true', default=False, help='Force overwriting all existing apps.')

deploy_parser.set_defaults(func=handle_deploy)


def handle_command_line():
    """It is like a `__main__` function in usual scripts.

    This function used as entry point for `spicy` script in setup.py

    Returns
    -------
    None

    """
    args = parser.parse_args()
    args.func(args)

    sys.exit(0)
