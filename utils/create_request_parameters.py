import json

_group_post_hash = "20b60f764fe0077f3d"
_account_post_hash = "7dfa0bdfd13d4aa7be"

def vk_account_post_details(payload, account_id, post_text):
    payload['to_id'] = account_id
    payload['Message'] = post_text
    payload['hash'] = f'{_account_post_hash}'
    return payload


def vk_group_post_details(payload, group_id, post_text):
    payload['to_id'] = f"-{group_id}"
    payload['Message'] = post_text
    payload['_ads_group_id'] = group_id
    payload['hash'] = f'{_group_post_hash}'
    return payload


def take_payload_data(payload_file_path):
    with open(f'{payload_file_path}', 'r') as file:
        return json.load(file)
