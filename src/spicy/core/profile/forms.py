# -*- coding: utf-8 -*-
import re
import datetime as dt
from copy import copy
from captcha.conf.settings import get_challenge, CAPTCHA_FLITE_PATH
from captcha.models import CaptchaStore
from captcha.fields import CaptchaField, CaptchaTextInput, ImproperlyConfigured
from django.conf import settings
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from spicy.core.siteskin.widgets import LabledRegexField, LabledEmailField
from spicy.utils.models import get_custom_model_class
from . import defaults


NAME_RE = re.compile(
    u'^[\\.\\-_a-zA-Z0-9абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    u'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ]+$')


Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)


class CaptchaWithId(CaptchaTextInput):
    """
    Monkey patched captcha input to set image ID.
    """
    def render(self, name, value, attrs=None):
        try:
            reverse('captcha-image', args=('dummy',))
        except Exception:
            raise ImproperlyConfigured(
                'Make sure you\'ve included captcha.urls as explained in the '
                'INSTALLATION section on '
                'http://code.google.com/p/django-simple-captcha/')

        challenge, response = get_challenge()()

        store = CaptchaStore.objects.create(
            challenge=challenge, response=response)
        key = store.hashkey
        value = [key, u'']

        self.image_and_audio = (
            '<img src="%s" id="%s_img" alt="captcha" class="captcha" />' % (
                reverse(
                    'captcha-image', kwargs=dict(key=key)),
                attrs['id']))
        if CAPTCHA_FLITE_PATH:
            self.image_and_audio = '<a href="%s" title="%s">%s</a>' % (
                reverse('captcha-audio', kwargs=dict(key=key)),
                unicode(_('Play captcha as audio file')), self.image_and_audio)

        return super(CaptchaTextInput, self).render(name, value, attrs=attrs)


class AdminPasswdForm(AdminPasswordChangeForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'required password'}))
    password2 = forms.CharField(
        label=_('Password (again)'),
        widget=forms.PasswordInput(attrs={'class': 'required password'}))

    # TODO active fields
    email_new_password = forms.BooleanField(
        label=_('Email new password'), required=False)

    def save(self, *args, **kwargs):
        email_pass = self.cleaned_data['email_new_password']
        passwd = self.cleaned_data['password1']
        user = super(AdminPasswdForm, self).save(*args, **kwargs)
        if email_pass:
            user.email_passwd(passwd)
        return user


