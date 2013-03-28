# coding: utf-8
__import__('pkg_resources').declare_namespace('spicy')
version = (1, 0, 2)
__version__ = '.'.join(map(str, version))

from fabric.colors import *


def handle_command_line():
    import sys
    import argparse

    def create_app_handler(ns):
        print(green('''Create app mock, passed name is "{name}"'''.format(name=ns.name)))
        sys.exit(0)


    def test_app_handler(ns):
        print(green('''Test app mock, passed name is "{name}"'''.format(name=ns.name)))
        sys.exit(0)


    def add_generic_arguments(parser):
        """
        Add to parser options like --verbose. It's modify
        passed parser and does not returns any result
        """
        parser.add_argument('-v', '--verbose', action='store_true')


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

    args = argparser.parse_args()
    args.func(args)

    sys.exit(0)
