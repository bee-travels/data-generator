#!/usr/bin/python3
import csv
import random
import json
import math
import os
import uuid
import logging


def generate_data_for_destination(filename, hotels, image_urls, hotel_type):
    hotel_base_cost = 100
    csvfile = open(filename, "rt")
    reader = csv.reader(csvfile, delimiter=',')
    hotel_data = []

    for row in reader:
        cityname = row[0]
        country = row[3]
        population = int(row[5])
        cost_of_living_index = float(row[4])
        upper_limit = random.randint(35, 45)
        lower_limit = int(max(random.randint(10,15), math.floor(population / 100000)))
        num_hotels = int(min(lower_limit, upper_limit))
        hotels_in_city = []
        for i in range(num_hotels):
            hotels_in_city.append(
                get_hotel(city=cityname,
                          country=country,
                          hotels=hotels,
                          hotel_type=get_hotel_type(hotel_type),
                          image_urls=get_image_urls_subset(image_urls),
                          col_index=cost_of_living_index,
                          base_cost=hotel_base_cost)
            )
        hotel_data.extend(hotels_in_city)

    for i in range(len(hotel_data)):
        hotel_data[i]["id"] = str(uuid.uuid4())

    return hotel_data
    csvfile.close()


def write_json_to_file(json_data, file_name):
    with open(file_name, "w+") as f:
        json.dump(json_data, f, ensure_ascii=True, indent=2)


def generate_list_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())
    return data


def get_hotel_type(hotel_type):
    new_list = []
    for data in hotel_type:
        new_list = new_list + [data[0]] * data[1]

    return random.choice(new_list)


def get_hotels(hotel_list, superchain, hotel_type):
    hotels = {}
    for hotel in hotel_list:
        superchain_choice = superchain[random.randint(0, len(superchain) - 1)]
        hotel_group = get_hotel_type(hotel_type)
        if not hotel_group in hotels:
            hotels[hotel_group] = {}
        if not superchain_choice in hotels[hotel_group]:
            hotels[hotel_group][superchain_choice] = []
        hotels[hotel_group][superchain_choice].append(hotel)
    return hotels


def get_price_multiplier(hotel_type):
    if hotel_type == "budget":
        return 1
    elif hotel_type == "comfort":
        return 1.25
    else:
        return 2


def get_image_urls_subset(image_urls):
    indexes = set()
    urls = []
    count = random.randint(9, 12)
    for i in range(count):
        indexes.add(random.randint(0, len(image_urls) - 1))
    for index in list(indexes):
        urls.append(image_urls[index])
    return urls


def get_hotel(city, country, hotels, hotel_type, image_urls, col_index=1.0, base_cost=100):
    # col_index is the cost of living index for each city
    hotel = {}
    superchain = random.choice(list(hotels[hotel_type].keys()))
    hotel["city"] = city
    hotel["country"] = country
    hotel["superchain"] = superchain
    hotel["name"] = random.choice(hotels[hotel_type][superchain])
    hotel["type"] = hotel_type
    hotel["cost"] = math.ceil(get_price_multiplier(
        hotel_type) * (random.uniform(1, 1.5)) * col_index * base_cost)
    hotel["images"] = image_urls
    return hotel


def flatten_hotels(hotels):
    hotel = []
    for t, ss in hotels.items():
        for s, htls in ss.items():
            for h in htls:
                htl = {}
                htl["name"] = h
                htl["superchain"] = s
                htl["type"] = t
                htl["id"] = str(uuid.uuid4())
                hotel.append(htl)
    return hotel


def generate_hotel_id(hotel_data, hotel_list):
    for i in range(len(hotel_data)):
        for hotel in hotel_list:
            if hotel_data[i]["name"] == hotel["name"]:
                hotel_data[i]["hotel_id"] = hotel["id"]
    return hotel_data


def generate_data():
    logging.info("generating data for hotels")
    hotel_list = generate_list_from_file("hotel_names.txt")
    superchain = generate_list_from_file("superchain_names.txt")
    image_urls = generate_list_from_file("urls.txt")

    # array of tuples. (type, relative_number)
    # if the relative_number s are 3, 2, 1 type 1 will be 3 times as likely as type 3
    hotel_type = [("budget", 2), ("comfort", 1), ("luxury", 1)]

    hotels = get_hotels(hotel_list, superchain, hotel_type)
    hotel = flatten_hotels(hotels)

    hotel_data = generate_data_for_destination(
        "cities.csv", hotels, image_urls, hotel_type)

    hotel_data = generate_hotel_id(hotel_data, hotel)
    logging.info("data generation complete")
    return hotel_data, hotel

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    hotel_data, hotel_info = generate_data()
    write_json_to_file(hotel_data, "hotel-data.json")
    write_json_to_file(hotel_info, "hotel-info.json")
