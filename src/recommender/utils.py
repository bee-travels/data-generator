import json
import csv

def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)

def write_json_to_file(json_data, file_name, minify=False):
    with open(file_name, "w+") as f:
        if minify:
            f.write(json.dumps(json_data))
            return
        json.dump(json_data, f, ensure_ascii=True, indent=2)

def generate_list_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())
    return data

def minify_json(file_name, new_file_name):
    data = load_json(file_name)
    write_json_to_file(data, new_file_name, True)

def write_csv_to_file(file_name, content, field_names):
    with open(file_name, "w+") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for row in content:
            writer.writerow(row)