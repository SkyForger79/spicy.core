# -*- coding: utf-8 -*-
import datetime
import re
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as auth_login
from django.contrib.auth import REDIRECT_FIELD_NAME
from spicy.core.profile.views import generate_random_password
from spicy.core.service import api
from spicy.utils import load_module
from spicy.utils.models import get_custom_model_class
from spicy.core.siteskin.decorators import ajax_request, render_to
from . import defaults, models
from .decorators import is_staff
from .forms import LoginForm

Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)

CUSTOM_USER_SIGNUP_FORM = getattr(
    settings, 'CUSTOM_USER_SIGNUP_FORM', 'spicy.core.profile.forms.SignupForm')


class ProfileProvider(api.Provider):
    model = defaults.CUSTOM_PERMISSION_PROVIDER_MODEL

    @ajax_request('/$', is_public=True, use_siteskin=True, use_cache=False)
    def login(self, request):
        result = self.service.login(request)

        status = result['status']
        message = result['message']

        return dict(status=status, message=message)

    @ajax_request('/$', is_public=True, use_siteskin=True, use_cache=False)
    def register(self, request):
        result = self.service.register(request)

        status = result['status']
        message = result['message']

        return dict(status=status, message=message)

    @render_to('profile/social_associations.html', is_public=True,
               url_pattern='/(?P<profile_id>[\d]+)/$', use_siteskin=True)
    def social_associations(self, request, profile_id):
        backends = (
            ('twitter', 'Twitter'),
            ('facebook', 'Facebook'),
            ('linkedin', 'Linkedin'),
            ('google-oauth', 'Google'),
            #('mailru-oauth2', 'Mail.ru'),
            ('odnoklassniki', 'Одноклассники'),
            ('vkontakte-oauth2', 'ВКонтакте'),
            ('vkontakte', 'ВКонтакте'),
            ('yandex', 'Yandex'),
            ('livejournal', 'Livejournal'),
            ('openid', 'OpenID'),
        )
        associated = request.user.social_auth.all().values_list(
            'provider', flat=True)
        return {'backends': backends, 'associated': associated}

    @is_staff()
    @ajax_request('/(?P<consumer_type>\w+)/(?P<consumer_id>\d+)/'
                  '(?P<tab_name>\w*)/?')
    def current_editors(self, request, consumer_type, consumer_id, tab_name):
        cache_key_doc = u':'.join((
            defaults.ACCESS_CACHE_PREFIX, consumer_type, consumer_id))
        if tab_name:
            cache_key_tab = u':'.join((cache_key_doc, tab_name))
        cache_keys = [(cache_key_doc, 'all_tabs')]
        if tab_name:
            cache_keys.append((cache_key_tab, 'current_tab'))

        now = datetime.datetime.now()
        min_time = now - datetime.timedelta(0, defaults.ACCESS_CACHE_PERIOD)

        results = {}
        users_dict = {}
        for cache_key, result_name in cache_keys:
            access_dict = cache.get(cache_key, {})
            new_dict = {}
            current_user_ids = set()
            current_users = []
            for user_id, access_time in access_dict.iteritems():
                if access_time < min_time:
                    continue
                else:
                    current_user_ids.add(user_id)
                    new_dict[user_id] = access_time
            current_user_ids.add(request.user.pk)

            for user_id in current_user_ids:
                if not user_id in users_dict.has_key:
                    profile = Profile.objects.get(pk=user_id)
                    users_dict[user_id] = u'%s &lt;%s&gt;' % (
                        escape(profile), profile.email)
                current_users.append([user_id, users_dict[user_id]])
            current_users.sort()

            new_dict[request.user.pk] = now
            cache.set(cache_key, new_dict, defaults.ACCESS_CACHE_PERIOD)

            results[result_name] = current_users
        if not tab_name:
            results['current_tab'] = []
        return results

    @render_to('', url_pattern='/', is_public=True)
    def get_captcha(self, request):
        from captcha.conf.settings import get_challenge
        from captcha.models import CaptchaStore
        challenge, response = get_challenge()()
        store = CaptchaStore.objects.create(
            challenge=challenge, response=response)
        key = store.hashkey
        return HttpResponse(key)


