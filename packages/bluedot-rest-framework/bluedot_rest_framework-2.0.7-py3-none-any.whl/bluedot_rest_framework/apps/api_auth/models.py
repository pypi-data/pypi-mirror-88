from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    avatar = models.TextField()

    class Meta(AbstractUser.Meta):
        db_table = 'AUTH_USER_MODEL'
