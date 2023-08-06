from django.db import models


class Category(models.Model):
    _type = models.IntegerField(max_length=10, default=1)
    title = models.CharField(max_length=100, null=True)
    parent = models.IntegerField(max_length=10, default=1)

    sort = models.AutoField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