class ProfileService(api.Interface):
    name = 'profile'
    label = _('Profile provider service')

    statistic_types = (
        ('default', _('New users')),
        ('actived', _('Only activated users')),
        ('commented', _('New users that commented')),
        ('orders', _('New users that did orders')),
        ('orders_and_commented', _('New users that commented and did orders')),
        ('pins_activated', _('Users with pins activated')),
        ('pins_not_activated', _('Users with pins not activated')),
    )

    PROVIDER_TEMPLATES_DIR = 'profile/providers/'

    schema = dict(GENERIC_CONSUMER=ProfileProvider)

    def login(self, request):
        status = 'error'
        message = ''

        redirect = request.GET.get(
            REDIRECT_FIELD_NAME,
            request.session.get(
                REDIRECT_FIELD_NAME,
                request.session.get('newuser-next', '')))
        try:
            del request.session[REDIRECT_FIELD_NAME]
        except KeyError:
            pass

        if request.user.is_authenticated():
            return dict(
                status='ok',
                message=unicode(_('User is signed in already')),
                redirect=redirect)

        can_login = True
        #captcha_required = False
        real_ip = request.META.get('REMOTE_ADDR')

        is_blacklisted = False
        # BBB
        #is_blacklisted = real_ip and models.BlacklistedIP.objects.filter(
        #    ip=real_ip).exists()

        if request.method == 'POST':
            form = LoginForm(data=request.POST)

            # Brute force check.
            username = request.POST.get('username')

            login_check = self.check_login(
                username, real_ip)
            if login_check == defaults.AUTH_DISALLOW:
                can_login = False
            elif login_check == defaults.AUTH_WARN:
                form.make_captcha_visible()
                #captcha_required = True

            if can_login and not is_blacklisted and form.is_valid():

                if not redirect or ' ' in redirect or (
                        '//' in redirect and re.match(r'[^\?]*//', redirect)):
                    redirect = settings.LOGIN_REDIRECT_URL

                if form.cleaned_data['is_remember']:
                    request.session.set_expiry(1209600)

                session_copy = dict(
                    item for item in request.session.iteritems()
                    if not item[0].startswith('_'))
                auth_login(request, form.get_user())

                for key, value in session_copy.iteritems():
                    request.session[key] = value
                request.session[
                    defaults.PASSWORD_HASH_KEY] = request.user.password

                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                status = 'ok'

            else:
                if not form.is_valid():
                    message = form.errors.as_text()
                elif not can_login or is_blacklisted:
                    message = _('Login is disabled or your account is banned.')
        else:
            if redirect:
                request.session[REDIRECT_FIELD_NAME] = redirect
                request.session['newuser-next'] = redirect

            form = LoginForm(request)

        return dict(
            status=status, message=unicode(message), redirect=redirect,
            form=form, REGISTRATION_ENABLED=defaults.REGISTRATION_ENABLED)

    def register(self, request):
        status = 'error'
        message = ''
        real_ip = request.META.get('REMOTE_ADDR')
        is_blacklisted = real_ip and models.BlacklistedIP.objects.filter(
            ip=real_ip).exists()

        if request.method == "POST":
            form = load_module(CUSTOM_USER_SIGNUP_FORM)(request.POST)
            redirect = reverse('profile:public:success-signup')
            if not is_blacklisted and form.is_valid():
                status = 'ok'
                new_profile = form.save(
                    request=request, realhost=request.get_host(),
                    next_url=request.session.get(REDIRECT_FIELD_NAME, '/'))
                request.session['profile_id'] = new_profile.pk
                request.session['profile_email'] = new_profile.email

        else:
            form = load_module(CUSTOM_USER_SIGNUP_FORM)()
            request.session.set_test_cookie()

            # Display the login form and handle the login action.
            redirect = request.REQUEST.get(REDIRECT_FIELD_NAME, '/')
            request.session[REDIRECT_FIELD_NAME] = redirect

        return dict(
            status=status, message=unicode(message), redirect=redirect,
            form=form, REGISTRATION_ENABLED=defaults.REGISTRATION_ENABLED)

    def restore(self, request):
        message = ''
        RestorePasswordForm = load_module(defaults.RESTORE_PASSWORD_FORM)
        if request.method == 'POST':
            form = RestorePasswordForm(request.POST)
            if form.is_valid():
                profile = Profile.objects.get(
                    email__iexact=form.cleaned_data['email'])
                if 'send_pass' in request.POST:
                    newpass = generate_random_password()
                    profile.set_password(newpass)
                    profile.save()
                    profile.email_forgotten_passwd(newpass)

                    return dict(
                        form=form,
                        message=_(
                            'New password has been sent to you email address'))

                elif 'resend_activation' in request.POST:
                    if profile.check_activation():
                        return dict(
                            form=form,
                            message=_('Profile has been already activated'))
                    else:
                        try:
                            profile.generate_activation_key(
                                realhost=request.get_host(),
                                next_url=request.path)

                            message = _(
                                'New activation key has been sent to your '
                                'email address.')
                            return dict(form=form, message=message)

                        except Exception:
                            return dict(
                                form=form,
                                message=_(
                                    'Unable to send activation key, please '
                                    'try again later'))
            else:
                message = form.errors.as_text()
        else:
            if request.user.is_authenticated():
                form = RestorePasswordForm(
                    initial={'email': request.user.email})
            else:
                form = RestorePasswordForm()
        return dict(form=form, message=message)

    def get_profiles(self, **kwargs):
        return Profile.objects.filter(**kwargs)

    def get_profile(self, **kwargs):
        return Profile.objects.get(**kwargs)

    def get_statistic(self, from_date=None, to_date=None, type='default',
                      date_trunc='day', where=None):
        from statistic.utils import make_stats
        if type == 'default':
            return make_stats(
                'date_joined', date_trunc, 'auth_user', from_date, to_date,
                where)
        elif type == 'actived':
            where.append('is_active = true')
            return make_stats(
                'date_joined', date_trunc, 'auth_user', from_date, to_date,
                where)
        elif type == 'commented':
            where.append(
                'exists (select 1 from cm_comment '
                'where cm_comment.author_id = auth_user.id)')
            return make_stats(
                'date_joined', date_trunc, 'auth_user', from_date, to_date,
                where)
        elif type == 'orders':
            where.append(
                'exists (select 1 from sh_order '
                'where sh_order.profile_id = auth_user.id)')
            return make_stats(
                'date_joined', date_trunc, 'auth_user', from_date, to_date,
                where)
        elif type == 'orders_and_commented':
            where.extend([
                'exists (select 1 from cm_comment '
                'where cm_comment.author_id = auth_user.id)',
                'exists (select 1 from sh_order '
                'where sh_order.profile_id = auth_user.id)'])
            return make_stats(
                'date_joined', date_trunc, 'auth_user', from_date, to_date,
                where)
        elif type == 'pins_activated':
            where.append(
                'sh_prepaid_content_provider.is_activated = true')
            return make_stats(
                'sh_prepaid_content_provider.activated_from', date_trunc,
                'auth_user', from_date, to_date, where,
                join=('sh_prepaid_content_provider on '
                      'auth_user.id = sh_prepaid_content_provider.profile_id')
            )
        elif type == 'pins_not_activated':
            where.append('sh_prepaid_content_provider.is_activated = false')
            return make_stats(
                'sh_prepaid_content_provider.activated_from', date_trunc,
                'auth_user', from_date, to_date, where,
                join=('sh_prepaid_content_provider on '
                      'auth_user.id = sh_prepaid_content_provider.profile_id'))

    def check_login(self, username, add_ip=None):
        if not defaults.BRUTEFORCE_CHECK:
            return defaults.AUTH_ALLOW

        logins = cache.get('login-attempts:%s' % username)
        if logins is None:
            logins = []

        result = defaults.AUTH_DISALLOW
        now = datetime.datetime.now()

        # Exclude expired attempts made beford hard limit period.
        hard_time = datetime.datetime.now() - datetime.timedelta(
            defaults.BRUTEFORCE_HARD_PERIOD)
        logins = [login for login in logins if login[0] >= hard_time]
        if add_ip:
            logins.append((now, add_ip))

        if len(logins) < defaults.BRUTEFORCE_HARD_LIMIT:
            # Number of attempts is lower than hard limit.
            soft_time = now - datetime.timedelta(
                defaults.BRUTEFORCE_SOFT_PERIOD)
            soft_cnt = 0
            for time, ip in logins:
                if time > soft_time:
                    soft_cnt += 1
                    if soft_cnt >= defaults.BRUTEFORCE_SOFT_LIMIT:
                        # Numer of attempts is higher than soft limit,
                        # but lower than hard limit.
                        result = defaults.AUTH_WARN
                        break
            else:
                result = defaults.AUTH_ALLOW

        cache.set('login-attempts:%s' % username, logins)
        return result
