from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db.models import Q
from django import http
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from spicy.core.admin import conf, defaults as admin_defaults
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.core.siteskin.decorators import APIResponse, APIResponseFail
from spicy import utils
from spicy.utils.permissions import perm, change_perm, add_perm, delete_perm
from . import defaults, forms
from .decorators import is_staff
from .models import BlacklistedIP


Profile = utils.get_custom_model_class(defaults.CUSTOM_USER_MODEL)

admin.site.register(Profile)


class AdminApp(conf.AdminAppBase):
    name = 'profile'
    label = _('Profile')
    order_number = 10

    menu_items = (
        conf.AdminLink(
            'profile:admin:create', _('Create profile'),
            perms=add_perm(defaults.CUSTOM_USER_MODEL)),
        conf.AdminLink(
            'profile:admin:index', _('All profiles'),
            perms=change_perm(defaults.CUSTOM_USER_MODEL)),
        conf.AdminLink(
            'profile:admin:create-group', _('Create group'),
            perms='auth.add_group'),
        conf.AdminLink(
            'profile:admin:groups', _('Groups & Permissions'),
            perms='auth.change_group'),
    )

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    dashboard_links = [
        conf.AdminLink(
            'profile:admin:create', _('Create user'), Profile.on_site.count(),
            'icon-user', perms=add_perm(defaults.CUSTOM_USER_MODEL))]
    dashboard_lists = [
        conf.DashboardList(
            _('New users'), 'profile:admin:edit',
            Profile.on_site.order_by('-id'), 'date_joined',
            change_perm(defaults.CUSTOM_USER_MODEL))]


