from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import EventConfiguration


class EventConfigurationSerializer(DocumentSerializer):

    class Meta:
        model = EventConfiguration
        fields = '__all__'
