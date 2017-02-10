from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from spicy.core.service import api
from spicy.core.service.models import ProviderModel
from spicy.core.profile.defaults import CUSTOM_USER_MODEL
from spicy.core.siteskin.threadlocals import get_current_user


class NonTrashManager(models.Manager):
    def get_query_set(self):
        query_set = super(NonTrashManager, self).get_query_set()
        return query_set.filter(is_deleted=False)


class SiteNonTrashManager(NonTrashManager):
    def get_query_set(self):
        query_set = super(SiteNonTrashManager, self).get_query_set()
        return query_set.filter(site=Site.objects.get_current())


class MultiSitesNonTrashManager(NonTrashManager):
    def get_query_set(self):
        query_set = super(MultiSitesNonTrashManager, self).get_query_set()

        # XXX for syncdb
        if connection.introspection.table_names():
            return query_set.filter(sites=Site.objects.get_current())
        return query_set


class TrashManager(models.Manager):
    def get_query_set(self):
        query_set = super(TrashManager, self).get_query_set()
        return query_set.filter(is_deleted=True)


class SiteTrashManager(TrashManager):
    def get_query_set(self):
        query_set = super(SiteTrashManager, self).get_query_set()
        return query_set.filter(site=Site.objects.get_current())


class MultiSitesTrashManager(TrashManager):
    def get_query_set(self):
        query_set = super(MultiSitesTrashManager, self).get_query_set()
        return query_set.filter(sites=Site.objects.get_current())


class MultiSitesManager(TrashManager):
    def get_query_set(self):
        query_set = super(MultiSitesManager, self).get_query_set()
        return query_set.filter(sites=Site.objects.get_current())


class TrashModel(models.Model):
    is_deleted = models.BooleanField(_('Object is deleted'), default=False)

    objects = NonTrashManager()
    deleted_objects = TrashManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, trash=True, user=None):
        """
        If trash param is True (by default) object deletes to trash.
        if trash is False - object deleted absolutely.
        """
        if not self.is_deleted and trash:
            # For spicy.history.
            self._action_type = 5
            self.is_deleted = True
            self.save()
            try:
                prov = api.register['trash'].get_provider(
                    self).create_instance(consumer=self)
                if user is None:
                    user = get_current_user()
                prov.user = user
                prov.save()
            except Exception, e:
                print u"Error while moving %s to trash: %s" % (
                    e, self)
        else:
            super(TrashModel, self).delete()


class SiteTrashModel(TrashModel):
    objects = SiteNonTrashManager()
    deleted_objects = SiteTrashManager()
    all_objects = CurrentSiteManager()

    class Meta:
        abstract = True


class MultiSitesTrashModel(TrashModel):
    objects = MultiSitesNonTrashManager()
    deleted_objects = MultiSitesTrashManager()
    all_objects = MultiSitesManager()
    on_site = objects

    class Meta:
        abstract = True


class TrashProviderModel(ProviderModel):
    date_deleted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CUSTOM_USER_MODEL, null=True, blank=True)

    class Meta:
        db_table = 'trash_provider'
        ordering = ['-date_deleted']
        unique_together = ('consumer_type', 'consumer_id')
