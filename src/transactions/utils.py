import json
def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)