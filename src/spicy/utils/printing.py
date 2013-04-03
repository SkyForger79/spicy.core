# coding: utf-8
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
    print(paint_text(prefix_message(message), 'red'))


def print_warning(message):
    print(paint_text(prefix_message(message), 'yellow'))


def print_info(message):
    print(paint_text(prefix_message(message), 'cyan'))


def print_success(message):
    print(paint_text(prefix_message(message), 'green'))


def print_text(message):
    """
    Print text with no additional styling, with defult color, defined by
    terminal emulator settings

    Args:
        message (str): Message to print
    """
    print(prefix_message(message))
