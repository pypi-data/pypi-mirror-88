from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    avatar = models.TextField()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
