from django.core.management.base import NoArgsCommand
from spicy.core.simplepages import utils

class Command(NoArgsCommand):
    help = "Delete expired user profiles from the database"

    def handle_noargs(self, **options):
        result = utils.find_simplepages()
        print len(result['found']), 'pages found,', \
            len(result['existing']), 'existing.'
