from rest_framework.routers import DefaultRouter
from bluedot_rest_framework.settings import api_settings

EventQuestionView = api_settings.EVENT['question']['views']
EventQuestionUserView = api_settings.EVENT['question']['user_views']
EventScheduleView = api_settings.EVENT['schedule']['views']
EventSpeakerView = api_settings.EVENT['speaker']['views']
EventDataDownloadView = api_settings.EVENT['data_download']['views']
EventRegisterView = api_settings.EVENT['register']['views']
EventChatView = api_settings.EVENT['chat']['views']
EventConfigurationView = api_settings.EVENT['configuration']['views']
EventView = api_settings.EVENT['views']


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
