#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

__import__('pkg_resources').declare_namespace('spicy')

version = (1, 0, 2)
__version__ = '.'.join(map(str, version))


# Парсер аргументов командной строки. Олдскул, хардкор ;)
import optparse
# Цветной вывод в терминал позаимствуем у fabric, тем паче,
# что мы его используем, значит он предположительно _всегда_ поставлен
from fabric.colors import *


# Инициализируем список команд
parser = optparse.OptionParser()
parser.add_option('-n', '--name', dest='name', help='App name')
parser.add_option('-p', '--path', dest='path', help='App path')

def main():
    # парсим командную строку
    (opts, args) = parser.parse_args()

    print(red(opts.name))
    print(green(opts.path))
