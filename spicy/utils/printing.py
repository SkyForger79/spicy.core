# coding: utf-8
import sys
from fabric import colors


def paint_text(text, color_name):
    """
    Paints text with color. Parameter ``color`` must be string name
    of one fabric's color

    Args:
        text (str): Text to paint
        color_name (str): Name of fabric color function
    Returns:
        str. Message, wrapped into color escape symbols (it's
            still JUST a text symbols string, as like if it
            was message="some text")
    """
    try:
        color_function = getattr(colors, color_name)
        return color_function(text)

    except AttributeError, msg:
        print('No such color', msg)
        raise ImportError, 'Error importing color'



def prefix_message(message, prefix='~> '):
    """
    Prefix message with string. Useless, but dat's so cute ^_^

    Args:
        message (str): Message to prefix
        prefix (str): Prefix string
    Returns:
        str. Prefixed message
    """
    return '{pfx}{msg}'.format(pfx=prefix, msg=message)


# So, we need just a little copy-paste but still have readable
# and obvious code. Only first function implementation documented.
def print_error(message):
    """
    Prints error red message

    Args:
        message (str): Message to print
    """
    sys.stderr.write(paint_text(prefix_message(message), 'red') + '\n')


def print_warning(message):
    sys.stdout.write(paint_text(prefix_message(message), 'yellow') + '\n')


def print_info(message):
    sys.stdout.write(paint_text(prefix_message(message), 'green') + '\n')


def print_success(message):
    sys.stdout.write(paint_text(prefix_message(message), 'green') + '\n')


def print_text(message):
    """
    Print text with no additional styling, with defult color, defined by
    terminal emulator settings

    Args:
        message (str): Message to print
    """
    sys.stdout.write(prefix_message(message) + '\n')


def spicy_info(*args):
    print_info(' '.join(str(arg) for arg in args))

def spicy_warn(*args):
    print_warning(' '.join(str(arg) for arg in args))


def sp_info(title, message):
    """"""
    sys.stdout.write('%s: %s\n' % (colors.green(title),
                                   colors.cyan(message)))


class SpicyPrintingHelper(object):
    """Print helpers."""

    def _write_stream(self, text):
        sys.stdout.write('%s\n' % (text))

    def action_info(self, action, description, color='white'):
        text = ''.join([
            paint_text(action, 'green'),
            paint_text(': ', 'blue'),
            paint_text(description, color)
        ])
        self._write_stream(text)
