# coding: utf-8
"""spicy main test cases."""
import unittest

from fabric.api import local
from fabric.colors import red, green, yellow

import spicy
import spicy.script as tool


class TestSpicy(unittest.TestCase):
    """Tests for `spicy` command."""

    def test_version(self):
        """All is up to date?"""
        self.assertEqual(spicy.__version__, '1.1')

    def test_is_not_correct_package(self):
        """It's must crush due wrong params"""
        self.assertFalse(tool.is_package('some random foo about bar'))

    def test_sscp(self):
        """It's must crush due wrong params"""
        self.assertFalse(tool.sscp(appname='foo',
                                   user='bar',
                                   host='baz',
                                   remotepath='/unixway'))
