# coding: utf-8
version = (1, 1)
__version__ = '.'.join(map(str, version))

from fabric.colors import *
from fabric.context_managers import lcd
from fabric.operations import put, local


def handle_command_line():
    import sys
    import argparse

    def add_generic_arguments(parser):
        """
        Add to parser options like --verbose. It's modify
        passed parser and does not returns any result
        """
        parser.add_argument('-v', '--verbose', action='store_true')


    def create_app_handler(ns):
        print(green('''Create app mock, passed name is "{name}"'''.format(name=ns.name)))
        sys.exit(0)


    def test_app_handler(ns):
        print(green('''Test app mock, passed name is "{name}"'''.format(name=ns.name)))
        sys.exit(0)


    def build_docs_handler(ns):
        with lcd('docs'):
            print(green('''Build docs'''))
            local('make gettext; make html')
            print(green('''Sending to remote host'''))
            put('docs/_build', ns.remote)

        sys.exit(0)


    argparser = argparse.ArgumentParser(description='''
        Spicy management tool. Add spices to taste.
        ''')
    argparser.add_argument('--version', action='version', version=__version__)
    subparsers = argparser.add_subparsers()

    create_app_subparser = subparsers.add_parser('create-app', help="Create new Spicy application")
    create_app_subparser.add_argument('name', type=str, help='Name of new application')
    add_generic_arguments(create_app_subparser)
    create_app_subparser.set_defaults(func=create_app_handler)

    test_app_subparser = subparsers.add_parser('test-app', help="Test application")
    test_app_subparser.add_argument('name', type=str, help='Name of application to test')
    add_generic_arguments(test_app_subparser)
    test_app_subparser.set_defaults(func=test_app_handler)

    build_docs_subparser = subparsers.add_parser('build-docs', help="Build docs application")
    build_docs_subparser.add_argument('remote', type=str, help='Name of application to build docs')
    add_generic_arguments(build_docs_subparser)
    build_docs_subparser.set_defaults(func=build_docs_handler)

    args = argparser.parse_args()
    args.func(args)

    sys.exit(0)
