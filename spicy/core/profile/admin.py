# coding: utf-8
from . import defaults, forms
from .decorators import is_staff
from .models import BlacklistedIP
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from spicy.core.profile.utils import get_concrete_profile
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.core.siteskin import defaults as sk_defaults
from spicy.utils import NavigationFilter, make_slug

Profile = get_concrete_profile()



@is_staff
def main(request):
    for app in defaults.APP_ORDER:
        if isinstance(app, basestring):
            module = app
        else:
            module, app = app
        if request.user.has_module_perms(app):
            return HttpResponseRedirect(reverse('%s:admin:index' % module))
    else:
        raise PermissionDenied(_("Unable to redirect to main page"))
        

@is_staff(required_perms='extprofile.change_profile')
@ajax_request
def passwd(request, profile_id):
    message = ''
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = forms.AdminPasswdForm(profile, request.POST)
        if form.is_valid():
            form.save()
            message = settings.MESSAGES['success']
        else:
            print '###', form.errors
            message = settings.MESSAGES['error']
        
    return dict(message=unicode(message),)


@is_staff(required_perms='extprofile.add_profile')
@render_to('spicy.core.profile/admin/create.html', use_admin=True)
def create(request):
    message = None
    if request.method == 'POST':
        form = forms.CreateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(realhost=request.get_host())
            return HttpResponseRedirect('/admin/profile/%s/?action=new' % profile.id)
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.CreateProfileForm(initial={
                'email_activation_key': True})
    return {
        'form': form,
        'message': message}


@is_staff(required_perms='auth.change_group')
@render_to('spicy.core.profile/admin/groups.html', use_admin=True)
def groups(request):   
    message = None
    if request.method == 'POST':
        groups = forms.GroupFormSet(request.POST, request.FILES, 
                              queryset=Group.objects.all())
        if groups.is_valid():
            groups.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        groups = forms.GroupFormSet(queryset=Group.objects.all())
    return {
        'groups': groups,
        'message': message,
        }                


@is_staff(required_perms='auth.add_group')
@render_to('spicy.core.profile/admin/create_group.html', use_admin=True)
def create_group(request):
    if request.method == 'POST':
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            form.save()
            redirect = reverse(
                'profile:admin:groups'
                if request.user.has_perm('auth.change_group')
                else 'profile:admin:index')
            return HttpResponseRedirect(redirect)
    else:
        form = forms.GroupForm()
    return {'group_form': form}


@is_staff(required_perms='auth.delete_group')
@render_to('spicy.core.profile/admin/delete_group.html', use_admin=True)
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            group.delete()
            return HttpResponseRedirect(reverse('profile:admin:groups'))    
    return {'group': group}


@is_staff(required_perms=(('extprofile.change_profile',),
                          ('extprofile.view_profile',)))
@render_to('spicy.core.profile/admin/edit.html', use_admin=True)
def edit(request, profile_id):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    message = None
    action = request.GET.get('action') # what do we gonna doin?
    profile = get_object_or_404(Profile, id=profile_id)

    if action == 'new':
        message = _('New account created, welcome to editing.')

    if request.method == 'POST' and request.user.has_perm(
        'extprofile.change_profile'):
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.ProfileForm(instance=profile)

    passwd_form = forms.AdminPasswdForm(profile)

    return { # TODO: needs to be Context()?
        'action': action,
        'profile': profile, 
        'form': form,
        'passwd_form': passwd_form,
        'message': message,
        'services': api.register.get_list(consumer=profile)
    }


@is_staff(required_perms='extprofile.moderate_profile')
@render_to('spicy.core.profile/admin/moderate.html', use_admin=True)
def moderate(request, profile_id):
    message = None
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = forms.ModerateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        form = forms.ModerateProfileForm(instance=profile)
    return {'profile': profile, 'form': form, 'message': message}


