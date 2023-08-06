from rest_framework_mongoengine.serializers import DocumentSerializer
from bluedot_rest_framework.settings import api_settings

EventConfiguration = api_settings.EVENT['configuration']['models']


class EventConfigurationSerializer(DocumentSerializer):

    class Meta:
        model = EventConfiguration
        fields = '__all__'
