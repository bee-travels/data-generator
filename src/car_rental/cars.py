import csv
import os
import json
import math
import random

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

            print(row[1])
            car_values = {
                "name": row[0], "image": urls.get(row[1]), "price_multiplier": row[3]}
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
    car_count = min(math.floor(population / 100000), upper_limit)
    for i in range(car_count):
        body_type = random.choice(availbale_types)
        car_rental = random.choice(car_rentals)
        styles = get_available_style(car_info, body_type)
        style = random.choice(styles)
        selected_car = random.choice(car_info[body_type][style])
        car_name = selected_car["name"]
        car_image = selected_car["image"]
        car_cost = math.ceil(math.sqrt(float(selected_car["price_multiplier"]))
                             * math.sqrt(col_idx) * random.uniform(.9, 1.1) * base_cost)
        car = {}
        car["city"] = city
        car["country"] = country
        car["name"] = car_name
        car["rental_company"] = car_rental
        car["image"] = car_image
        car["cost"] = car_cost
        car["body_type"] = body_type
        car["style"] = style
        car_data.append(car)
    return car_data


def generate_car_data(filename, urls):
    car_data = []
    base_cost = 30
    car_info = generate_car_type_data('cars.csv', urls)
    with open('cities.csv') as csvFile:
        reader = csv.reader(csvFile, delimiter=",")
        for row in reader:
            city = row[0]
            country = row[3]
            print("Generating Data for %s, %s" % (city, country))
            population = int(row[5])
            cost_of_living_index = float(row[4])

            car_data_for_city = generate_car_data_for_city(city, country,
                                                           cost_of_living_index, population, car_info, base_cost)
            car_data.extend(car_data_for_city)
    return car_data


def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)


def main():
    urls = load_json("urls.json")
    car_data = generate_car_data('cities.csv', urls)

    with open('cars.json', 'w', encoding='utf-8') as f:
        json.dump(car_data, f, ensure_ascii=True, indent=2)


if __name__ == "__main__":
    main()