class PublicProfileForm(forms.ModelForm):
    username = forms.RegexField(
        label=_('Username'), max_length=30, regex=r'^[\w\-_]+$', required=True)
    first_name = forms.RegexField(
        label=_('First name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    second_name = forms.RegexField(
        label=_('Second name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    last_name = forms.RegexField(
        label=_('Last name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    birthday = forms.DateField(
        label=_('Birthday'), required=False,
        widget=SelectDateWidget(
            years=xrange(
                dt.datetime.now().year - 2, dt.datetime.now().year - 90, -1),
            required=False
        ))

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        try:
            Profile.objects.exclude(pk=self.instance.id).get(
                username=username)
        except Profile.DoesNotExist:
            return username
        else:
            raise forms.ValidationError(_("Username must be unique."))

    class Meta:
        model = Profile
        fields = (
            'username', 'first_name', 'last_name', 'second_name',
            'subscribe_me', 'birthday')
        widgets = {'preview': forms.widgets.HiddenInput()}


class ProfileForm(forms.ModelForm):
    username = forms.RegexField(
        label=_('Username'), max_length=30, regex=r'^[\w\-_]+$',
        help_text=_(
            "Required. 30 characters or fewer. Alphanumeric characters only "
            "(letters, digits and underscores)."),
        error_message=_(
            "This value must contain only letters, numbers and underscores."))
    first_name = forms.RegexField(
        label=_('First name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    second_name = forms.RegexField(
        label=_('Second name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    last_name = forms.RegexField(
        label=_('Last name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    groups = forms.ModelMultipleChoiceField(
        label=_('Groups'), required=False,
        widget=widgets.FilteredSelectMultiple(_("Groups"), is_stacked=False),
        queryset=Group.objects.all())
    sites = forms.ModelMultipleChoiceField(
        label=_('Sites'), required=False,
        widget=forms.SelectMultiple(
            attrs={'class': 'SelectMultiple nosearch'}),
        queryset=Site.objects.all())
    user_permissions = forms.ModelMultipleChoiceField(
        label=_('Permissions'), required=False,
        widget=widgets.FilteredSelectMultiple(
            _("Permissions"), is_stacked=False),
        queryset=Permission.objects.all())

    if 'spicy.crm' in settings.INSTALLED_APPS:
        sms_notification = forms.BooleanField(_('SMS notifications'))
        skype = forms.RegexField(
            label=_('Skype'), max_length=40, regex=r'^[\w\-_]+$')
        inner_phone = forms.CharField(_('Inner phone'))


    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(*args, **kwargs)
        if self.cleaned_data['is_active']:
            profile.activate()

    def __init__(self, *args, **kwargs):
        profile = super(ProfileForm, self).__init__(*args, **kwargs)
        if 'spicy.crm' in settings.INSTALLED_APPS:
            self._meta.fields.extend(
                ['skype', 'sms_notification', 'inner_phone'])

    class Meta:
        model = Profile
        fields = [
            'username', 'first_name', 'second_name', 'last_name', 'email',
            'groups', 'user_permissions', 'sites', 'is_staff', 'is_active',
            'is_banned', 'accept_agreement', 'is_superuser', 'subscribe_me',
            'hide_email', 'phone', 'timezone', 'google_profile_id']

class ModerateProfileForm(forms.ModelForm):
    username = forms.RegexField(
        label=_('Username'), max_length=30, regex=r'^[\w\-_]+$',
        help_text=_(
            "Required. 30 characters or fewer. Alphanumeric characters only "
            "(letters, digits and underscores)."),
        error_message=_(
            "This value must contain only letters, numbers and underscores."))
    first_name = forms.RegexField(
        label=_('First name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    second_name = forms.RegexField(
        label=_('Second name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)
    last_name = forms.RegexField(
        label=_('Last name'), max_length=30, regex=NAME_RE,
        error_message=_(
            "This value must contain only russian or english letters, numbers "
            "and underscores."),
        required=False)

    class Meta:
        model = Profile
        fields = (
            'username', 'first_name', 'second_name', 'last_name', 'email',
            'is_active', 'is_banned',
            'accept_agreement')


class ValidateEmailMixin:
    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                Profile.objects.get(email__iexact=email)
            except Profile.DoesNotExist:
                return email
            except Profile.MultipleObjectsReturned:
                pass
            raise forms.ValidationError(
                _(u'This address already belongs to other user'))
                # + ' <a href="%s">%s</a>&nbsp;<a href="%s">%s</a>' % (reverse('profile:public:signin'), _(u'Authorization'), reverse('profile:public:restorepass'),  _(u'Restore password')),code='alreadyused')
        elif self.fields['email'].required:
            raise forms.ValidationError(_(u'This field is required'))
        return email


class RestorePasswordForm(forms.Form):
    if defaults.USE_CAPTCHA:
        captcha = CaptchaField(widget=CaptchaWithId)

    email = LabledEmailField(label=_('Registered email'), required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                Profile.objects.get(email__iexact=email)
            except Profile.DoesNotExist:
                raise forms.ValidationError(
                    _(u'There is no user with this email'))
        else:
            raise forms.ValidationError(_(u'This field is required'))
        return email


class SetEmailForm(forms.Form):
    if defaults.USE_CAPTCHA:
        captcha = CaptchaField(widget=CaptchaWithId)

    email = forms.EmailField(_('Email'), required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            try:
                if Profile.objects.filter(email__iexact=email).count():
                    raise forms.ValidationError(
                        _(u'This address is already used'))
            except Profile.DoesNotExist:
                return email
        else:
            raise forms.ValidationError(_(u'This field is required'))
        return email


class SignupForm(forms.Form, ValidateEmailMixin):
    if defaults.USE_CAPTCHA:
        captcha = CaptchaField(widget=CaptchaWithId)

    email = forms.EmailField(label=_('Email'), required=True, initial='')

    password = forms.CharField(label=_('Password'),
        widget=forms.PasswordInput(), min_length=6, required=False)
    password2 = forms.CharField(label=_('Password (again)'),
        widget=forms.PasswordInput(), min_length=6, required=False)

    subscribe_me = forms.BooleanField(
        label=_('I want to subscribe for the news digest'), initial=True,
        required=False)
    accept_agreement = forms.BooleanField(
        label=_('I read & accept user agreement'), initial=True, required=True)

    def clean_accept_agreement(self):
        accept = self.cleaned_data.get('accept_agreement')
        if not accept:
            raise forms.ValidationError(
                _("Please, accept the agreement to continue."))
        return accept

    def clean_password2(self):
        value = self.cleaned_data['password2']
        if self.cleaned_data.get('password') != value:
            raise forms.ValidationError(
                _('Password confirmation doesn\'t match'))
        return value

    @transaction.commit_manually
    def save(self, request=None, realhost=None, next_url=None):
        try:
            data = self.cleaned_data.copy()
            email = data.pop('email')

            data.pop('password')
            password = data.pop('password2')

            profile = Profile.objects.create_inactive_user(
                email, password=password,
                next_url=next_url,
                realhost=realhost,
                **data)

            profile.sites.add(*Site.objects.all())
            profile.save()

            if 'mediacenter' in settings.INSTALLED_APPS:
                from mediacenter.models import Library
                # add medialibrary for the profile userpics
                library = Library.objects.create(
                    title="Userpics for %s" % profile.screenname,
                    profile=profile, slug='_userpics_%s' % profile.username)
                library.profile = profile
                library.save()

        except Exception, error_msg:
            transaction.rollback()
            raise Exception(error_msg)

        transaction.commit()
        return profile


class CreateProfileForm(ProfileForm, ValidateEmailMixin):
    email = forms.EmailField(_('Email'), required=True)
    password1 = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(
        label=_('Password (again)'), widget=forms.PasswordInput(),
        required=False)
    groups = forms.ModelMultipleChoiceField(
        label=_('Groups'), required=False,
        widget=forms.SelectMultiple(attrs={'class': 'SelectMultiple'}),
        queryset=Group.objects.all())
    sites = forms.ModelMultipleChoiceField(
        label=_('Sites'), required=False,
        initial=lambda: [Site.objects.get_current()],
        widget=forms.SelectMultiple(
            attrs={'class': 'SelectMultiple nosearch '}),
        queryset=Site.objects.all())

    class Meta:
        model = Profile
        fields = (
            'username', 'first_name', 'second_name', 'last_name', 'email',
            'groups', 'sites', 'is_staff', 'is_superuser', 'is_active',
            'is_banned', 'user_permissions', 'phone', 'timezone',
            'hide_email', 'subscribe_me', 'accept_agreement',
            'google_profile_id')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Username must be unique."))
        else:
            return username

    def clean_password1(self):
        return self.cleaned_data.get('password1', '').strip()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '').strip()
        password2 = self.cleaned_data.get('password2', '').strip()
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    _("The two password fields didn't match."))
            return password2
        return

    @transaction.commit_on_success
    def save(self, realhost=None):
        email = self.cleaned_data['email']
        data = self.cleaned_data.copy()
        data.pop('email')

        data.pop('password1')
        sites = data.pop('sites')
        groups = data.pop('groups')
        user_permissions = data.pop('user_permissions')

        password = data.pop('password2')

        profile = Profile.objects.create_inactive_user(
            self.cleaned_data['email'], password=password, realhost=realhost,
            **data)

        profile.sites.add(*sites)
        profile.groups.add(*groups)
        profile.user_permissions.add(*user_permissions)

        profile.save()
        return profile


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        label=_('Permissions'), required=False,
        widget=forms.SelectMultiple(attrs={'class': 'SelectMultiple'}),
        queryset=Permission.objects.select_related('content_type'))

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        #widgets = {
        #    'permissions': forms.SelectMultiple(
        #        attrs={'class': 'SelectMultiple'})}


GroupFormSet = forms.models.modelformset_factory(
    Group, form=GroupForm, extra=0)


class LoginForm(AuthenticationForm):
    username = LabledRegexField(
        label=_('Username or email'), max_length=30, regex=r'^[\w\-_\.@]+$',
        required=True)

    is_remember = forms.BooleanField(initial=True, required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        user = None
        try:
            if '@' in username:
                user = Profile.objects.get(email=username)
            else:
                user = Profile.objects.get(username=username)
        except:
            pass
        if user and user.is_banned:
            raise forms.ValidationError(_("User was banned"))
        elif user and not user.check_activation():
            raise forms.ValidationError(_("User not activated"))

        return username

    def make_captcha_visible(self):
        captcha_field = CaptchaField(initial=[u'', u''], required=True)
        self.fields['captcha'] = captcha_field


class SocialProfileUpdateForm(forms.ModelForm):
    email = LabledEmailField(label=_('Email'), required=True)
    username = LabledRegexField(
        label=_('Username'), max_length=30, regex=r'^[\w\-_]+$', required=True)
    accept_agreement = forms.BooleanField(initial=True, required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        if Profile.objects.filter(username=username).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError(_('Username must be unique'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Profile.objects.filter(email=email).exclude(
                pk=self.instance.pk).exists():
            raise forms.ValidationError(
                _(u'This address already belongs to other user'))
        return email

    class Meta:
        model = Profile
        fields = 'username', 'email', 'accept_agreement'


class AcceptUserAgreementForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['accept_agreement']


class HiddenCaptchaWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = forms.HiddenInput, forms.HiddenInput
        super(HiddenCaptchaWidget, self).__init__(widgets, attrs)


class SigninForm(AuthenticationForm):
    is_registration = forms.ChoiceField(
        choices=((0, False), (1, True)), widget=forms.HiddenInput)
    username = forms.RegexField(
        label=_('User name'), max_length=30, regex=r'^[\w\-_\.]+$')
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, required=False)
    if defaults.USE_CAPTCHA:
        captcha = CaptchaField(
            required=False, initial=[u'', u''], widget=CaptchaWithId)
    password1 = forms.CharField(
        label=_('Password'), required=False, widget=forms.PasswordInput())
    password2 = forms.CharField(
        label=_('Password (again)'), required=False,
        widget=forms.PasswordInput())
    email = forms.EmailField(_('Email'), required=False)
    is_remember = forms.BooleanField(initial=True, required=False)

    strict = False

    def __init__(self, *args, **kwargs):
        # Path request=None to auth form or it eats our data!
        super(SigninForm, self).__init__(None, *args, **kwargs)

        # We inherit username and password from AuthenticationForm,
        # but we actually want is_registration to be first field to clean.
        # So we have to re-add some fields.
        for fieldname in ('username', 'password', 'email'):
            field = self.fields[fieldname]
            del self.fields[fieldname]
            self.fields[fieldname] = field

        if self.is_bound:
            fields = copy(self.fields)

            auth_fields = 'password',
            reg_fields = 'captcha', 'email', 'password1', 'password2'

            is_registration = self.data.get('%s-is_registration' % self.prefix)
            required = reg_fields if is_registration == '1' else auth_fields

            for field in required:
                self.fields[field].required = True

            self.fields = fields

    def clean_is_registration(self):
        return int(self.cleaned_data.get('is_registration', 0))

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        is_registration = self.cleaned_data['is_registration']
        if self.strict and is_registration == 1:
            try:
                Profile.objects.get(username=username)
                raise forms.ValidationError(_("Username must be unique."))
            except Profile.DoesNotExist:
                pass
        return username

    def clean_password(self):
        if self.cleaned_data['is_registration']:
            return ''
        else:
            return self.cleaned_data.get('password', '').strip()

    def clean_password2(self):
        if self.cleaned_data['is_registration']:
            password1 = self.cleaned_data.get('password1', '').strip()
            password2 = self.cleaned_data.get('password2', '').strip()
            if password1 and password2:
                if password1 != password2:
                    raise forms.ValidationError(
                        _("The two password fields didn't match."))
                return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data.get('username')
        if self.strict and self.cleaned_data['is_registration']:
            if not username:
                return
            try:
                user = Profile.objects.get(email=email)
                if not (
                        user.check_password(self.cleaned_data['password2'])
                        and user.username == username):
                    # Raise ValidationError unless it looks like wizard's
                    # resubmit.
                    raise forms.ValidationError(
                        _(u'This address already belongs to other user'))
            except Profile.DoesNotExist:
                pass
        return email

    def clean(self):
        if not self.cleaned_data['is_registration']:
            super(SigninForm, self).clean()

        return self.cleaned_data


class ProfileFiltersForm(forms.Form):
    group = forms.ModelChoiceField(
        label=_('Group'), queryset=Group.objects.all(), required=False)
    group.widget.attrs['class'] = 'uniform'
    search_text = forms.CharField(max_length=100, required=False)


class ProfileUploadForm(forms.Form):
    file = forms.FileField(label=_('CVS file'), required=False)
    file_kind = forms.ChoiceField(
        label=_('File type'), widget=forms.RadioSelect,
        choices=(
            (u'0', _('Profiles data')),  # (u'1', _('Images'))
        ),
        initial=u'0'
    )
    search_text = forms.CharField(label=_('Search'), required=False)

DynamicProfileColumnForm = type(
    'DynamicProfileColumnForm', (forms.Form,),
    dict(
        (field,
         forms.BooleanField(
             initial=True, label=Profile.get_field_label(field), required=False))
        for field in Profile.get_exported_fields()
    ))
