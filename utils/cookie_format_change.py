import base64
import json


def cookie_to_base64(cookie_json):
    try:
        json_string = json.dumps(cookie_json)
        return base64.b64encode(json_string.encode()).decode()
    except:
        return None


def cookie_to_json(cookie_base64):
    try:
        encoded_cookie = cookie_base64
        decoded_string = base64.b64decode(encoded_cookie).decode()
        return json.loads(decoded_string)
    except:
        return None