@is_staff(required_perms='extprofile')
@render_to('spicy.core.profile/admin/list.html', use_admin=True)
def profiles_list(request):
    nav = NavigationFilter(request, accepting_filters=[
        ('group', None), ('search_text', ''), ('is_staff', None),
        ('last_login', None)])
    search_args, search_kwargs = [], {}
    form = forms.ProfileFiltersForm(request.GET)

    if nav.search_text:
        search_args.append(
            Q(username__icontains = nav.search_text) |
            Q(email__icontains = nav.search_text) |
            Q(first_name__icontains = nav.search_text) |
            Q(last_name__icontains = nav.search_text))
        
    is_staff = request.GET.get('is_staff', False)
    if nav.is_staff:
        is_staff = is_staff != 'false'        
        search_kwargs['is_staff'] = is_staff
    
    if is_staff != False and nav.group:
        search_args.append(Q(groups=nav.group))        
    
    if nav.last_login == 'month':
        search_kwargs['last_login__gte'] = datetime.today() - timedelta(30)
    
    paginator = nav.get_queryset_with_paginator(
        Profile, reverse('profile:admin:index'),
        search_query=(search_args, search_kwargs),
        obj_per_page=sk_defaults.ADMIN_OBJECTS_PER_PAGE, 
    )
    objects_list = paginator.current_page.object_list


    # mock_profiles = []

    mock_paginator = nav.get_queryset_with_paginator(
        Profile, reverse('profile:admin:index'),
        search_query=(search_args, search_kwargs),
        obj_per_page=1,
    )
    objects_list = mock_paginator.current_page.object_list


    return {
        'nav': nav, 'objects_list': objects_list, 'paginator': paginator,
        'is_staff': is_staff, 'form': form}


@is_staff(required_perms='extprofile.delete_profile')
@ajax_request
def delete_profile_list(request):
    message = ''
    status = 'ok'
    try:
        for profile in Profile.objects.filter(
            id__in=request.POST.getlist('id')):
            profile.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    return dict(message=unicode(message), status=status)


@is_staff(required_perms="extprofile.change_profile")
@ajax_request
def resend_activation(request, profile_id):
    try:
        profile = Profile.objects.get(pk=profile_id)
        if profile.check_activation():
            message = _('Profile is already active')
            status = 'error'
        else:
            profile.generate_activation_key(realhost=request.get_host())
            message = ''
            status = 'ok'
    except Profile.DoesNotExist:
        message = _('Unable to send activation key, please try again later')
        status = 'error'
    return {'message': message, 'status': status}


@is_staff
@ajax_request
def profile_autocomplete(request, form_input_name, staff=None):
    search = request.GET.get('search')
    staff_filter = {}
    if staff == 'staff':
        staff_filter['is_staff'] = True
    users = Profile.objects.filter(
        Q(username__icontains=search) | Q(first_name__icontains=search) |
        Q(last_name__icontains=search) | Q(email__icontains=search),
        **staff_filter)[:20]
    result = map(
        lambda user: {'text': '%s (%s)' % (user.fullname(), user.email),
                      form_input_name: user.id},
        users)
    return dict(result=result)


@is_staff
@ajax_request
def last_created(request, form_input_name, staff_only=False):
    users = Profile.objects.all()
    if staff_only:
        users = users.filter(is_staff=True)
    return dict(
        result=[{form_input_name: user.id,
                 'text': '%s (%s)' % (user.fullname(), user.email)}
                for user in users[:20]])


@is_staff(required_perms='extprofile')
@render_to('spicy.core.profile/blacklisted_ips.html', use_admin=True)
def blacklisted_ips(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(
        BlacklistedIP, reverse('profile:admin:blacklisted-ips'),
        obj_per_page=sk_defaults.ADMIN_OBJECTS_PER_PAGE, 
        )
    objects_list = paginator.current_page.object_list

    return {'nav': nav, 'objects_list': objects_list, 'paginator': paginator}


@is_staff(required_perms='extprofile.delete_blacklistedip')
@ajax_request
def delete_blacklisted_ips(request):
    message = ''
    status = 'ok'
    try:
        for ip in BlacklistedIP.objects.filter(
            id__in=request.POST.getlist('id')):
            ip.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    return dict(message=unicode(message), status=status)
