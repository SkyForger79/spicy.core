"""
Management utility to create superusers.
"""
import getpass
import os
import re
import sys
from django.contrib.sites.models import Site
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _
from optparse import make_option
from spicy.core.profile import defaults, utils
from spicy.utils.models import get_custom_model_class


Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)


RE_VALID_USERNAME = re.compile('\w+$')
EMAIL_RE = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)  # domain

def is_valid_email(value):
    if not EMAIL_RE.search(value):
        raise exceptions.ValidationError(_('Enter a valid e-mail address.'))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--email', dest='email', default=None,
            help='Specifies the email address for the superuser.'),
        make_option('--noinput', action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind. '    \
                 'You must use --email with --noinput, and '      \
                 'superusers created with --noinput will not be able to log in '  \
                 'until they\'re given a valid password.'),

    )
    help = 'Used to create a superuser.'

    def handle(self, *args, **options):
        email = options.get('email', None)
        interactive = options.get('interactive')
        
        if not interactive:
            if not email:
                raise CommandError("You must use --email")
            try:
                is_valid_email(email)
            except exceptions.ValidationError:
                raise CommandError("Invalid email address.")

        password = ''
        # Try to determine the current system user's username to use as a default.
        try:
            import pwd
            default_username = pwd.getpwuid(os.getuid())[0].replace(' ', '').lower()
        except (ImportError, KeyError):
            # KeyError will be raised by getpwuid() if there is no
            # corresponding entry in the /etc/passwd file (a very restricted
            # chroot environment, for example).
            default_username = ''

        # Determine whether the default username is taken, so we don't display
        # it as an option.
        if default_username:
            try:
                Profile.objects.get(username=default_username)
            except Profile.DoesNotExist:
                pass
            else:
                default_username = ''

        # Prompt for username/email/password. Enclose this whole thing in a
        # try/except to trap for a keyboard interrupt and exit gracefully.
        if interactive:
            try:    
                # Get an email
                while 1:
                    if not email:
                        email = raw_input('E-mail address: ')
                    try:
                        is_valid_email(email)
                    except exceptions.ValidationError:
                        sys.stderr.write("Error: That e-mail address is invalid.\n")
                        email = None
                    else:
                        break
            
                # Get a password
                while 1:
                    if not password:
                        password = getpass.getpass()
                        password2 = getpass.getpass('Password (again): ')
                        if password != password2:
                            sys.stderr.write("Error: Your passwords didn't match.\n")
                            password = None
                            continue
                    if password.strip() == '':
                        sys.stderr.write("Error: Blank passwords aren't allowed.\n")
                        password = None
                        continue
                    break
            except KeyboardInterrupt:
                sys.stderr.write("\nOperation cancelled.\n")
                sys.exit(1)
        
        profile = Profile.objects.create_inactive_user(email, password=password, 
                                            is_staff=True, send_email=False)
        
        profile.sites.add(*Site.objects.all())
        profile.activate()
        profile.is_superuser = True
        profile.save()
        print "Superuser created successfully."
