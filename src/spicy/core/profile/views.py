# -*- coding: utf-8 -*-
import random
import string
from uuid import uuid4
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from spicy.utils.printing import print_warning
from spicy.utils.models import get_custom_model_class
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from . import defaults, models, forms
from .models import BlacklistedIP


Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)


def generate_random_password(length=10):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])


@render_to('spicy.core.profile/profile.html')
def profile(request, username):
    user = get_object_or_404(Profile, username=username)
    return dict(user=user)


@login_required
@render_to('spicy.core.profile/edit.html')
def edit(request, username):
    messages = ''
    user = get_object_or_404(Profile, username=username)

    if request.user != user:
        raise PermissionDenied()

    form = forms.PublicProfileForm(instance=user)

    if request.POST:
        form = forms.PublicProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

    return dict(
        user=user,
        form=form,
        messages=messages)


@login_required
@render_to('spicy.core.profile/passwd.html')
def passwd(request, username):
    # Dublicate in the spicy.core.profile.admin
    # TODO: use service
    print_warning('Deprecated method spicy.core.profile.views.passwd')

    message = ''
    user = get_object_or_404(Profile, username=username)

    if request.user != user:
        raise PermissionDenied()

    form = PasswordChangeForm(user)
    if request.POST:
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            message = _('Password has been change successful')

    return dict(user=user, form=form, message=message)


@ajax_request
def check_unic_username(request):
    # Dublicate in the spicy.core.profile.admin
    # TODO: use service
    print_warning(
        'Deprecated method spicy.core.profile.views.check_unic_username')

    mssgs = dict(error='error', success='ok')
    username = request.POST.get('username', None)

    if username is None:
        return dict(result=mssgs['error'])
    try:
        Profile.objects.get(username=username)
    except:
        response_txt = mssgs['success']
    else:
        response_txt = mssgs['error']
    return dict(result=response_txt)


@csrf_protect
@render_to('spicy.core.profile/activate.html')
def activate(request, profile_id, activation_key):
    next_url = request.GET.get('next', '/')
    profile = Profile.objects.activate_user(activation_key)
    return dict(profile=profile, next_url=next_url)


@render_to('spicy.core.profile/user_agreement.html')
def user_agreement(request):
    return dict()


@csrf_protect
@render_to('spicy.core.profile/restore_password.html')
def restorepass(request):
    return api.register['profile'].restore(request)


@login_required
def signout(request):
    redirect_to = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    try:
        del request.session['openid']
    except KeyError:
        pass
    auth_logout(request)
    return HttpResponseRedirect(redirect_to)


@login_required
@render_to('spicy.core.profile/set_email.html')
def set_email(request):

    if request.user.email:
        return {'msg': _('Email address is already set')}
    if request.method == 'POST':
        form = forms.SetEmailForm(request.POST)
        if form.is_valid():
            # Send validation email.
            request.user.email_confirm(form.cleaned_data['email'])
            return {'msg': _('Validation email has been sent')}
    elif all(request.GET.get(key) for key in ('email', 'hash')):
        hash_key = request.GET['hash']
        email = request.GET['email']
        if request.user.get_hash(email) == hash_key:
            request.user.email = email
            request.user.save()
            return HttpResponseRedirect(
                reverse('profile:public:index', args=[request.user.username]))
    else:
        form = forms.SetEmailForm()
    return {'form': form}


@never_cache
@render_to('spicy.core.profile/signin.html')
def signin(request):
    result = api.register['profile'].login(request)
    if result['status'] == 'ok':
        return HttpResponseRedirect(
            result.get('redirect') or user_redirect_uri)
    return result


@never_cache
@render_to('spicy.core.profile/signup.html')
def signup(request):
    result = api.register['profile'].register(request)
    if result['status'] == 'ok':
        return HttpResponseRedirect(
            '%s?next=%s' % (
                reverse('profile:public:success-signup'),
                result['redirect']))
    return result


@render_to('spicy.core.profile/widgets/signin_form.html')
def login_widget(request):
    result = api.register['profile'].login(request)
    if result['status'] == 'ok':
        result['redirect_now'] = True
    return result


@render_to('spicy.core.profile/widgets/signup_form.html')
def registration_widget(request):
    result = api.register['profile'].register(request)
    if result['status'] == 'ok':
        result['redirect_now'] = True
    return result


@render_to('spicy.core.profile/success_signup.html')
def success_signup(request):
    next_url = request.GET.get(REDIRECT_FIELD_NAME, '/')
    email = request.session.get('profile_email', '')
    return dict(next=next_url, email=email)


