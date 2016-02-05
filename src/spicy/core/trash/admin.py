from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to
from .models import TrashProviderModel


@is_staff
@render_to("list.html", use_admin=True)
def index(request):
    objects = TrashProviderModel.objects.all()
    for obj in objects:
        try:
            obj.obj = obj.consumer_type.model_class().deleted_objects.get(
                pk=obj.consumer_id)
        except ObjectDoesNotExist, e:
            obj.obj = 'Error: %s' % e
        except:
            obj.obj = 'Error'
    return dict(objects=objects)


@is_staff
def restore(request, provider_id):
    prov = get_object_or_404(TrashProviderModel, pk=provider_id)
    obj = prov.consumer_type.model_class().deleted_objects.get(
        pk=prov.consumer_id)
    obj.is_deleted = False
    obj.save()
    prov.delete()
    return HttpResponseRedirect(reverse('trash:admin:index'))
