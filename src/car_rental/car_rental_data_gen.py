import csv
import os
import json
import math
import random
import uuid
import logging

TYPE_BASIC = "basic"
TYPE_LUXURY = "luxury"
TYPE_PREMIUM = "premium"

BODY_SUV = "suv"
BODY_SEDAN = "sedan"
BODY_HATCHBACK = "hatchback"
BODY_CROSSOVER = "crossover"
BODY_CONVERTIBLE = "convertible"
BODY_MUSCLE = "muscle"
BODY_SPORTS = "sports"

def generate_list_from_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.strip())
    return data


def generate_car_type_data(filename, urls):

    car_info = {}
    with open('cars.csv') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        for row in csv_reader:
            vehicle_type = TYPE_BASIC
            if int(row[3]) > 60:
                vehicle_type = TYPE_LUXURY
            elif int(row[3]) > 35:
                vehicle_type = TYPE_PREMIUM

            body_type = row[2]

            if not car_info.get(body_type):
                car_info[body_type] = {}

            if not car_info[body_type].get(vehicle_type):
                car_info[body_type][vehicle_type] = []

            car_values = {
                "id": str(uuid.uuid4()),
                "name": row[0],
                "image": urls.get(row[1]),
                "price_multiplier": row[3]
            }
            car_info[body_type][vehicle_type].append(car_values)
    return car_info


def get_available_types(col_index):
    availbale_types = []
    if col_index >= 1.5:
        availbale_types = [BODY_SPORTS, BODY_MUSCLE,
                           BODY_CONVERTIBLE, BODY_SUV, BODY_SEDAN, BODY_CROSSOVER]
    elif col_index >= 1:
        availbale_types = [BODY_SEDAN, BODY_SUV,
                           BODY_CROSSOVER, BODY_HATCHBACK, BODY_MUSCLE]
    else:
        availbale_types = [BODY_SEDAN, BODY_SUV, BODY_HATCHBACK]
    return availbale_types


def get_available_style(car_info, body_type):
    styles = list(car_info[body_type].keys())
    return styles


def generate_car_data_for_city(city, country, col_idx, population, car_info, base_cost=30):
    car_data = []
    car_rentals = generate_list_from_file('car_rental.txt')
    availbale_types = get_available_types(col_idx)
    upper_limit = random.randint(45, 55)
    car_count = int(min(math.floor(population / 100000), upper_limit))
    for i in range(car_count):
        body_type = random.choice(availbale_types)
        car_rental = random.choice(car_rentals)
        styles = get_available_style(car_info, body_type)
        style = random.choice(styles)
        selected_car = random.choice(car_info[body_type][style])
        car_cost = math.ceil(math.sqrt(float(selected_car["price_multiplier"]))
                             * math.sqrt(col_idx) * random.uniform(.9, 1.1) * base_cost)
        car = {
            "id": str(uuid.uuid4()),
            "car_id": selected_car["id"],
            "city": city,
            "country": country,
            "name": selected_car["name"],
            "rental_company": car_rental,
            "image": selected_car["image"],
            "cost": car_cost,
            "body_type": body_type,
            "style": style
        }
        car_data.append(car)
    return car_data


def flatten_car_info(car_info):
    flat_info = []
    for body_type, data in car_info.items():
        for style, cars in data.items():
            for car in cars:
                info = {
                    "id": car["id"],
                    "name": car["name"],
                    "image": car["image"],
                    "body_type": body_type,
                    "style": style
                }
                flat_info.append(info)


    return flat_info


def generate_car_data(car_info, filename, urls):

    car_data = []
    base_cost = 30

    with open('cities.csv') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        for row in reader:
            city = row[0]
            country = row[3]
            population = int(row[5])
            cost_of_living_index = float(row[4])

            car_data_for_city = generate_car_data_for_city(city, country,
                                                           cost_of_living_index, population, car_info, base_cost)
            car_data.extend(car_data_for_city)
    return car_data


def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)

def generate_data():
    urls = load_json("urls.json")
    car_info = generate_car_type_data('cars.csv', urls)
    car_data = generate_car_data(car_info, 'cities.csv', urls)
    flat_info = flatten_car_info(car_info)
    return car_data, flat_info

def main():
    logging.info("generating data for cars")
    car_data, car_info = generate_data()
    logging.info("done gerating car data")

    with open('cars.json', 'w', encoding='utf-8') as f:
        json.dump(car_data, f, ensure_ascii=True, indent=2)

    with open('car-info.json', 'w', encoding='utf-8') as f:
        json.dump(car_info, f, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
