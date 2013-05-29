# coding: utf-8
"""`spicy build-docs` testing cases"""
import unittest
import subprocess

import spicy.script as tool


class TestBuildDocs(unittest.TestCase):
    """Tests for... Surprise! `build-docs` command of `spicy` tool."""

    def test_build_docs(self):
        """Trying to build docs"""

        cmd_str = 'scp ./{app}/docs/_build/html {user}@{host}:{path}'.format(
            app='spicy',
            user='user',
            host='localhost',
            path='/unixway')

        devnull = open('/dev/null', 'w')
        result = subprocess.call(cmd_str, shell=True, stdout=devnull, stderr=devnull)

        self.assertTrue(result)
