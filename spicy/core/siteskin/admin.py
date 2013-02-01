from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from spicy.core.service import api

from spicy.core.profile.decorators import is_staff

from .common import NavigationFilter
from .decorators import render_to, ajax_request
from . import defaults as sk_defaults

#from .forms import ContentBlockForm, CreateContentBlockForm
#from .models import ContentBlock


@is_staff(required_perms='siteskin.add_contentblock')
@transaction.commit_on_success
@render_to('siteskin/admin/create.html')
def create(request, content_service_name):
    message = ''
    content_provider = api.register[content_service_name].get_provider(
        ContentBlock)
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['content_service'] = api.register[
            content_service_name].instance

        form = CreateContentBlockForm(post_data)
        if form.is_valid():
            block = form.save()

            content_form = content_provider.create_inline_form(request, block)
            if content_form.is_valid():                
                content_form.save()
                return HttpResponseRedirect(
                    reverse('siteskin:admin:edit', args=[block.id]))            
            transaction.rollback()
        else:
            content_form = content_provider.create_form(prefix='provider')
        message = settings.MESSAGES['error']
    else:
        form = CreateContentBlockForm()
        content_form = content_provider.create_form(prefix='provider')
    
    return {'form': form,
            'content_form': content_form,
            'content_template': content_provider.create_template,
            'message': message}


@is_staff(required_perms='siteskin.change_contentblock')
@transaction.commit_on_success
@render_to('siteskin/admin/edit.html')
def edit(request, block_id):
    status = 'ok'
    message = ''
    block = get_object_or_404(ContentBlock, id=block_id)

    content_provider = api.register[
        block.content_service].get_provider(block)

    content_dict = content_provider.edit(request, block)

    if request.method == 'POST':
        if request.user.can_access_pub_points(
            pub_point.consumer for pub_point in block.pub_points):
            form = ContentBlockForm(request.POST, instance=block)
            if form.is_valid():
                block = form.save()            
                content_dict = content_provider.edit(
                    request, block, is_post=True)
                message = settings.MESSAGES['success']
            else:
                status = 'error'
                message = settings.MESSAGES['error']
        else:
            form = ContentBlockForm(instance=block)
            status = 'error'
            message = _(
                'You don\'t have access to publication points for this '
                'content block')
    else:
        form = ContentBlockForm(instance=block)
    
    #        'tag_prov_formset': tag_prov_formset,
    context = dict(
        form=form, status=status, message=message,
        content_service=block.content_service)
    
    # if HttpResponse redict to the /login/?=current_path from included content-service
    if isinstance(content_dict, HttpResponseRedirect):
        raise PermissionDenied

    context.update(content_dict)
    return context


def edit_by_slug(request, slug):
    block = get_object_or_404(ContentBlock, slug=slug)
    return HttpResponseRedirect(reverse('siteskin:admin:edit', args=[block.id]))



#XXX refactoring
#from xtag.models import Tag
@is_staff(required_perms='siteskin')
@render_to('siteskin/admin/list.html')
def block_list(request, year=None, month=None, day=None):
    message = request.GET.get('message', '')

    nav = NavigationFilter(
        request, default_order='-create_date',
        accepting_filters=[
        ('search_text', ''),
        ('pub_point', None),
    ])
    search_args, search_kwargs = [], {}

    if nav.search_text:
        search_args.append(Q(title__icontains = nav.search_text))

    if nav.pub_point:
        tag = Tag.on_site.get(term__slug=nav.pub_point, vocabulary__term__slug='pub_point')
        content_block_ids = [x.content_block_id for x in api.register['siteskin']['xtag'].get_instances(consumer=tag)]
        query = lambda x: x.filter(pk__in=content_block_ids,
            *search_args, **search_kwargs)
    else:
        query = lambda x: x.filter(
            *search_args, **search_kwargs)

    paginator = nav.get_queryset_with_paginator(
        ContentBlock, reverse('siteskin:admin:index'),
        search_query=query,
        obj_per_page=sk_defaults.ADMIN_OBJECTS_PER_PAGE,
        )
    objects_list = paginator.current_page.object_list

    return {
        'message': message,
        'nav': nav,
        'objects_list': objects_list,
        'paginator': paginator,
        }


@is_staff(required_perms='siteskin')
@render_to('admin/deleted_in_dialog.html')
def deleted(request):
    return dict()

@is_staff(required_perms='siteskin')
@render_to('admin/is_deleted.html')
def is_deleted(request):
    return dict()


@is_staff(required_perms='siteskin.delete_contentblock')
@render_to('siteskin/admin/delete_confirm.html')
def delete(request, block_id):
    content_block = get_object_or_404(ContentBlock, id=block_id)
    if not request.user.can_access_pub_points(
        pub_point.consumer for pub_point in content_block.pub_points):
        return {
            'status': 'error',
            'message': _('You don\'t have access to publication points for '
                         'this content block'), 'content_block': content_block}
    if request.method == 'POST':
        if 'confirm' in request.POST:
            content_block.delete()
            return HttpResponseRedirect(
                reverse('siteskin:admin:index')+
                '?message=' + unicode(
                    _('All objects have been deleted successfully')))
    return dict(content_block=content_block)


@is_staff(required_perms='siteskin.delete_contentblock')
@ajax_request
def delete_block_list(request):
    message = ''
    status = 'ok'
    try:
        for block in ContentBlock.objects.filter(
            id__in=request.POST.getlist('id')):
            if request.user.can_access_pub_points(
                pub_point.consumer for pub_point in block.pub_points):
                block.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']        
        status = 'error'
    return dict(message=unicode(message), status=status)


@is_staff(required_perms='siteskin.create_rss')
@render_to('siteskin/admin/create_rss.html')
def create_rss(request):
    return dict()
