# coding: utf-8
"""SpicyTools command handler implementation"""
from __builtin__ import input
from django.conf.locale import tr
from exceptions import OSError
from shutil import copyfile
from spicy import version

import os
import sys
import argparse
import subprocess

from fabric.colors import *
from fabric.context_managers import lcd
from fabric.api import local

# some in place helpers definitions
write_err = sys.stderr.write
write_std = sys.stdin.write

outwr = sys.stdout.write
errwr = sys.stderr.write

print_ok = lambda x: outwr(green('> {0}\n'.format(x)))
print_info = lambda x: outwr(yellow('> {0}\n'.format(x)))
print_warn = lambda x: outwr(red('> {0}\n'.format(x)))
print_err = lambda x: errwr(red('> {0}\n'.format(x)))

# Trying to get env vars
SPICY_REMOTE_SERVER = os.environ.get('SPICY_REMOTE_SERVER')
SPICY_DOCS_PATH = os.environ.get('SPICY_DOCS_PATH')

#: TODO: use that vars
env_opts = {
    'SPICY_REMOTE_SERVER': SPICY_REMOTE_SERVER,
    'SPICY_DOCS_PATH': SPICY_DOCS_PATH
}

#:
#: subutils
#:


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

def handle_create_app(ns):
    app_tpl_root = os.path.dirname(__file__)

    try:
        os.mkdir(ns.appname)
    except OSError, e:
        proceed = raw_input('Overwrite existing?')

        if proceed in ['n','N']:
            sys.exit()

        if proceed not in ['y','Y']:
            sys.exit(1)

    for path, subdirs, files in os.walk(os.path.join(app_tpl_root, 'app')):
        for name in files:
            if os.path.join(path, name).endswith(('.py',)):
                print_info(os.path.join(path, name))
                template_file = open(os.path.join(path, name))

                template_string = template_file.read()
                ctx = dict(
                    appname=ns.appname
                )
                result_string = template_string.format(**ctx)
                copyfile(os.path.join(path, name), os.path.join(ns.appname, name))

                fh = open(os.path.join(ns.appname, name), 'w+')
                fh.write(result_string)
                print(fh.read())
    #
    # for filename in files_to_process:
    #     fh = open(filename)
    #     result_str = fh.read().format(**{
    #         'appname': ns.appname
    #     })
    #     print(result_str)
    #     rendered_file = open(os.path.join(os.getcwd(), ns.appname), 'w+')
    #     print(rendered_file)
    #     rendered_file.write(result_str)
    #     rendered_file.close()

# define main parser
parser = argparse.ArgumentParser()

# add --version arg and commands subparsers
parser.add_argument('--version', action='version',
                    version=version.__version__, default=False)
# parser.add_argument('--verbose', '-v', action='count',
#                     help="ENLARGE UR VERBOSITY!")

subparsers = parser.add_subparsers(title='SpicyTool commands',
                                   description="""You can run each command with
                                               key `-h` for addition options
                                               and parameters description""",
                                   help='List of script commands')

# build-docs handler setup
build_docs_parser = subparsers.add_parser('build-docs', help="""TODO: write help""")
build_docs_parser.add_argument('-a', '--apps', action='store')
build_docs_parser.add_argument('-H', '--host', action='store', required=True)
build_docs_parser.add_argument('-P', '--port', action='store', required=False)
build_docs_parser.add_argument('-u', '--user', action='store')
build_docs_parser.add_argument('-p', '--path', action='store', required=True)
build_docs_parser.set_defaults(func=handle_build_docs)

# create app handler
create_app_parser = subparsers.add_parser('create-app', help="""TODO: write help""")
create_app_parser.add_argument('appname', action='store')
create_app_parser.set_defaults(func=handle_create_app)

def handle_command_line():
    """It is like a `__main__` function in usual scripts.

    This function used as entry point for `spicy` script in setup.py

    Returns
    -------
    None

    """

    for optname in env_opts:
        # check if env setuped
        if not env_opts[optname]:
            print(red('${} env var not set'.format(optname)))

    args = parser.parse_args()
    args.func(args)
    print(args)

    sys.exit(0)
