from app import app
from flask import make_response, request

import json
import requests

WEBHOOK_VERIFY_TOKEN = 'test_faq_token'
PAGE_ACCESS_TOKEN = 'EAAKDUMycqoIBADymkmpSZBPz8YVSrjI4jfZA52vgY6MtGaXdlsSfRfyAFHsXpdDTORNjv7G84gzg1OefMPnjA9g1Nc6ALGMlHgrI97uZCfimdGfzWyk9rEIZAdhJvMoFqyz6RWfn6trsKAH3SAoEylpwstzqz4vu62QfZAKt986GZAxZBbZBJT6DNZCP4NeZC6i0dCjzgxTXBCQ0T9xHapnx2GkwoeItvtzZCIZD'

SEND_API_URL = 'https://graph.facebook.com/v5.0/me/messages?access_token=%s'\
  % PAGE_ACCESS_TOKEN

HEADERS = {'content-type': 'application/json'}

def send_message(body):
  try:
    for entry in body['entry']:
        if 'messaging' in entry:
          channel = 'messaging'
        else:
          channel = 'standby'
        for message in entry[channel]:
          sender = message['sender']['id']
          recipient_id =  message['recipient']['id']
          if 'message' in message: 
            webhook_type='message'
          elif 'postback' in message:
            webhook_type='postback' 
          else:
            return
          if 'text' in message[webhook_type]:
            msg_text = message[webhook_type]['text']
          if 'is_echo' in message[webhook_type]:
            return
          else:
            send_message_to_recipient(msg_text, sender, recipient_id)
  except Exception as e:
     print("Exception sending")
     print(e)
      
      
def send_message_to_recipient(message_text, recipient_id, page_id):
  message = {
    'recipient': {
      'id': recipient_id,
    },
    'message': {
      'text': message_text,
    },
  }
  r = requests.post(SEND_API_URL, data=json.dumps(message), headers=HEADERS)
  if r.status_code != 200:
    print('== ERROR====')
    print(SEND_API_URL)
    print(r.json())
    print('==============')

    
@app.route('/')
@app.route('/index')
def index():
  return 'Hello, World!'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    mode = request.args['hub.mode']
    token = request.args['hub.verify_token']
    challenge = request.args['hub.challenge']
    if mode and token:
      if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return challenge
      else:
        return make_response('wrong token', 403)
    else:
      return make_response('invalid params', 400)
  else: # POST
    body = json.loads(request.data)
    send_message(body)
    print("hi this is webhook")
    print(body)
    #send_message(body)
    return ("", 205)

