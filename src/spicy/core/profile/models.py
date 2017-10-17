import xlrd
import xlwt
import errno
import random
import smtplib
import socket
import datetime as dt
from StringIO import StringIO
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User, UserManager, Group, Permission
from django.contrib.auth.models import AnonymousUser as BasicAnonymousUser
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management.color import color_style
from django.db import models, transaction
from django.db.models import FieldDoesNotExist
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor
from django.utils.html import escape
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives

from spicy.core.service.models import ProviderModel
from spicy.utils.printing import print_error
from . import cache, defaults, signals


style = color_style()


class ProfileQuerySet(QuerySet):

    def export_data(self, columns):
        result = StringIO()
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Profile')

        fields = []
        fields.insert(0, ('id', ugettext('Identifier')))
        for field in columns:
            label = self.model.get_field_label(field)
            fields.append((field, label))

        for i, (field, title) in enumerate(fields):
            sheet.write(0, i, field)
            sheet.write(1, i, title)
            for j, item in enumerate(self):
                if field == 'subscribe_me':
                    if getattr(item, field) == 1:
                        sheet.write(j + 2, i, '+')
                    else:
                        sheet.write(j + 2, i, '-')
                else:
                    sheet.write(j + 2, i, getattr(item, field))

        workbook.save(result)
        result.seek(0)
        return result


class ProfileManager(UserManager):
    def get_query_set(self):
        return ProfileQuerySet(self.model, using=self._db)

    def import_data(self, src, fields):
        fields.insert(0, 'id')
        workbook = xlrd.open_workbook(file_contents=src.read())
        sheet = workbook.sheet_by_index(0)
        import_fields = {}
        for i in xrange(sheet.ncols):
            field_name = sheet.cell_value(0, i)
            if field_name in fields:
                import_fields[field_name] = i
        id_pos = import_fields['email']
        del import_fields['email']
        del import_fields['id']
        ids = []
        for i in xrange(2, sheet.nrows):
            email = sheet.cell_value(i, id_pos)
            
            if email:
                try:
                    profile = self.model.objects.get(email=email)
                    _create = False
                except:
                    _create = True
            else:
                _create = True
            prof = {}
            for field, pos in import_fields.iteritems():
#               if sheet.cell_type(i, pos) != xlrd.XL_CELL_EMPTY:
                if not _create and field not in [
                    'username', 'password']:
                    setattr(profile, field, sheet.cell_value(i, pos))
                elif _create:
                    prof.update({field: sheet.cell_value(i, pos)})
            if _create and prof:
                try:
                    profile = self.model.objects.create_inactive_user(
                        email, prof['password'],
                        first_name=prof['first_name'],
                        last_name=prof['last_name'],
                        phone=prof['phone'])
                    ids.append(profile.pk)
                except:
                    pass
            else:
                profile.save()
                ids.append(profile.pk)
        return self.model.objects.filter(pk__in=ids)

    def make_random_password(self, length=10,
        allowed_chars=defaults.ACCOUNT_ALLOWED_CHARS):
            return get_random_string(length, allowed_chars)

    def activate_user(self, activation_key):
        if defaults.SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
                if not profile.activation_key_expired():
                    profile.activate()
                return profile
            except self.model.DoesNotExist:
                pass

    @transaction.commit_on_success
    def create_inactive_user(
            self, email, password=None, send_email=True, next_url=None,
            realhost=None, **kwargs):
        now = dt.datetime.now()
        email = email.lower()
        if not 'username' in kwargs.keys():
            username = self.get_available_username(email.split('@')[0])
        else:
            username = kwargs.pop('username')

        if realhost is None:
            site = Site.objects.get_current()
            realhost = site.domain

        try:
            profile = self.get(email=email)
        except self.model.DoesNotExist:
            is_active = kwargs.pop('is_active', False)

            profile = self.model(
                username=username, is_active=is_active,
                email=email, last_login=now, date_joined=now, **kwargs)

            profile.save()
            signals.create_profile.send(
                sender=self.model, profile=profile)

            if password in (None, '', ' '):
                password = self.make_random_password()
            profile.set_password(password)

            if defaults.MANUAL_ACTIVATION:
                self.model.email_hello(profile, password=password)
                profile.is_banned = defaults.MANUAL_ACTIVATION
                profile.activate()

                if 'is_banned' in kwargs.keys():
                    profile.is_banned = kwargs.pop('is_banned')

                profile.save()

            else:
                profile.generate_activation_key(
                    send_email=send_email, password=password,
                    realhost=realhost, next_url=next_url)
                
            if defaults.NOTIFY_MANAGERS:
                self.model.notify_managers(profile)

        return profile

    def get_available_username(self, username):
        uuid_length = getattr(settings, 'SOCIAL_AUTH_UUID_LENGTH', 4)
        username_fixer = getattr(
            settings, 'SOCIAL_AUTH_USERNAME_FIXER',
            lambda u: u)

        short_username = username[:defaults.USERNAME_MAX_LENGTH - uuid_length]
        final_username = None

        while True:
            final_username = username_fixer(
                username)[:defaults.USERNAME_MAX_LENGTH]

            try:
                User.objects.get(username=final_username)
            except User.DoesNotExist:
                break
            else:
                # User with same username already exists, generate a unique
                # username for current user using username as base but adding
                # a unique hash at the end. Original username is cut to avoid
                # the field max_length.
                username = short_username + uuid4().get_hex()[:uuid_length]
        return final_username

    def delete_expired_users(self):
        raise NotImplementedError
        # # XXX: antisvin 2011-02-24: This would delete shop orders from
        # express registration. Fix foreign keys to Profile or use trash app
        # before deleting expirted users.

        count = 0
        for profile in self.all():
            if profile.activation_key_expired():
                if not profile.is_active:
                    profile.delete()
                    count += 1
        return count


