from django.test import TestCase
from django.core.urlresolvers import reverse

__all__ = ['ProfileMixinTestCase',]

# BBB deprecated. remove
class ProfileMixin(TestCase):
    fixtures = ['profile_testdata.json']
    #urls = 'profile.urls'

    def signin(self, username='superuser', password='password'):
        response = self.client.post(reverse('profile:public:signin'), {
            'username': username,
            'password': password
            }
        )
        self.assertEqual(response.status_code, 302)

    def signout(self):
        response = self.client.get(reverse('profile:public:signout'))
