from django.conf import settings
from django.test import TestCase

from django.core.urlresolvers import reverse

#from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.webdesign.lorem_ipsum import paragraphs, words
from datetime import datetime


class BlockViewsTestCase(TestCase):
    fixtures = ['profile_testdata.json',
                'siteskin_testdata.json']

    def test_create(self):
        self.client.login(username='superuser', password='password')

        response = self.client.get(reverse('xtag:admin:create'))
        self.assertEqual(response.status_code, 200)

#         response = self.client.post(reverse('xtag:admin:create'), {
#                 'announce': paragraphs(5), 
#                 'title': 'test doc 1',
#                 'site': Site.objects.get_current().id,
#                 'pub_date': self.pub_date.strftime("%Y-%m-%d %H:%M")})
#         self.assertEqual(response.status_code, 200)
#         self.assert_("Dublicate document title in the same publication date."
#                      in response.content)

#         response = self.client.post(reverse('presscenter:admin:create'), {
#                 'announce': paragraphs(5), 
#                 'title': 'test article title',
#                 'site': Site.objects.get_current().id,
#                 'pub_date': self.pub_date.strftime("%Y-%m-%d %H:%M")})

#         self.assertEqual(response.status_code, 302)
#         self.assert_(
#             Document.objects.get(title='test article title', pub_date=self.pub_date))
