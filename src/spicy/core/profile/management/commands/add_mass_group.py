"""
Management utility to create superusers.
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

from spicy.core.profile import defaults as pf_defaults
from spicy.utils.models import get_custom_model_class

from optparse import make_option

Profile = get_custom_model_class(pf_defaults.CUSTOM_USER_MODEL)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--logins', dest='logins', default=None,
            help='Specifies the logins file'),
        make_option(
            '--group_id', dest='group_id', default=None,
            help='group_id'),
        make_option(
            '--test', dest='test', default=None,
            help='run test'),
        )
    help = 'Add group for logins from file'

    def handle(self, *args, **options):
        logins = options.get('logins', None)
        group_id = options.get('group_id', None)
        test = options.get('test', None)

        if logins is None or group_id is None:
            raise CommandError("Invalid logins file or group id")

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            print 'cant find group id%'%group_id

        cnt = 0
        print 'Group %s'%group
        logins = open(logins).readlines()         
        for login in logins:
            login = login.strip()
            try:
                profile = Profile.objects.get(username=login)

                if test is not None:
                    profile.activate()
                    profile.is_staff = False
                    if not group in profile.groups.all():
                        profile.groups.add(group)
                    profile.save()
                    cnt += 1
                    
            except Profile.DoesNotExist:
                print 'Cant find login: [%s]'%login

        if test is None:
            print 'Test mode is enabled'
        print 'Group %s'%group
        print "completed for %s"%cnt
