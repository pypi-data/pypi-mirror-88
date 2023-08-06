from datetime import datetime
from rest_framework.decorators import (action)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .func import get_tree
from .jwt_token import jwt_get_userid_handler, jwt_get_openid_handler, jwt_get_unionid_handler


class CustomModelViewSet(ModelViewSet):
    model_class = None

    def get_queryset(self):
        queryset = self.model_class.objects.all()
        return queryset


def user_perform_create(token, serializer):
    user_id = jwt_get_userid_handler(token)
    openid = jwt_get_openid_handler(token)
    unionid = jwt_get_unionid_handler(token)
    serializer.save(user_id=user_id, openid=openid, unionid=unionid)


class TreeAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        parent = request.query_params.get('parent', 0)
        data = get_tree(serializer.data, parent)
        return Response(data)


class AllView:

    @action(detail=False, methods=['get'], url_path='all', url_name='all')
    def all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
