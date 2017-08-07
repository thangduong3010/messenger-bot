import os
import sys
import json

import requests
from flask import Flask, request


app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    """ when the endpoint is registered as a webhook, it must echo back
    the 'hub.challenge' value it receives in the query arguments

    :rtype tuple: (message, return code)
    """
    if (request.args.get("hub.mode") == "subscribe" and
            request.args.get("hub.challenge")):
        if not (request.args.get("hub.verify_token") ==
                os.environ["VERIFY_TOKEN"]):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/messenger', methods=['POST'])
def messenger_webhook():
    """ endpoint for processing incoming messaging events
    
    :rtype tuple: (message, return code)
    """
    data = request.get_json()
    log(data, "DATA")

    if data["object"] == "page":

        for entry in data["entry"]:
            log(entry, "ENTRY")
            for messaging_event in entry["messaging"]:
                # someone sent a message
                # the facebook ID of the person sending you the message
                sender_id = messaging_event["sender"]["id"]
                if messaging_event.get("message"):
                    # the recipient's ID - your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]
                    # the message's text
                    message_text = messaging_event["message"]["text"]
                    # for now, the respond will be "roger that!"
                    send_message(sender_id, "roger that!")

                # delivery confirmation
                if messaging_event.get("delivery"):
                    pass
                # optin confirmation
                if messaging_event.get("optin"):
                    pass
                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return "ok", 200


def send_message(recipient_id, message_text=None):
    """
    :param recipient_id:
    :param message_text:
    """

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data_ = {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

    data = json.dumps(data_)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message, entity=None):
    """ simple wrapper for logging to stdout on heroku

    :param message:
    :param entity: log identifier
    """
    out = "{0}: {1}".format(entity, message) if entity is not None else message
    print str(out)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
