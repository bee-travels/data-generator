import json


def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)


def write_json_to_file(json_data, file_name, minify=False):
    with open(file_name, "w+") as f:
        if minify:
            f.write(json.dumps(json_data))
            return
        json.dump(json_data, f, ensure_ascii=True, indent=2)
