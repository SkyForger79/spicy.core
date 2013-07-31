from django.conf import settings 

DB_LOGGER_URL = getattr(settings, 'DB_LOGGER_URL', 'pg.example.com')
