# -*- coding: utf-8 -*-
from __future__                      import unicode_literals
from django.shortcuts                import render, redirect
from django.http                     import HttpResponse;
from django.http                     import HttpRequest;
from twilio.rest                     import Client            #Library for Django to facilitate interaction with Twilio.
from twilio.twiml.messaging_response import MessagingResponse #Library for Django to facilitate interaction with Twilio.
from django.views.decorators.csrf    import csrf_exempt       #Necesary to avoid security message from django for not having a CSRF
import json;
import requests;

###**************************************************
### Author : Project Created By Rodolfo Valdivieso.
### Date   : FEB-27-2018.
### Version: V 1.0.
###**************************************************
### Description: - Communication Pipe between Slack - Twilio.
### This Web App allowed you to Manage Messages between Slack API and Twillio API.
### If a meesage is post on slack, it will trigger an event and Slack will send a POST Request
### to the the URL specified in the settings.
### That request will be handled here and will create a new Post Reques to Twilio API with the message.
### The same way, If the SMS is replied, Twilio API will create a Post request to the specific URL.
### Then the request will be handle here and redirected to Slack API and show the message.

### For testing:
### Run ngrok htpp 8000 ang get the URL
### Update in Slack APP - Event API and Webhook the new URL
### Update webhook in Twilio.
### Go to settings.py and add allowed_host the new URL
### Add Api keys and phone numbers in views.


# To test this app, is necessary to create an Slack acc, Slack app, Twilio acc, and to use NGROK.

# Create your views here.
#View to render the landing page and allow the user to send a message to Slack or Twilio.
def index(request):
  return render(request, 'first_app/index.html')

# Method to handle a User request to Send a Message to Slack form the App.
def slackMessageSender(request):
  message   = request.POST['contentSlack']
  content   = sendMessageToSlack(message)
  context   = {"responseSlack":content}
  return render(request, 'first_app/index.html', context)

# Method to handle a User request to Send a Message to Twilio form the App.
def twilioMessageSender(request):
  to        = "+1"+ request.POST['phone']
  fromPhone = "xxxxx"
  body      = request.POST['contentTwilio']
  message   = sendMessageToTwilio(fromPhone, to, body)
  #print message
  context   = {"responseTwilio":message}
  return render(request, 'first_app/index.html', context)


# Method to handle a POST Request from Twilio. Incoming message from Twilio.
@csrf_exempt
def smsReceived(request):
  # print request.body
  content  = request.POST.get('Body', '')
  response = sendMessageToSlack(content)
  twiml    = '<Response><Message>Message Sent To Slack!</Message></Response>'
  return HttpResponse(twiml, content_type='text/xml')

# Method to handle a Slack POST request. Incoming message from Slack.
@csrf_exempt
def slackRecieved(request):
  json_data = json.loads(request.body)
  # print json_data
  if json_data['type'] == "url_verification":
  	return HttpResponse(json_data['challenge'], content_type='text/plain')
  print json_data['event']['text']
  content   = json_data['event']['text']
  message   = sendMessageToTwilio("xxxxx", "xxxx", content)
  return HttpResponse("ok", content_type='text/plain')


# Method to send a Message to Twilio
def sendMessageToTwilio(fromPhone, to, body):
  account   = "xxxx"
  token     = "xxxx"
  client    = Client(account, token)
  message   = client.messages.create(to=to, from_=fromPhone,body=body)
  return message

# Method to send a Message to Slack.
def sendMessageToSlack(message):
  post_data = {"text": message}
  response  = requests.post('xxxxx', json=post_data)
  return response.content
