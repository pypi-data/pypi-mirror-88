from django.db.models import get_model
from rest_framework import serializers


class AuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_model('auth', 'User')
        fields = '__all__'
