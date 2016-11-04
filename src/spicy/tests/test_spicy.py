"""spicy main test cases."""
import unittest

# from fabric.api import local
# from fabric.colors import red, green, yellow

import spicy
# import spicy.script as tool


class TestSpicy(unittest.TestCase):
    """Tests for `spicy` command."""

    def test_version(self):
        """All is up to date?"""
        self.assertEqual(spicy.get_version(), '.'.join([str(x) for x in spicy.VERSION]))
