import errno
import random
import smtplib
import socket
import sys
import datetime as dt
from . import cache, defaults
from django.conf import settings
from django.contrib.auth.models import User, UserManager, Group, Permission
from django.contrib.auth.models import AnonymousUser as BasicAnonymousUser
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models, transaction
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.hashcompat import sha_constructor
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.core.management.color import color_style
#from social_auth.signals import pre_update
from spicy.core.service.models import ProviderModel
from spicy.core.siteskin import defaults as sk_defaults

from uuid import uuid4



style = color_style()


class ProfileManager(UserManager):
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
    def create_inactive_user(self, email, password=None, is_staff=False,
                             first_name='', last_name='', username='', 
                             send_email=True, next_url=None, realhost=None):
        now = dt.datetime.now()
        if username == '':
            username = self.get_available_username(email.split('@')[0])
        profile = self.model(
            username=username, email=email, first_name=first_name,
            last_name=last_name, is_staff=is_staff, is_active=False,
            is_superuser=False, last_login=now, date_joined=now)
        if password is None:
            password = self.make_random_password()
        profile.set_password(password)

        profile.generate_activation_key(
            send_email=send_email, password=password, realhost=realhost,
            next_url=next_url)
        return profile

    def get_available_username(self, username):
        from social_auth.backends.pipeline import USERNAME_MAX_LENGTH
        
        uuid_length = getattr(settings, 'SOCIAL_AUTH_UUID_LENGTH', 4)
        username_fixer = getattr(
            settings, 'SOCIAL_AUTH_USERNAME_FIXER',
            lambda u: u)
        
        short_username = username[:USERNAME_MAX_LENGTH - uuid_length]
        final_username = None

        while True:
            final_username = username_fixer(
                username)[:USERNAME_MAX_LENGTH]

            try:
                Profile.objects.get(username=final_username)
            except Profile.DoesNotExist:
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


