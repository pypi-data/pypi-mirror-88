from rest_framework.routers import DefaultRouter
from django.utils.module_loading import import_string
from bluedot_rest_framework.settings import api_settings

EventQuestionView = import_string(api_settings.EVENT['question']['views'])
EventQuestionUserView = import_string(
    api_settings.EVENT['question']['user_views'])
EventScheduleView = import_string(api_settings.EVENT['schedule']['views'])
EventSpeakerView = import_string(api_settings.EVENT['speaker']['views'])
EventDataDownloadView = import_string(
    api_settings.EVENT['data_download']['views'])
EventRegisterView = import_string(api_settings.EVENT['register']['views'])
EventChatView = import_string(api_settings.EVENT['chat']['views'])
EventConfigurationView = import_string(
    api_settings.EVENT['configuration']['views'])
EventView = import_string(api_settings.EVENT['views'])


router = DefaultRouter(trailing_slash=False)


router.register(r'event/configuration', EventConfigurationView,
                basename='event-configuration')

router.register(r'event/question/user', EventQuestionUserView,
                basename='event-question-user')
router.register(r'event/chat', EventChatView,
                basename='event-chat')
router.register(r'event/register', EventRegisterView,
                basename='event-register')
router.register(r'event/question', EventQuestionView,
                basename='event-question')
router.register(r'event/data-download', EventDataDownloadView,
                basename='event-data-download')
router.register(r'event/speaker', EventSpeakerView,
                basename='event-speaker')
router.register(r'event/schedule', EventScheduleView,
                basename='event-schedule')
router.register(r'event', EventView,
                basename='event')

urlpatterns = router.urls
