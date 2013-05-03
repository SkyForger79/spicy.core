from django.db import models


class ServerLog(models.Model):
    class Meta:
        permissions = (('view_system_info', 'View system info'),)
