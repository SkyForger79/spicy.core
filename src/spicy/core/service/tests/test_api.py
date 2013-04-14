from django.utils.translation import ugettext_lazy as _

from django.test import TestCase

from django.db import models

from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from spicy.core.service import api
from spicy.core.service.api import GENERIC_CONSUMER

class ServiceProviderForUser(api.Interface):
    name = 'test_service_for_user'
    label = _('Test Service for User')
    
    provider_schema = dict(
        user = api.BillingProvider,
        )


class FakeService:
    pass


class ServiceProviderForAll(api.Interface):
    name = 'test_service_for_all'
    label = _('Test Service for All')
    
    provider_schema = dict(
        GENERIC_CONSUMER=api.BillingProvider
        )


class ServiceRegisterTestCase(TestCase):
    def setUp(self):
        api.register.add(ServiceProviderForUser)
        api.register.add(ServiceProviderForAll)

    def tearDown(self):
        api.register.remove('test_service_for_user')
        api.register.remove('test_service_for_all')

    def test_register(self):
        self.assertTrue('test_service_for_user' in api.register)
        self.assertTrue('test_service_for_all' in api.register)

    def test_register_fake(self):
        self.assertRaises(api.WrongServiceAPI, api.register.add, FakeService)
        
    def test_remove(self):
        api.register.remove('test_service_for_user')
        self.assertFalse('test_service_for_user' in api.register)
        api.register.add(ServiceProviderForUser)
    
    def test_does_not_exist(self):
        self.assertRaises(api.ServiceDoesNotExist,
                          api.register.remove, 'test_service_fake')


class ProviderTestCase(TestCase):
    def setUp(self):
        self.consumer, created = User.objects.get_or_create(username='test')
                
        api.register.add(ServiceProviderForUser)
        api.register.add(ServiceProviderForAll)

    def tearDown(self):
        api.register.remove('test_service_for_user')
        api.register.remove('test_service_for_all')

#     def test_settings_init(self):
#         api.register.remove('test_service_for_user')

#         self.assertTrue(isinstance(ServiceProviderForUser.model, str))
        
#         api.register.add(ServiceProviderForUser)
#         self.assertTrue(isinstance(
#                 ServiceProviderForUser.model, models.Model))
        

    def test_get_provider(self):
        #provider = api.register.get(
        #    'test_service_for_all', self.consumer_1)
        assert 'TODO' == True

    def test_getitem(self):
        assert 'TODO' == True

    def test_class_view(self):
        provider = api.register.get(
            'test_service_for_user', self.consumer)
        response = self.client.get(
            reverse('service:admin:test_service_for_user_user', 
                    args=[self.consumer.id]))
        self.assertEqual(response.status_code, 200)


        provider = api.register.get(
            'test_service_for_user', self.consumer)
        response = self.client.get(
            reverse('service:admin:test_service_for_all', 
                    args=['user', self.consumer.id]))
        self.assertEqual(response.status_code, 200)


class ServiceInterfaceTestCase(TestCase):
    def setUp(self):
        self.consumer_1, created = User.objects.get_or_create(username='test')
        self.consumer_2, created = User.objects.get_or_create(username='test2')

        self.current_site = Site.objects.get_current()
                
        api.register.add(ServiceProviderForUser)
        api.register.add(ServiceProviderForAll)
        
    def tearDown(self):
        api.register.remove('test_service_for_user')
        api.register.remove('test_service_for_all')

    def test_sites(self):
        api.register[
            'test_service_for_user'].enable_site(self.current_site)
        self.assertEqual(
            list(api.register['test_service_for_user'].get_sites()), 
            [self.current_site])
        
        api.register[
            'test_service_for_user'].disable_site(self.current_site)
        self.assertEqual(
            list(api.register['test_service_for_user'].get_sites()), [])

    def test_schema_error(self):
        is_ok = False
        try:
            all_provider = api.register.get(
                'test_service_for_user', self.current_site)
        except api.ProviderSchemaError:
            is_ok = True
        self.assertTrue(is_ok)

    def test_get_provider_ctype(self):
        """Get provider instance for the defined content_type, 
        using provider's schema.
        """
        user_provider = api.register.get(
            'test_service_for_user', self.consumer_1)
        self.assertEqual(user_provider.instance.consumer_id, self.consumer_1.id)


    def test_get_provider(self):
        """Get provider for * (all) content_types.
        """
        all_provider = api.register.get(
            'test_service_for_all', self.consumer_2)
        assert all_provider.instance.consumer_id == self.consumer_2.id
        
        all_provider = api.register.get(
            'test_service_for_all', self.current_site)
        assert all_provider.instance.consumer_id == self.current_site.id