class AbstractProfile(User):
    IS_ACTIVATED = 'Already activated'

    user_ptr = models.OneToOneField(User, parent_link=True)
    activation_key = models.CharField(_('activation key'), max_length=40)
    is_banned = models.BooleanField(
        _('user is banned'), blank=True, default=defaults.MANUAL_ACTIVATION)
    accept_agreement = models.BooleanField(
        _('Accept user agreement'), blank=True, default=True)
    subscribe_me = models.BooleanField(
        _('Subscribe me for news update'), blank=True, default=True)
    hide_email = models.BooleanField(_('Hide my email'), default=True)
    second_name = models.CharField(
        _('Second name'), max_length=255, blank=True)
    phone = models.CharField(_('Phone'), max_length=100, blank=True)
    timezone = models.CharField(
        max_length=50, default=settings.TIME_ZONE, blank=True)
    google_profile_id = models.CharField(
        _('Google profile ID'), max_length=100, blank=True,
        help_text=_(
            'Visit http://profiles.google.com/me to find out ID from redirect '
            'URL'))
    sites = models.ManyToManyField(Site, blank=True)

    objects = ProfileManager()
    on_site = CurrentSiteManager(field_name='sites')

    class Meta:
        abstract = True
        ordering = ['-date_joined', '-id']
        permissions = (
            ('view_profile', 'Can view user profiles'),
            ('moderate_profile', 'Can moderate profiles'),
        )

    def save(self, *args, **kwargs):
        is_old = bool(self.id or False)
        if is_old:
            old = self.__class__.objects.get(pk=self.pk)

        result = super(AbstractProfile, self).save(*args, **kwargs)
        if is_old:
            if old.is_banned != self.is_banned:
                self.email_banned()

        elif not self.sites.all():
            self.sites = [Site.objects.get_current()]

        return result

    @classmethod
    def get_field_label(cls, field):
        try:
            label = cls._meta.get_field_by_name(field)[0].verbose_name
        except FieldDoesNotExist:
            try:
                label = getattr(cls, field, ).__doc__
            except AttributeError:
                if field.endswith('_id'):
                    label = getattr(cls, field[:-3]).field.verbose_name
                else:
                    raise
        return unicode(label)

    # XXX deprecated
    @classmethod
    def get_exported_fields(cls):
        return [
            'username', 'email', 'password', 'first_name',
            'second_name', 'last_name', 'phone', 'subscribe_me']


    @property
    def screenname(self):
        # Social auth sets a string value to self.fullname, here's a
        # workaround for this shit.
        if hasattr(self, 'fullname'):
            return self.fullname
        return self.get_fullname()

    def get_fullname(self):
        name = self.first_name + ' ' + self.last_name
        if not name.strip():
            name = self.username
        name = escape(name)
        return name

    def __unicode__(self):
        return self.screenname

    def activate(self):
        self.is_active = True
        self.activation_key = self.IS_ACTIVATED
        self.save()

    def check_activation(self):
        if (dt.datetime.now() - self.date_joined) < dt.timedelta(days=1):
            return True
        return self.is_active  # and (self.activation_key == self.IS_ACTIVATED)

    def generate_activation_key(
            self, send_email=True, password=None, realhost=None,
            next_url=None):
        if next_url is None:
            next_url = settings.LOGIN_URL
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = smart_str(self.username)
        self.activation_key = sha_constructor(salt + username).hexdigest()
        self.date_joined = dt.datetime.now()
        self.save()
        if send_email:
            self.email_activation_key(
                password, realhost, next_url=next_url)

    def activation_key_expired(self):
        expiration_date = dt.timedelta(
            days=int(defaults.ACCOUNT_ACTIVATION_DAYS))
        return self.activation_key == self.IS_ACTIVATED or (
            self.date_joined + expiration_date <= dt.datetime.now())
    activation_key_expired.boolean = True

    def get_hash(self, email=None):
        if email is None:
            email = self.email
        key = ':'.join((str(self.pk), email, settings.SECRET_KEY))
        return sha_constructor(key).hexdigest()

    def email_user(self, subject, message, email=None, html_body=None):
        email = email or self.email

        if not email:
            # No email - do nothing.
            return

        try:
            mail = EmailMultiAlternatives(subject=subject.strip('\n'), body=message,
                from_email=None, to=[email], headers={'format': 'flowed'})
            if html_body:
                mail.attach_alternative(html_body, 'text/html')
            mail.send()
            return True
        except socket.error, e:
            # TODO: log error
            if e.errno == errno.ECONNREFUSED:
                print_error(
                    'Connection refused, please configure your mail server '
                    'correctly.\n')
            else:
                print_error('Can not send mail, error: {}\n'.format(e))
        except smtplib.SMTPException, e:
            print_error('Can not send mail, SMTP error: {}\n'.format(e))

    def email_hello(
            self, password='not-activated', realhost=None, next_url=None):
        site = Site.objects.get_current()
        context = {
            'expiration_days': defaults.ACCOUNT_ACTIVATION_DAYS,
            'user_id': self.id, 'user': self, 'site': site,
            'password': password, 'key': self.activation_key,
            'email': self.email, 'next_url': next_url,
            'realhost': realhost}
        subject = render_to_string(
            'spicy.core.profile/mail/hello_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/hello_email.txt', context)
        
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/hello_email.html', context)
            self.email_user(subject, message, html_body=html_body)
        else:
            self.email_user(subject, message)

    def email_banned(self):
        site = Site.objects.get_current()
        context = {'user': self, 'site': site}

        subject = render_to_string(
            'spicy.core.profile/mail/banned_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/banned_email.txt', context)
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/banned_email.html', context)
            self.email_user(subject, message, html_body=html_body)
        else:
            self.email_user(subject, message)

    def notify_managers(self, user_password=None):
        context = {
            'user': self, 'site': Site.objects.get_current(), 'user_password': user_password}
        subject = render_to_string(
            'spicy.core.profile/mail/notify_managers_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/notify_managers_email.txt', context)
        try:
            send_mail(
                subject.strip('\n'), message, None,
                [admin_email for admin_name, admin_email in settings.ADMINS])
        except Exception, e:
            print_error(
                'Can not send registration notify, error: {}\n'.format(e))

    def email_activation_key(self, password, realhost=None, next_url=None):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        context = {
            'expiration_days': defaults.ACCOUNT_ACTIVATION_DAYS,
            'password': password, 'user_id': self.id, 'user': self,
            'site': site, 'key': self.activation_key, 'email': self.email,
            'next_url': next_url, 'realhost': realhost}
        subject = render_to_string(
            'spicy.core.profile/mail/activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/activation_email.txt', context)
        
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/activation_email.html', context)
            self.email_user(subject, message, html_body=html_body)
        else:
            self.email_user(subject, message)

    def email_passwd(self, password):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        context = {'password': password, 'user': self, 'site': site}
        subject = render_to_string(
            'spicy.core.profile/mail/passwd_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/passwd_email.txt', context)
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/passwd_email.html', context)
            self.email_user(subject, message, html_body=html_body)
        else:
            self.email_user(subject, message)

    def email_confirm(self, email):
        site = Site.objects.get_current()
        context = {
            'user': self, 'site': site, 'email': email,
            'hash': self.get_hash(email)}
        subject = ' '.join(
            render_to_string(
                'spicy.core.profile/mail/set_email_subject.txt', context
            ).splitlines())
        message = render_to_string(
            'spicy.core.profile/mail/set_email_email.txt', context)
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/set_email_email.html', context)
            self.email_user(subject, message, email=email, html_body=html_body)
        else:
            self.email_user(subject, message, email=email)

    def email_message_notify(self, msg):
        # !!! deprecated method use spicy.messages app
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        subject = unicode(_(
            'You received a new message from %s') % msg.sender.screenname)

        message = render_to_string(
            'spicy.core.profile/mail/message_notify_email.txt',
            dict(msg=msg, user=self, site=site))
        self.email_user(subject, message)

    def email_forgotten_passwd(self, password):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        context = dict(password=password, user=self, site=site)
        subject = render_to_string(
            'spicy.core.profile/mail/forgotten_password_subject.txt', context)
        message = render_to_string(
            'spicy.core.profile/mail/forgotten_password_email.txt', context)
        if defaults.USE_HTML_EMAIL:
            html_body = render_to_string(
                'spicy.core.profile/mail/forgotten_password_email.html', context)
            self.email_user(subject, message, html_body=html_body)
        else:
            self.email_user(subject, message)

    @models.permalink
    def get_absolute_url(self):
        return 'profile:public:index', (self.username,), {}


    # Signals for permission cache invalidation.
