"""`spicy.core.profile.models` test cases."""
import os

from django.contrib.sites.models import Site

os.environ['DJANGO_SETTINGS_MODULE'] = 'spicy.core.profile.tests.settings'

import unittest
# from django.contrib.auth.models import User
# from spicy.core.profile.utils import get_concrete_profile


import spicy
from spicy.core.profile.models import TestProfile


class TestSpicyProfileModels(unittest.TestCase):
    """Tests for `spicy.core.profile.models` module."""

    def test_profile_model(self):
        """ """
        # p = TestProfile.objects.create_inactive_user(
        #     'test@example.com',
        #     first_name='testuser',
        #     password='testpw',
        #     is_staff=True)
        #
        # self.assertEqual(p.has_usable_password(), True)

        # user = User.objects

        # Profile = get_concrete_profile()
        profile = TestProfile.objects.create_inactive_user(
            'test@email.test',
            username='test',
            password='test',
            first_name='test',
            last_name='test',
            is_staff=True,
            send_email=False,
            realhost='localhost')

        self.assertTrue(
            profile.has_usable_password())

        self.assertFalse(
            profile.check_password('badpwd'))

        self.assertTrue(
            profile.check_password('test'))

        self.assertFalse(
            profile.activation_key_expired())

        self.assertTrue(
            profile.is_authenticated())

        self.assertTrue(
            profile.is_staff)

        self.assertFalse(
            profile.is_active)
