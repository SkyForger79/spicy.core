from django.core.management.base import NoArgsCommand

from extprofile.models import Profile

class Command(NoArgsCommand):
    help = "Delete expired user profiles from the database"

    def handle_noargs(self, **options):
        count = Profile.objects.delete_expired_users()
        return '%s profiles has been expired and deleted.'%count
