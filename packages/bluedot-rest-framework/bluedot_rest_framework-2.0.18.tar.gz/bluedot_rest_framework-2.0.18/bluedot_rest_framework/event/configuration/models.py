from django.db import models


class AbstractEventConfiguration(models.Model):

    event_id = models.IntegerField()
    value = models.JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventConfiguration(AbstractEventConfiguration):

    class Meta:
        db_table = 'event_configuration'
