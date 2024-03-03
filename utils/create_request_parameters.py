import json

def take_payload_data(payload_file_path):
    with open(f'{payload_file_path}', 'r') as file:
        return json.load(file)
