# -*- coding: utf-8 -*-
import random
import string
from . import defaults, models
from .forms import PublicProfileForm, RestorePasswordForm
from .forms import LoginForm, SetEmailForm, SocialProfileUpdateForm
from .models import BlacklistedIP
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
from spicy.core.profile.utils import get_concrete_profile
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to, ajax_request
from uuid import uuid4

Profile = get_concrete_profile()


def generate_random_password(length=10):
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])


@render_to('profile/profile.html', use_siteskin=True)
def profile(request, username):
    user = get_object_or_404(Profile, username=username)
    return dict(user=user)

@login_required
@render_to('profile/future_articles.html', use_siteskin=True)
def future_articles(request, username):
    user = get_object_or_404(Profile, username=username)
    if request.user != user:
        raise PermissionDenied()

    return dict(user=user)


@login_required
@render_to('profile/draft.html', use_siteskin=True)
def draft(request, username):
    user = get_object_or_404(Profile, username=username)

    if request.user != user:
        raise PermissionDenied()

    return dict(user=user)


@login_required
@render_to('profile/edit.html', use_siteskin=True)
def edit(request, username):
    # XXX Deephunt code
    messages = ''
    user = get_object_or_404(Profile, username=username)

    if request.user != user:
        raise PermissionDenied()

    from xtag.forms import SportcardFormSet

    forms = SportcardFormSet(instance=user.xtag, prefix='scard')

    if request.POST:
        forms = SportcardFormSet(
            request.POST, instance=user.xtag, prefix='scard')
        if forms.is_valid():
            forms.save()
            forms = SportcardFormSet(instance=user.xtag, prefix='scard')

    return dict(
        user=user,
        forms=forms,
        messages=messages,
        )


@login_required
@render_to('profile/passwd.html', use_siteskin=True)
def passwd(request, username):
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

@login_required
@render_to('profile/settings.html', use_siteskin=True)
def user_settings(request, username):
    user = get_object_or_404(Profile, username=username)

    if request.user != user:
        raise PermissionDenied()

    form = PublicProfileForm(instance=user)

    from xtag.forms import UserTagForm

    xtag_form = UserTagForm(instance=user.xtag)

    if request.POST:
        form = PublicProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()

        xtag_form = UserTagForm(request.POST, instance=user.xtag)
        if xtag_form.is_valid():
            xtag_form.save()

    return dict(form=form, xtag_form=xtag_form, user=user)


@csrf_protect
@login_required
@render_to('profile/profile.html', use_siteskin=True)
def settings_profile(request, profile_id):
    owner = get_object_or_404(Profile, pk=profile_id)

    form = PublicProfileForm(instance=request.user)
    if request.method == 'POST':
        form = PublicProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    return dict(form=form, owner=owner)


@ajax_request
def check_unic_username(request):
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
@render_to('profile/activate.html', use_siteskin=True)
def activate(request, profile_id, activation_key):
    next_url = request.GET.get('next', '/')
    profile = Profile.objects.activate_user(activation_key)
    return dict(profile=profile, next_url=next_url)


@render_to('profile/user_agreement.html', use_siteskin=True)
def user_agreement(request):
    return dict()


@csrf_protect
@render_to('profile/restore.html', use_siteskin=True)
def restorepass(request):
    message = ''
    if request.method == 'POST':
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(email__iexact=form.cleaned_data['email'])

            if request.POST.has_key('send_pass'):
                newpass = generate_random_password()
                profile.set_password(newpass)
                profile.save()
                profile.email_forgotten_passwd(newpass)
                                                
                return dict(
                    form=form, message=_('New password has been sent to you email address'))

            elif request.POST.has_key('resend_activation'):
                if profile.check_activation():
                    return dict(
                        form=form, message= _('Profile has been already activated'))

                else:
                    try:
                        profile.generate_activation_key(
                            realhost=request.get_host(), next_url=request.path)

                        message = _('New activation key has been sent to yout email address.')
                        return dict(form=form, message=message)

                    except Exception:
                        return dict(
                            form=form,
                            message = _('Unable to send activation key, please try again later'))
        else:
            message = form.errors.as_text()
    else:
        if request.user.is_authenticated():
            form = RestorePasswordForm(initial={'email': request.user.email})
        else:
            form = RestorePasswordForm()
    return dict(form=form, message=message)


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
@render_to('profile/set_email.html', use_siteskin=True)
def set_email(request):

    if request.user.email:
        return {'msg': _('Email address is already set')}
    if request.method == 'POST':
        form = SetEmailForm(request.POST)
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
        form = SetEmailForm()
    return {'form': form}


