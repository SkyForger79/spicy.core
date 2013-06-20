from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.forms.models import modelformset_factory

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.csrf import csrf_protect

from spicy.core.siteskin.common import NavigationFilter
from spicy.core.siteskin.decorators import render_to, ajax_request

from spicy.core.profile.decorators import is_staff

from .models import TrashProviderModel

@is_staff
@render_to("list.html", use_admin=True)
def index(request):
    objects = TrashProviderModel.objects.all()
    for obj in objects:
        try:
            obj.obj = obj.consumer_type.model_class().deleted_objects.get(pk=obj.consumer_id)
        except ObjectDoesNotExist, e:
            obj.obj = 'Error: %s'%e
        except:
            obj.obj = 'Error'
    return dict(objects=objects)


@is_staff
def restore(request, provider_id):
    prov = get_object_or_404(TrashProviderModel, pk=provider_id)
    obj = prov.consumer_type.model_class().deleted_objects.get(pk=prov.consumer_id)
    obj.is_deleted = False
    obj.save()
    prov.delete()
    return HttpResponseRedirect(reverse('trash:admin:index'))
