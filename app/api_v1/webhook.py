import requests, json
from flask import Response, request, current_app
from . import api
from .. import db

@api.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@api.route('/webhook', methods=['POST'])
def webhook_action():
    data = request.get_json()
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        handle_message(user_id, user_message)
    return Response(response="EVENT RECEIVED",status=200)

@api.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = request.get_json()
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    return handle_message_dev(user_id, user_message)

@api.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

def action(user_id, user_message):
    # do something ¯\_(ツ)_/¯ with the user_message and user_id
    return "Hello, user #"+user_id+", you sent : "+user_message

def handle_message(user_id, user_message):
    text = action(user_id, user_message)
    response = {
        'recipient': {'id': user_id},
        'message': {'text': text}
    }
    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages/?access_token=' + os.environ.get('FB_ACCESS_TOKEN'), json=response)

def handle_message_dev(user_id, user_message):
    text = action(user_id, user_message)
    response = {
        'recipient': {'id': user_id},
        'message': {'text': text}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
