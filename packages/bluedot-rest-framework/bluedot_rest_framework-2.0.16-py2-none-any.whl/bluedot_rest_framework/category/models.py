from django.db import models


class AbstractCategory(models.Model):
    category_type = models.IntegerField(default=1)
    title = models.CharField(max_length=100, null=True)
    parent = models.IntegerField(default=0)

    sort = models.IntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(AbstractCategory):
    class Meta:
        db_table = 'category'
