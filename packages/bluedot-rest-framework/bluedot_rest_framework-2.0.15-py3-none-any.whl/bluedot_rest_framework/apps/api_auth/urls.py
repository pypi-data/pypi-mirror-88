from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import current_user_url

urlpatterns = [
    url(r'^auth/login', obtain_jwt_token),
    url(r'^auth/current', current_user_url),
]
