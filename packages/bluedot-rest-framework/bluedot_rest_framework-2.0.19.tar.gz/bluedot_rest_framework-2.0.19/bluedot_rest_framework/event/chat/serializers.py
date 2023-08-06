from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
EventChat = import_string(api_settings.EVENT['chat']['models'])


class EventChatSerializer(CustomSerializer):

    class Meta:
        model = EventChat
        fields = '__all__'