@is_staff(required_perms=change_perm(defaults.CUSTOM_USER_MODEL))
@ajax_request
def passwd(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        form = forms.AdminPasswdForm(profile, request.POST)
        if form.is_valid():
            form.save()
            return APIResponse(messages=[_('Password successfully changed.')])
        return APIResponseFail(errors=[unicode(form.errors.as_text())])

    return APIResponse(
        messages=[
            _('Not enough parametes has been passed. Use POST request.')])


@is_staff(required_perms=add_perm(defaults.CUSTOM_USER_MODEL))
@render_to('create.html', use_admin=True)
def create(request):
    message = None
    CreateProfileForm = utils.load_module(defaults.ADMIN_CREATE_PROFILE_FORM)
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(realhost=request.get_host())
            return HttpResponseRedirect(
                '/admin/profile/%s/?action=new' % profile.id)
        else:
            message = settings.MESSAGES['error']
    else:
        form = CreateProfileForm(
            initial={'email_activation_key': True})
    return {
        'form': form,
        'message': message}


@is_staff(required_perms='auth.change_group')
@render_to('groups.html', use_admin=True)
def groups(request):
    """Groups list/formset combined view."""
    message = None
    if request.method == 'POST':
        groups = forms.GroupFormSet(
            request.POST, request.FILES, queryset=Group.objects.all())
        if groups.is_valid():
            groups.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        groups = forms.GroupFormSet(queryset=Group.objects.all())
    return {
        'group_formset': groups,
        'message': message,
    }


@is_staff(required_perms='auth.add_group')
@render_to('create_group.html', use_admin=True)
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
@render_to('delete_group.html', use_admin=True)
def delete_group(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            group.delete()
            return HttpResponseRedirect(reverse('profile:admin:groups'))
    return {'group': group}


@is_staff(required_perms=change_perm(defaults.CUSTOM_USER_MODEL))
@render_to('edit.html', use_admin=True)
def edit(request, profile_id):
    """Handles edit requests, renders template according `action`
    get parameter

    """
    message = None
    action = request.GET.get('action')
    profile = get_object_or_404(Profile, id=profile_id)
    ProfileForm = utils.load_module(defaults.ADMIN_EDIT_PROFILE_FORM)

    if action == 'new':
        message = _('New account created, welcome to editing.')

    if (request.method == 'POST' and request.user.has_perm(
            'profile.change_profile')):
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            message = settings.MESSAGES['success']
        else:
            message = settings.MESSAGES['error']
    else:
        form = ProfileForm(instance=profile)

    passwd_form = forms.AdminPasswdForm(profile)

    return {
        'action': action, 'instance': profile, 'form': form,
        'passwd_form': passwd_form, 'message': message,
        'services': api.register.get_list(consumer=profile), 'tab': 'edit'}


@is_staff(required_perms=change_perm(defaults.CUSTOM_USER_MODEL))
@render_to('edit_media.html', use_admin=True)
def edit_media(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    model = defaults.CUSTOM_USER_MODEL.split('.')[1].lower()
    return {'instance': profile, 'tab': 'media', 'model': model}


@is_staff(required_perms=delete_perm(defaults.CUSTOM_USER_MODEL))
@render_to('delete.html', use_admin=True)
def delete(request, profile_id):
    message = ''
    profile = get_object_or_404(Profile, id=profile_id)
    if request.POST.get('confirm', False):
        profile.delete()
        return HttpResponseRedirect(reverse('profile:admin:index'))
    return {
        'message': message, 'instance': profile}


@is_staff(required_perms=perm(defaults.CUSTOM_USER_MODEL, 'moderate'))
@render_to('moderate.html', use_admin=True)
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


@is_staff(required_perms='profile')
@render_to('list.html', use_admin=True)
def profiles_list(request):
    nav = utils.NavigationFilter(request, accepting_filters=[
        ('group', None), ('search_text', ''), ('is_staff', None),
        ('last_login', None)])
    search_args, search_kwargs = [], {}
    form = forms.ProfileFiltersForm(request.GET)
    status = 'ok'
    message = ''

    if nav.search_text:
        search_args.append(
            Q(username__icontains=nav.search_text) |
            Q(email__icontains=nav.search_text) |
            Q(first_name__icontains=nav.search_text) |
            Q(last_name__icontains=nav.search_text))

    if 'export' in request.POST and request.user.is_superuser:
        form = forms.ProfileUploadForm(request.POST, request.FILES)
        form.is_valid()
        if form.cleaned_data['file_kind'] == u'0':
            queryset = Profile.objects.filter(pk__in=nav.get_queryset_ids(
                Profile, search_query=(search_args, search_kwargs)))
            columns_form = forms.DynamicProfileColumnForm(
                request.POST, prefix='columns')
            columns_form.is_valid()
            columns = [
                col[0] for col in columns_form.cleaned_data.iteritems()
                if col[1]]
            items = queryset.export_data(columns)
            response = http.HttpResponse(
                items, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=profiles.xls'
            return response
        else:
            raise NotImplementedError

    elif 'import' in request.POST and request.user.is_superuser:
        form = forms.ProfileUploadForm(request.POST, request.FILES)
        form.is_valid()
        if form.cleaned_data['file_kind'] == u'0':
            columns_form = forms.DynamicProfileColumnForm(
                request.POST, prefix='columns')
            columns_form.is_valid()
            columns = [
                col[0] for col in columns_form.cleaned_data.iteritems()
                if col[1]]
            if form.is_valid() and 'file' in request.FILES:
                file_csv = request.FILES['file']
                try:
                    profiles = Profile.objects.import_data(file_csv, columns)
                    status = 'ok'
                    message = _('Imported: %s' % len(profiles))
                except:
                    status = 'error'
                    message = _('Error importing data')
            else:
                form = forms.ProfileUploadForm(request.POST, request.FILES)
        else:
            raise NotImplementedError
    else:
        form = forms.ProfileUploadForm()
        columns_form = forms.DynamicProfileColumnForm(prefix='columns')    

    is_staff = request.GET.get('is_staff', False)
    if nav.is_staff:
        is_staff = is_staff != 'false'
        search_kwargs['is_staff'] = is_staff

    if is_staff is not False and nav.group:
        search_args.append(Q(groups=nav.group))
    
    if nav.group:
         search_args.append(
            Q(groups=nav.group))

    if nav.last_login == 'month':
        search_kwargs['last_login__gte'] = datetime.today() - timedelta(30)

    paginator = nav.get_queryset_with_paginator(
        Profile, reverse('profile:admin:index'),
        search_query=(search_args, search_kwargs),
        obj_per_page=admin_defaults.ADMIN_OBJECTS_PER_PAGE,
    )
    objects_list = paginator.current_page.object_list

    return {
        'nav': nav, 'objects_list': objects_list, 'paginator': paginator,
        'is_staff': is_staff, 'form': form, 'columns_form': columns_form,
        'status': status, 'message': message,}


@is_staff(required_perms=delete_perm(defaults.CUSTOM_USER_MODEL))
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


@is_staff(required_perms=change_perm(defaults.CUSTOM_USER_MODEL))
@ajax_request
def resend_activation(request, profile_id):
    try:
        profile = Profile.objects.get(pk=profile_id)
        if profile.is_active:
            return APIResponseFail(
                messages=[_('Profile is already activated.')])

        profile.generate_activation_key(realhost=request.get_host())
        return APIResponse(messages=[_('Activation key has been sent.')])
    except Profile.DoesNotExist:
        return APIResponseFail(messages=[_('Profile does not exists!')])
    return APIResponse(messages=[_('Do nothing.. Use correct API call')])


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


@is_staff(required_perms='profile')
@render_to('spicy.core.profile/blacklisted_ips.html', use_admin=True)
def blacklisted_ips(request):
    nav = utils.NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(
        BlacklistedIP, reverse('profile:admin:blacklisted-ips'),
        obj_per_page=admin_defaults.ADMIN_OBJECTS_PER_PAGE)
    objects_list = paginator.current_page.object_list

    return {'nav': nav, 'objects_list': objects_list, 'paginator': paginator}


@is_staff(required_perms='profile.delete_blacklistedip')
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
