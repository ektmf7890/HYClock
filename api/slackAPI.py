import requests
import json
from django.conf import settings

def slack(text):
    url = settings.SECRETS.get("SLACK_CS_WEBHOOK")
    data = {
        "payload": json.dumps({"text": text})
        
    }
    return requests.post(url, data=data)
