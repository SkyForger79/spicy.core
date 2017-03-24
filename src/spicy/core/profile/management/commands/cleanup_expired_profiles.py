from django.core.management.base import NoArgsCommand
from spicy.utils.models import get_custom_model_class

Profile = get_custom_model_class(defaults.CUSTOM_USER_MODEL)

class Command(NoArgsCommand):
    help = "Delete expired user profiles from the database"

    def handle_noargs(self, **options):
        count = Profile.objects.delete_expired_users()
        return '%s profiles has been expired and deleted.'%count
