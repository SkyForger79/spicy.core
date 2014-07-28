from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to
from spicy import utils
from spicy.core.admin.conf import AdminAppBase, AdminLink
from . import models, forms


class AdminApp(AdminAppBase):
    name = 'trash'
    label = _('Trash')
    order_number = 10

    menu_items = (
        AdminLink(
            'trash:admin:index', _('Trash'),
            models.TrashProviderModel.objects.count(),
            icon_class='icon-trash', perms='trash.change_trashprovidermodel'),
    )

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='trash.change_trashprovidermodel')
@render_to('spicy.core.trash/admin/list.html', use_admin=True)
def trash_list(request):
    nav = utils.NavigationFilter(request, accepting_filters=[
        ('consumer_type', None), ('date_deleted', None), ('search_text', '')])
    search_args, search_kwargs = [], {}

    form = forms.TrashFiltersForm(request.GET)
    if nav.search_text:
        search_args.append(
            Q(user__username__icontains=nav.search_text) |
            Q(consumer_type__name__icontains=nav.search_text)
            )

    if nav.consumer_type:
        search_args.append(
            Q(consumer_type=nav.consumer_type))

    if nav.date_deleted:
        search_kwargs['date_deleted'] = nav.date_deleted

    paginator = nav.get_queryset_with_paginator(
        models.TrashProviderModel, reverse('trash:admin:index'),
        search_query=(search_args, search_kwargs),
    )
    objects_list = paginator.current_page.object_list

    for obj in objects_list:
        try:
            obj.obj = obj.consumer_type.model_class().deleted_objects.get(
                pk=obj.consumer_id)
        except ObjectDoesNotExist, e:
            obj.obj = 'Error: %s' % e
        except:
            obj.obj = 'Error'

    return dict(
        objects_list=objects_list, paginator=paginator, nav=nav, form=form)


@is_staff(required_perms='trash.change_trashprovidermodel')
def restore(request, provider_id):
    prov = get_object_or_404(models.TrashProviderModel, pk=provider_id)
    obj = prov.consumer_type.model_class().deleted_objects.get(
        pk=prov.consumer_id)
    obj.is_deleted = False
    # For spicy.history.
    obj._action_type = 6
    obj.save()
    prov.delete()
    return HttpResponseRedirect(reverse('trash:admin:index'))
