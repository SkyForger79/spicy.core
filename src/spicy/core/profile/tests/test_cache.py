from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.test import TestCase
from spicy.core.profile.models import TestProfile


class PermissionCacheTest(TestCase):
    """
    Permission cache test.

    Mostly deals with data invalidation.
    """
    fixtures = ['profile_testdata.json']

    def setUp(self):
        cache.clear()
        self.user = None

    def login(self, username='user'):
        self.user = User.objects.get(username=username)
        self.client.login(username=username, password='123')
        self.user_key = 'Perm::User::%s' % (
            'Superuser' if self.user.is_superuser else str(self.user.pk))
        self.group_key = 'Perm::Group::%s' % (
            'Superuser' if self.user.is_superuser else str(self.user.pk))

    def all_perms(self):
        return set([
            (u'%s.%s' % perm) for perm in Permission.objects.all().values_list(
                'content_type__app_label', 'codename')])

    def group_perms(self):
        return set([
            (u'%s.%s' % perm) for perm in Permission.objects.filter(
                group__user=self.user).values_list(
                'content_type__app_label', 'codename')])

    def user_perms(self):
        return set([
            (u'%s.%s' % perm) for perm in Permission.objects.filter(
                user=self.user).values_list(
                'content_type__app_label', 'codename')])

    def test_non_existant_permission_denied(self):
        """
        Request a permission that doesn't exist.
        """
        self.login()
        non_existant_perm = 'foo.none_such_perm'
        self.assertEqual(cache.get(self.user_key), None)
        self.assertEqual(cache.get(self.group_key), None)
        self.assertEqual(self.user.has_perm(non_existant_perm), False)
        self.assertEqual(cache.get(self.user_key), set([]))
        self.assertEqual(cache.get(self.group_key), set([]))

    def test_not_granted_permission_denied(self):
        """
        Request a permission that isn't granted to the user.
        """
        self.login()
        not_granted_perm = 'shop.add_item'
        self.assertEqual(cache.get(self.user_key), None)
        self.assertEqual(cache.get(self.group_key), None)
        self.assertEqual(self.user.has_perm(not_granted_perm), False)
        self.assertEqual(cache.get(self.user_key), set([]))
        self.assertEqual(cache.get(self.group_key), set([]))

    def test_superuser_perms(self):
        """
        Check superuser permissions.
        """
        self.login('superuser')
        perm = 'shop.add_item'
        self.assertEqual(cache.get(self.user_key), None)
        self.assertEqual(cache.get(self.group_key), None)
        self.assertEqual(self.user.has_perm(perm), True)
        self.assertEqual(cache.get(self.user_key), None)
        self.assertEqual(cache.get(self.group_key), None)

        self.assertEqual(self.user.get_all_permissions(), self.all_perms())
        self.assertEqual(self.user.get_group_permissions(), self.all_perms())

    def test_granted_permission_allowed(self):
        """
        Make sure user can get his granted permission. Editor is used as an
        example.
        """
        self.login('editor')
        perm = 'presscenter.change_document'
        # Key should be added to cache.
        self.assertEqual(self.user.has_perm(perm), True)
        self.assertEqual(cache.get(self.user_key), set([]))
        self.assertEqual(cache.get(self.group_key), self.group_perms())

    def test_get_all_permissions(self):
        """
        Test get_all_permissions and get_group_permissions.
        """
        self.login('editor')
        editor_group_perms = self.group_perms()
        self.assertEqual(self.user.get_all_permissions(), editor_group_perms)
        self.assertEqual(self.user.get_group_permissions(), editor_group_perms)
        self.assert_(
            self.user.get_all_permissions().issubset(self.all_perms()))
        self.assert_(
            self.user.get_group_permissions().issubset(self.all_perms()))
        self.assertFalse(cache.get(self.user_key))
        self.assert_(cache.get(self.group_key))
        self.assert_(cache.get(self.user_key).issubset(self.all_perms()))
        self.assert_(cache.get(self.group_key).issubset(self.all_perms()))

    def test_user_permission_signals(self):
        """
        Cache invalidation on permission saving/deleting for user.
        """
        self.login('editor')
        # Get group perms in cache.
        self.assert_(self.user.get_all_permissions())
        self.assertEqual(cache.get(self.user_key), set())
        content_type = ContentType.objects.get_for_model(TestProfile)
        # Create new perm.
        perm = Permission.objects.create(
            name='change', content_type=content_type,
            codename='fake_group_perm')
        # Cache is kept.
        self.assertEqual(cache.get(self.user_key), set())
        self.user.user_permissions = [perm]

        # Login again in order to reset local object cache.
        self.login('editor')
        # Cache is empty.
        self.assertFalse(cache.get(self.user_key))
        # New perm should appear in user's permissions.
        all_perms = self.group_perms()
        all_perms.update(self.user_perms())
        self.assertEqual(self.user.get_all_permissions(), all_perms)
        self.assert_('extprofile.fake_group_perm' in all_perms)

    def test_superuser_permission_signals(self):
        """
        Cache invalidation on permission saving/deleting for superuser.
        """
        self.login('superuser')
        self.assert_(self.user.is_superuser)
        # Get group perms in cache.
        self.assertEqual(self.user.get_all_permissions(), self.all_perms())
        self.assertEqual(cache.get(self.user_key), self.all_perms())
        content_type = ContentType.objects.get_for_model(TestProfile)
        # Create new perm.
        perm = Permission.objects.create(
            name='change', content_type=content_type,
            codename='fake_group_perm')
        # Cache is kept.
        self.assertNotEqual(cache.get(self.user_key), self.all_perms())
        self.user.user_permissions = [perm]
        # Cache is not empty.
        self.assertFalse(cache.get(self.user_key))

        # Login again in order to reset local object cache.
        self.login('superuser')
        # New perm should appear in user's permissions.
        self.assertEqual(self.user.get_all_permissions(), self.all_perms())
        self.assertEqual(cache.get(self.user_key), self.all_perms())
        self.assert_('extprofile.fake_group_perm' in self.all_perms())

    def test_group_permission_signals(self):
        """
        Cache invalidation on permission saving/deleting for user group.
        """
        self.login('editor')
        # Get group perms in cache.
        self.assert_(self.user.get_group_permissions())
        self.assert_(cache.get(self.group_key))
        content_type = ContentType.objects.get_for_model(TestProfile)
        # Create new perm.
        perm = Permission.objects.create(
            name='change', content_type=content_type,
            codename='fake_group_perm')
        # Cache is not cleared.
        self.assert_(cache.get(self.group_key))
        group = self.user.groups.get()
        group.permissions = [perm]
        # Cache is cleared.
        self.assertFalse(cache.get(self.group_key))

        # Login again in order to reset local object cache.
        self.login('editor')
        # New perm should appear in user's permissions.
        group_perms = self.group_perms()
        self.assertEqual(self.user.get_group_permissions(), group_perms)
        self.assert_('extprofile.fake_group_perm' in group_perms)



