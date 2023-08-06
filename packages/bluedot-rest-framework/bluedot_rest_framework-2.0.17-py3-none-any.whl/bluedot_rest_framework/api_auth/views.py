from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import AuthUserSerializer


class CurrentUserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = AuthUserSerializer(request.user, context={
            'request': request}).data
        return Response(user)


current_user_url = CurrentUserAPIView.as_view()
