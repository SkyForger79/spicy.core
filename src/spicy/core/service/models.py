import datetime
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from spicy.utils import cached_property


class CustomAbstractModel(models.Model):
    @cached_property
    def ctype(self):
        return self._meta.object_name.lower()

    class Meta:
        abstract = True



class ProviderModel(models.Model):
    consumer_type = models.ForeignKey(ContentType, blank=True)
    consumer_id = models.PositiveIntegerField()
    consumer = generic.GenericForeignKey(
        ct_field='consumer_type', fk_field='consumer_id')

    date_joined = models.DateTimeField(_('Date joined'), blank=True, auto_now_add=True)

    class Meta:
        ordering = ('-date_joined',)
        abstract = True


class ContentProviderModel(ProviderModel):
    template = models.CharField(
        _('Template'), max_length=255, 
        default='default.html')

    @property
    def get_template(self):
        return self.template
        #from spicy.core.service import api
        #return api.register[
        #    self.service.name].PROVIDER_TEMPLATES_DIR + self.template
    """
    def clean_cache(self):
        cache_key = '%s:%s'%(Site.objects.get_current().domain, request.path)
        return cache.delete(cache_key)

    def get_absolute_url(self):
        return self.content_block.get_absolute_url()
    """

    class Meta:
        abstract = True


class TestProviderModel(ProviderModel):
    class Meta:
        db_table = 'test_srv_provider'


class BillingProviderModel(models.Model):
    billing_id = models.IntegerField(_('Billing PK'), blank=True, null=True)
    billing_type = models.ForeignKey(ContentType, blank=True, null=True)
    billing = generic.GenericForeignKey(
        ct_field='billing_type', fk_field='billing_id')

    activated_from = models.DateTimeField(
        _('Activated from'), blank=True, auto_now_add=False, null=True)
    activated_till = models.DateTimeField(
        _('Activated till'), blank=True, auto_now_add=False, null=True)

    expiration_period = models.PositiveIntegerField(
        _('Expiration time in seconds'), default=60*60*24*7,
        blank=False, null=False)

    is_activated = models.BooleanField(_('Is activated'), default=False)

    def activate(self):
        self.is_activated = True
        self.activated_from = datetime.datetime.now()
        self.activated_till = datetime.datetime.now() + datetime.timedelta(
            seconds=self.expiration_period)
        self.save()

    @property
    def is_active(self):
        now = datetime.datetime.now()
        return self.activated_till > now and self.activated_from < now

    def expiration_date(self):
        return self.activated_till - self.activated_from

    class Meta:
        abstract = True
        db_table = 'srv_billing_provider'
