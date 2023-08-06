import requests
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.response import Response
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler, jwt_get_userinfo_handler, jwt_get_openid_handler

from .register.models import EventRegister
from .data_download.models import EventDataDownload


class FrontendView:

    @action(detail=False, methods=['post'], url_path='list-frontend', url_name='list-frontend')
    def list_frontend(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(request.auth)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serializer(page, many=True).data

            for item in data['data']:
                item['is_register'] = 0
                if EventRegister.objects.filter(
                        user_id=user_id, event_id=data['event_id']):
                    item['is_register'] = 1

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
