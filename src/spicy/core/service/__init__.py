__import__('pkg_resources').declare_namespace(__name__)
# XXX #1819
from django.db import connection
from django.core import signals

def close_connection(**kwargs):
    connection.close()
signals.request_started.connect(close_connection)
