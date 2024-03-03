import base64
import json

def cookie_to_base64(cookie_json):
    json_string = json.dumps(cookie_json)
    return base64.b64encode(json_string.encode()).decode()

def cookie_to_json(cookie_base64):
    encoded_cookie = cookie_base64
    decoded_string = base64.b64decode(encoded_cookie).decode()
    return json.loads(decoded_string)
