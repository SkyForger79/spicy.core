# coding: utf-8
"""
Stuff for simplify styled console printing
"""
from __future__ import unicode_literals
# Reusing fabric colors submodule. Why not?
from fabric.colors import *


def paint_text(message, color):
    """
    Paints message with color

    Args:
        message (str): Message to paint
        color (function): Any color function from fabric.colors
    Returns:
        str. Message, wrapped into color escape symbols (it's
            still JUST a text symbols string, as like if it
            was message="some text")
    """
    return color(message)


def prefix_message(message, prefix='~> '):
    """
    Prefix message with string. Useless, but dat's so cute ^_^

    Args:
        message (str): Message to prefix
        prefix (str): Prefix string
    Returns:
        str. Prefixed message
    """
    return '{msg}{pfx}'.format(msg=message, pfx=prefix)


# So, we need just a little copy-paste but still have readable
# and obvious code. Only first function implementation documented.
def print_error(message):
    """
    Prints error red message

    Args:
        message (str): Message to print
    """
    print(prefix_message(paint_text(message, red)))


def print_warning(message):
    print(prefix_message(paint_text(message, red)))


def print_info(message):
    print(prefix_message(paint_text(message, red)))


def print_success(message):
    print(prefix_message(paint_text(message, red)))


def print_text(message):
    """
    Print text with no additional styling, with defult color, defined by
    terminal emulator settings

    Args:
        message (str): Message to print
    """
    print(prefix_message(message))
