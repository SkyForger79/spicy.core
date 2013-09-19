from django.contrib.auth.management.commands.changepassword import Command
from django.core.management.base import CommandError

from spicy.utils.models import get_custom_model_class
from spicy.core.profile import defaults

Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)

import getpass


class Command(Command):
    def handle(self, *args, **options):
        if len(args) > 1:
            raise CommandError("need exactly one or zero arguments for email")

        if args:
            email, = args
        else:
            email = getpass.getuser()

        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise CommandError("profile '%s' does not exist" % email)

        print "Changing password for profile '%s'" % profile.email

        MAX_TRIES = 3
        count = 0
        p1, p2 = 1, 2  # To make them initially mismatch.
        while p1 != p2 and count < MAX_TRIES:
            p1 = self._get_pass()
            p2 = self._get_pass("Password (again): ")
            if p1 != p2:
                print "Passwords do not match. Please try again."
                count = count + 1

        if count == MAX_TRIES:
            raise CommandError("Aborting password change for user '%s' after %s attempts" % (email, count))

        profile.set_password(p1)
        profile.save()

        return "Password changed successfully for user '%s'" % profile.email