@never_cache
@render_to('profile/signin.html', use_siteskin=True)
def signin(request):
    if request.user.is_authenticated():
        redirect_to = request.REQUEST.get(
            REDIRECT_FIELD_NAME, request.session.get(REDIRECT_FIELD_NAME))

        import types
        if isinstance(defaults.DEFAULT_PROFILE_URL, types.FunctionType):
            user_redirect_uri = defaults.DEFAULT_PROFILE_URL(request.user)
        else:
            user_redirect_uri = defaults.DEFAULT_PROFILE_URL
            
        return HttpResponseRedirect(
            redirect_to or user_redirect_uri)

    result = api.register['profile'].login(request)
    if result['status'] == 'ok':
        return HttpResponseRedirect(
            result.get('redirect') or
            reverse("profile:public:index", args=[request.user.username]))
    return result


@never_cache
@render_to('profile/signup.html', use_siteskin=True)
def signup(request):
    if request.user.is_authenticated():
        redirect_to = request.REQUEST.get(
            REDIRECT_FIELD_NAME, request.session.get(REDIRECT_FIELD_NAME))
        return HttpResponseRedirect(
            redirect_to or defaults.DEFAULT_PROFILE_URL(request.user))

    result = api.register['profile'].register(request)
    if result['status'] == 'ok':
        return HttpResponseRedirect(
            '%s?next=%s' % (
                reverse('profile:public:email-notify'),
                result['redirect']))
    return result


@render_to('profile/login_widget.html', use_siteskin=True)
def login_widget(request):
    if request.user.is_authenticated():
        redirect_to = request.REQUEST.get(
            REDIRECT_FIELD_NAME, request.session.get(REDIRECT_FIELD_NAME))

        return {
            'redirect_now': True,
            'redirect': redirect_to or defaults.DEFAULT_PROFILE_URL(request.user)}

    result = api.register['profile'].login(request)
    if result['status'] == 'ok':
        result['redirect_now'] = True
    return result


@render_to('profile/registration_widget.html', use_siteskin=True)
def registration_widget(request):
    if request.user.is_authenticated():
        redirect_to = request.REQUEST.get(
            REDIRECT_FIELD_NAME, request.session.get(REDIRECT_FIELD_NAME))
        return {
            'redirect_now': True,
            'redirect': redirect_to or defaults.DEFAULT_PROFILE_URL(request.user)}

    result = api.register['profile'].register(request)
    if result['status'] == 'ok':
        result['redirect_now'] = True
    return result


@render_to('profile/email_notify.html', use_siteskin=True)
def email_notify(request):
    next = request.GET.get('next', '/')
    email = request.session.get('profile_email', '')
    return dict(next=next, email=email)


@render_to('profile/signin.html', use_siteskin=True)
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
    return sa_views.auth(request, backend)


@render_to("profile/new_social_user.html", use_siteskin=True)
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
            login_form = LoginForm(request, request.POST, prefix='associate')
            update_form = SocialProfileUpdateForm(
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
            login_form = LoginForm(request, prefix='associate')
            update_form = SocialProfileUpdateForm(
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
        login_form = LoginForm(request, prefix='associate')
        update_form = SocialProfileUpdateForm(
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
