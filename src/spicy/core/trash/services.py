from django.utils.translation import ugettext_lazy as _
from spicy.core.service import api


class TrashProvider(api.Provider):
    model = 'trash.models.TrashProviderModel'


class TrashService(api.Interface):
    name = 'trash'
    label = _('Trash provider service')

    provider_schema = dict(GENERIC_CONSUMER=TrashProvider)
