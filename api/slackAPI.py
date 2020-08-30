import requests
import json
from django.conf import settings

def slack(title, text):
    url = settings.SECRETS.get("SLACK_CS_WEBHOOK")
    data = {
        "payload": json.dumps({
            "pretext": ":loudspeaker: " + title,
            "text": text    
        })
    }
    return requests.post(url, data=data)
