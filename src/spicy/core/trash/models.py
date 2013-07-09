from django.db import models
from django.utils.translation import ugettext_lazy as _

from spicy.core.service import api
from spicy.core.service.models import ProviderModel
from spicy.core.profile.defaults import CUSTOM_USER_MODEL
from spicy.core.siteskin.threadlocals import get_current_user


class NonTrashManager(models.Manager):
    def get_query_set(self):
        query_set = super(NonTrashManager, self).get_query_set()
        return query_set.filter(is_deleted=False)

class TrashManager(models.Manager):
    def get_query_set(self):
        query_set = super(TrashManager, self).get_query_set()
        return query_set.filter(is_deleted=True)


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
            self.is_deleted = True
            self.save()
            try:
                prov = api.register['trash'].get_provider(
                    self).create_instance(consumer=self)
                if user is None:
                    user = get_current_user()
                prov.user = user
                prov.save()
            except:
                print u"@@ Object %s already in trash" % self
        else:
            super(TrashModel, self).delete()


class TrashProviderModel(ProviderModel):
    date_deleted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CUSTOM_USER_MODEL, null=True, blank=True)

    class Meta:
        db_table = 'trash_provider'
        ordering = ['-date_deleted']
        unique_together = ('consumer_type', 'consumer_id')