class ProfileBase(User):
    user_ptr = models.OneToOneField(User, parent_link=True)    
    
    IS_ACTIVATED = 'Already activated'
    activation_key = models.CharField(_('activation key'), max_length=40)

    is_banned = models.BooleanField(_('user is banned'), blank=True, default=False)

    accept_agreement = models.BooleanField(_('Accept user agreement'), blank=True, default=True)
    subscribe_me = models.BooleanField(_('Subscribe me for news update'), blank=True, default=True)    
    
    hide_email = models.BooleanField(_('Hide my email'), default=True)
        
    second_name = models.CharField(
        _('Second name'), max_length=255, blank=True)
    
    phone = models.CharField(_('Phone'), max_length=100, blank=True)
    
    timezone = models.CharField(
        max_length=50, default=settings.TIME_ZONE, blank=True)

    sites = models.ManyToManyField(Site, blank=True)

    objects = ProfileManager()

    class Meta:
        abstract = True
        ordering = ['-id']
        db_table = 'auth_profile'
        permissions = (
            ('view_profile', 'Can view user profiles'),
            ('moderate_profile', 'Can moderate profiles'),
        )
        

    @property
    def screenname(self):
        # Social auth sets a string value to self.fullname, here's a
        # workaround for this shit.
        if callable(self.fullname):
            return self.fullname()
        else:
            return self.fullname

    def fullname(self):
        name =  getattr(self, 'full_name', self.get_full_name())
        if not unicode(name).strip():
            name = self.username
        name = escape(name)
        return name

    __unicode__ = fullname
       
    def activate(self):
        self.is_active = True
        self.activation_key = self.IS_ACTIVATED
        self.save()

    def check_activation(self):
        if (dt.datetime.now() - self.date_joined) < dt.timedelta(days=1):
            return True
        return self.is_active # and (self.activation_key == self.IS_ACTIVATED)

    def generate_activation_key(
        self, send_email=True, password=None, realhost=None, next_url=None):
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
        return self.activation_key == self.IS_ACTIVATED or \
               (self.date_joined + expiration_date <= dt.datetime.now())
    activation_key_expired.boolean = True

    def email_user(self, subject, message, email=None):
        email = email or self.email

        #print '@@SOCIAL@@', [(soc.provider, soc.uid) for soc in self.social_auth.all()]
        
        if not email:
            # No email - do nothing.
            return
        
        try:
            send_mail(subject, message, None, [email])
            return True
        except socket.error, e:
            # TODO: log error
            if e.errno == errno.ECONNREFUSED:
                sys.stderr.write(
                    style.ERROR(
                        'Connection refused, please configure your mail server'
                        'correctly.\n'))
            else:
                sys.stderr.write(
                    style.ERROR(
                        'Can not send mail, error: %s\n'% e))
        except smtplib.SMTPException, e:
            sys.stderr.write(
                style.ERROR(
                    'Can not send mail, SMTP error: %s\n'% e))


    def email_activation_key(self, password, realhost=None, next_url=None):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        context = {
            'expiration_days': defaults.ACCOUNT_ACTIVATION_DAYS, 
            'password': password, 'user_id': self.id, 'user':self, 'site': site,
            'key': self.activation_key, 'email': self.email, 'next_url': next_url,
            'realhost': realhost,}
        subject = render_to_string(sk_defaults.SITESKIN + '/mail/activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(sk_defaults.SITESKIN + '/mail/activation_email.txt', context)
        self.email_user(subject, message)

    def get_hash(self, email=None):
        if email is None:
            email = self.email
        key = ':'.join((str(self.pk), email, settings.SECRET_KEY))
        return sha_constructor(key).hexdigest()

    def email_passwd(self, password):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        context = {'password': password, 'user': self, 'site': site}
        subject = render_to_string(sk_defaults.SITESKIN + '/mail/passwd_email_subj.txt', context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(sk_defaults.SITESKIN + '/mail/passwd_email.txt', context)
        self.email_user(subject, message)

    def email_confirm(self, email):
        site = Site.objects.get_current()
        context = {
            'user': self, 'site': site, 'email': email,
            'hash': self.get_hash(email)}
        subject = ' '.join(
            render_to_string(sk_defaults.SITESKIN + '/mail/set_email_subject.txt', context).splitlines())
        message = render_to_string(sk_defaults.SITESKIN + '/mail/set_email.txt', context)
        self.email_user(subject, message, email=email)                    

    def email_message_notify(self, msg):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        subject = unicode(_('You received a new message from %s'%msg.sender.screenname))

        message = render_to_string(sk_defaults.SITESKIN + '/mail/message_notify_email.txt', 
            dict(msg=msg, user=self, site=site))
        self.email_user(subject, message)

    def email_forgotten_passwd(self, password):
        if not self.email:
            # No email - do nothing.
            return

        site = Site.objects.get_current()
        subject = unicode(_('Restore password for you account on the %s'%site.domain.capitalize()))

        message = render_to_string(sk_defaults.SITESKIN + '/mail/forgotten_passwd_email.txt', 
            dict(password=password, user=self, site=site))
        self.email_user(subject, message)

    def delete(self, *args, **kwargs):
        user_comments = self.comments.all()
        for comment in user_comments:
            comment.delete()
        super(Profile, self).delete(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return 'profile:public:index', (self.username,), {}


class Profile(ProfileBase):
    pass


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
    obj_per_page = sk_defaults.OBJECTS_PER_PAGE

    def fullname(self):
        return _('Anonymous')

    can_edit_tags = False


class StaffAlias(models.Model):
    fullname = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, unique=True)

    class Meta:
        db_table = 'auth_profile_alias'


class ExtProfileProviderModel(ProviderModel):
    class Meta:
        db_table = 'auth_provider'


class BlacklistedIP(models.Model):
    ip = models.IPAddressField(_('IP address'))
    date_banned = models.DateTimeField(_('Date banned'), auto_now_add=True)
    set_by = models.ForeignKey(
        Profile, related_name='in_blacklisted_ips', verbose_name=_('Set by'))
    set_for = models.ForeignKey(
        Profile, null=True, related_name='created_blacklisted_ips',
        verbose_name=_('Set for'))

    class Meta:
        db_table = 'auth_black_ip'
        ordering = 'date_banned',
