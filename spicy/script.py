#!/usr/bin/env python
import os
import sys
import argparse
import subprocess
import tarfile
import shutil
import errno
import string
from importlib import import_module

version = __import__('spicy').get_version()
import spicy
from spicy.utils.printing import *
# from django.utils.translation import ugettext_lazy as _

from fabric.context_managers import lcd
from fabric.api import local

# Trying to get env vars
SPICY_REMOTE_SERVER = os.environ.get('SPICY_REMOTE_SERVER')
SPICY_DOCS_PATH = os.environ.get('SPICY_DOCS_PATH')

#: TODO: use that vars
env_opts = {
    'SPICY_REMOTE_SERVER': SPICY_REMOTE_SERVER,
    'SPICY_DOCS_PATH': SPICY_DOCS_PATH
}

ph = SpicyPrintingHelper()
#: define main parser
parser = argparse.ArgumentParser()
#: add `--version` arg and commands subparsers
parser.add_argument('--version', action='version',
                    version=spicy.get_version(), default=False)

subparsers = parser.add_subparsers(title='Spicy tool',
                                   description="""desc.""",
                                   help='help text')



def handle_build_docs(args):
    """Handler function for `build-docs` command."""

    ph.action_info('running', 'handle_build_docs', 'green')
    app_list = []
    if args.apps:
        app_list = args.apps.split(',')
        ph.action_info('Apps list:', app_list, 'green')

    for app in app_list:
        spicy_info('Processing application:',
                   paint_text(app, 'cyan'))
        app_module = import_module(app)
        app_dir = os.path.dirname(app_module.__file__)
        docs_catalog = os.path.join(app_dir, '../../docs')

        with lcd(docs_catalog):
            ph.action_info('building docs in:',
                           docs_catalog, 'cyan')
            # local('make gettext', capture=False)
            local('make html;', capture=False)

        sp_info('Done building docs for', app)

    return True


def handle_upload_docs(args):
    """Handler function for `upload-docs` command."""

    ph.action_info('running', 'handle_upload_docs', 'green')
    user = args.user if args.user else os.environ.get('USER')

    app_list = []
    if args.apps:
        app_list = args.apps.split(',')
    spicy_info('Apps list:', app_list)

    for app in app_list:
        ph.action_info('processing application:', app, 'cyan')

        try:
            app_module = import_module(app)
        except ImportError:
            ph.action_info('import_module(%s)' % (app), 'failed', 'red')
            sys.exit(1)

        app_dir = os.path.dirname(app_module.__file__)
        docs_catalog = os.path.join(app_dir, 'docs')

        try:
            if not os.path.exists(docs_catalog):
                ph.action_info('Path does not exist', docs_catalog, 'red')
                sys.exit(1)

            ph.action_info('packing docs dir into tar archive for single-file '
                           'transferring', docs_catalog, 'cyan')
            docs_tarfile = tarfile.open('/tmp/%s_docs.tar.gz' % (app), 'w:gz')
            for dirpath, dirnames, filenames in os.walk(docs_catalog):
                for filename in filenames:
                    relative_filename = os.path.relpath(
                        os.path.join(dirpath, filename), '.')
                    docs_tarfile.add(relative_filename)
            docs_tarfile.close()

            command = [
                'scp', '-C', '-c', 'arcfour', '-r',
                '-P', str(args.port),
                docs_tarfile.name,
                '{0}@{1}:{2}'.format(user, args.host, args.path)
            ]
            ph.action_info('uploading docs tarfile command',
                           ' '.join(command), 'cyan')
            subprocess.call(command)

            command = [
                'ssh', '-c', 'arcfour',
                '-p', str(args.port),
                '%s@%s' % (user, args.host),
                '/bin/bash -c "tar -xzf %s/%s -C %s"' % (args.path,
                                                         os.path.basename(docs_tarfile.name),
                                                         args.path)
            ]
            ph.action_info('unpacking remote docs tar command',
                           ' '.join(command), 'cyan')
            subprocess.call(command)



        except OSError as e:
            sp_info('upload-docs', 'failed')

            if e.errno == 2:
                sp_info('upload-docs', """%s: %s. Probably, you have not build
                                       docs yet""" % (e.strerror, e.filename))


def handle_create_app(args):
    """Handler function for `create-app` command."""

    spicy_dir = os.path.dirname(__file__)
    app_template_dir = os.path.join(spicy_dir, 'app')
    dest_app_dir = os.path.join(os.getcwd(), args.appname)

    #: provide more context vars here
    template_ctx=dict(
        APPNAME=args.appname.lower(), #: would be 'appname' in templates
        APPNAME_CLASS=args.appname.capitalize(), #: would be 'Appname'
        APP_DESCRIPTION=args.description
    )

    try:
        shutil.copytree(app_template_dir, dest_app_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dest_app_dir):

            while True:
                proceed = raw_input('Overwrite existing app catalog ({})? y\\n: '.format(
                    args.appname))
                if proceed in ['n','N']:
                    print_info('Do not overwrite', 'app dir exists', 'red')
                    sys.exit()
                if proceed not in ['y','Y']:
                    print_info('', 'press y, Y, n or N')
                    continue
                if proceed in ['y', 'Y']:
                    print_info('Overwriting')
                    shutil.rmtree(dest_app_dir)
                    shutil.copytree(app_template_dir, dest_app_dir)
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
                    print_info('Processing now: %s' % (file_with_path))

                template = string.Template(template_str)
                #: using safe substituting, it's not throwing exceptions
                result_str = template.safe_substitute(template_ctx)
                fh = open(file_with_path, 'w+')
                fh.write(result_str)
                fh.close()
    print_info('Application created successfully')

#
# Build docs command parser
#
builddocs_parser = subparsers.add_parser('build-docs', help="""TODO: write help""")
builddocs_parser.add_argument('-a', '--apps', action='store', required=True)
builddocs_parser.set_defaults(func=handle_build_docs)

upload_docs_parser = subparsers.add_parser('upload-docs', help='')
upload_docs_parser.add_argument('-a', '--apps', action='store', required=True)
upload_docs_parser.add_argument('-H', '--host', action='store', required=True)
upload_docs_parser.add_argument('-P', '--port', action='store', default=22)
upload_docs_parser.add_argument('-u', '--user', action='store')
upload_docs_parser.add_argument('-p', '--path', action='store', required=True)
upload_docs_parser.set_defaults(func=handle_upload_docs)

create_app_parser = subparsers.add_parser('create-app', help='')
create_app_parser.add_argument('appname', action='store')
create_app_parser.add_argument('-d', '--description', action='store', default='generic description')
create_app_parser.set_defaults(func=handle_create_app)


def handle_command_line():
    """It is like a `__main__` function in usual scripts.

    This function used as entry point for `spicy` script in setup.py
    """

    args = parser.parse_args()
    args.func(args)

    sys.exit(0)
