from django.db import models
from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    avatar = models.TextField()

    class Meta:
        app_label = 'bluedot_rest_framework.apps.api_auth.models.AuthUser'
