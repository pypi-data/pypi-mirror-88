from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    avatar_url = models.TextField()

    class Meta:
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'
