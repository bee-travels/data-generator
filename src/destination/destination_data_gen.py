import csv
import json
import os
import uuid


def generate_data_for_destination(filename, image_filename):
    hotel_base_cost = 100
    csvfile = open(filename, "rt")
    reader = csv.reader(csvfile, delimiter=',')
    destination_data = []

    image_urls = generate_list_from_file(image_filename)

    for row in reader:
        id = str(uuid.uuid4())
        city = row[0]
        country = row[3]
        latitude = float(row[1])
        longitude = float(row[2])
        population = int(row[4])
        description = row[5].encode("ascii", errors="ignore").decode()
        images = get_images_for_destination(city, country, image_urls)
        destination = {
          "id": id,
          "city": city,
          "country": country,
          "latitude": latitude,
          "longitude": longitude,
          "population": population,
          "description": description,
          "images": images
        }
        destination_data.append(destination)

    csvfile.close()
    return destination_data


def get_images_for_destination(city, country, image_urls):
    images = []
    _city = city.replace(" ", "-").lower()
    _country = country.replace(" ", "-").lower()
    search_item = f'{_city}-{_country}'
    for url in image_urls:
        if search_item in url:
            images.append(url)
    return images


def generate_list_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())
    return data

def write_json_to_file(json_data, file_name):
    with open(file_name, "w+") as f:
        json.dump(json_data, f, ensure_ascii=True, indent=2)

def generate_destination_data():
    destination_data = generate_data_for_destination("cities.csv", "urls.txt")
    write_json_to_file(destination_data, "destination.json")
    return


def main():
    generate_destination_data()


if __name__ == "__main__":
    main()