@render_to('spicy.core.profile/social/signin.html')
def signin_social(request, backend):
    real_ip = request.META.get('REMOTE_ADDR')
    if real_ip and BlacklistedIP.objects.filter(ip=real_ip).exists():
        return HttpResponseRedirect(reverse('profile:public:signup'))

    request.session.set_test_cookie()
    # Set redirect to previous URL unless it's already set in session.
    redirect_to = request.REQUEST.get(
        REDIRECT_FIELD_NAME, request.META.get('HTTP_REFERER', ''))
    if redirect_to and not request.session.get(REDIRECT_FIELD_NAME):
        request.session[REDIRECT_FIELD_NAME] = redirect_to
        request.session['newuser-next'] = redirect_to

    from social_auth import views as sa_views
    return sa_views.auth(request, backend)


@render_to("spicy.core.profile/social/new_user.html")
def new_social_user(request):
    new_user = request.session.get('NEW_USER')
    if not new_user:
        return HttpResponseRedirect(reverse('profile:public:signin'))
    elif not (new_user.is_active and new_user.is_authenticated()):
        new_user.is_active = True
        new_user.save()
        user = auth_login(request, new_user)

    if request.method == 'POST':
        if request.POST.get('signin'):
            # Associate with existing account.
            login_form = forms.LoginForm(
                request, request.POST, prefix='associate')
            update_form = forms.SocialProfileUpdateForm(
                instance=new_user, prefix='newuser')
            if login_form.is_valid():
                old_user = login_form.get_user()
                social_user = new_user.social_auth.get()
                social_user.user = old_user
                social_user.save()
                new_user.delete(trash=False)

                # Make session copy and login.
                session_copy = dict(
                    (k, v) for k, v in request.session.iteritems()
                    if not k.startswith('_'))
                redirect_to = session_copy.pop(REDIRECT_FIELD_NAME, None)
                if not redirect_to:
                    redirect_to = session_copy.pop('newuser-next', None)
                del session_copy['NEW_USER']
                request.session.delete()
                auth_login(request, old_user)

                # Update session from saved copy.
                for k, v in session_copy.iteritems():
                    request.session[k] = v
                request.session[
                    defaults.PASSWORD_HASH_KEY] = old_user.password
                if login_form.cleaned_data['is_remember']:
                    request.session.set_expiry(1209600)
                return HttpResponseRedirect(
                    redirect_to or reverse(
                        'profile:public:index',
                        args=[old_user.username]))
        else:
            login_form = forms.LoginForm(request, prefix='associate')
            update_form = forms.SocialProfileUpdateForm(
                request.POST, instance=new_user, prefix='newuser')

            old_email = new_user.email
            # Django bug - this field would be overridden with form data if
            # we save user used as form instance. So save email in advance.

            if update_form.is_valid():
                email = update_form.cleaned_data['email']
                user = update_form.save(commit=False)
                user.username = update_form.cleaned_data['username']
                # Email address requires validation first, don't save it!
                user.email = old_email
                user.activate()

                #tag, exists = api.register['xtag'].get_or_create_by_term_name(
                #    user.screenname, vocabulary='persons', user=user)
                #tag.save()

                # Login.
                redirect_to = request.session.pop(REDIRECT_FIELD_NAME, None)
                if not redirect_to:
                    redirect_to = request.session.pop('newuser-next', None)

                request.session[
                    defaults.PASSWORD_HASH_KEY] = new_user.password

                if user.email != email:
                    user.email_confirm(email)
                    if not redirect_to:
                        return {'msg': _('Validation email has been sent')}
                return HttpResponseRedirect(
                    redirect_to or reverse(
                        'profile:public:index', args=[user.username]))
    else:
        new_user.sites = Site.objects.all()
        login_form = forms.LoginForm(request, prefix='associate')
        update_form = forms.SocialProfileUpdateForm(
            instance=new_user, prefix='newuser')

    return {
        'login_form': login_form, 'update_form': update_form,
        'next_url': settings.LOGIN_URL}


def sa_get_username(details, user=None, *args, **kwargs):
    """
    Return an username for new user.

    Returns current user username if user was given.
    """
    if user:
        return {'username': user.username}

    from social_auth.backends.pipeline import USERNAME
    if details.get(USERNAME):
        username = details[USERNAME]
    else:
        username = uuid4().get_hex()

    final_username = models.Profile.objects.get_available_username(username)
    return {'username': final_username}


def sa_set_new_user_inactive(
        backend, details, response, uid, username, user=None, *args, **kwargs):
    if user:
        return {'user': user}
    if not username:
        return None

    email = details.get('email')
    user = Profile.objects.create_user(username=username, email=email)
    user.accept_agreement = True
    user.is_active = False
    user.save()
    kwargs['request'].session['NEW_USER'] = user
    return {'user': user, 'is_new': True}