models.signals.m2m_changed.connect(
    cache.m2m_changed_permission, sender=User.user_permissions.through)
models.signals.m2m_changed.connect(
    cache.m2m_changed_permission, sender=Group.permissions.through)
models.signals.post_save.connect(cache.post_save_permission, sender=Permission)
models.signals.post_delete.connect(
    cache.post_delete_permission, sender=Permission)
#pre_update.connect(listeners.update_user_details)


class AnonymousUser(BasicAnonymousUser):
    timezone = settings.TIME_ZONE
    theme = 'default'
    obj_per_page = 20

    def fullname(self):
        return _('Anonymous')

    can_edit_tags = False


class PermissionProviderModel(ProviderModel):
    profile = models.ForeignKey(
        defaults.CUSTOM_USER_MODEL, null=False, blank=False)
    role = models.ForeignKey(
        defaults.CUSTOM_ROLE_MODEL, null=False, blank=False)

    class Meta:
        db_table = 'auth_permission_provider'
        unique_together = 'profile', 'consumer_id', 'consumer_type'


class BlacklistedIP(models.Model):
    ip = models.IPAddressField(_('IP address'))
    date_banned = models.DateTimeField(_('Date banned'), auto_now_add=True)
    set_by = models.ForeignKey(
        User, related_name='in_blacklisted_ips', verbose_name=_('Set by'))
    set_for = models.ForeignKey(
        User, null=True, related_name='created_blacklisted_ips',
        verbose_name=_('Set for'))

    class Meta:
        db_table = 'auth_black_ip'
        ordering = 'date_banned',


# This shit doesn't belong here
class TestProfile(AbstractProfile):

    class Meta:
        abstract = False
        db_table = 'test_profile'
        ordering = '-is_staff', '-id'
