from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$'           , views.index              ),
  url(r'^slack/send$' , views.slackMessageSender ),
  url(r'^twilio/send$', views.twilioMessageSender),
  url(r'^sms/$'       , views.smsReceived        ),
  url(r'^slack/$'     , views.slackRecieved      )
]