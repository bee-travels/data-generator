from faker import Faker
import random
import json
import requests

def write_json_to_file(json_data, file_name, minify=False):
    with open(file_name, "w+") as f:
        if minify:
            f.write(json.dumps(json_data))
            return
        json.dump(json_data, f, ensure_ascii=True, indent=2)


def get_reason():
    return random.choice(['business', 'leisure', 'family'])


def get_party_size(reason, marital_status):
    if reason == 'business':
        return random.choice([1,1,1,1,2,2,3,4])
    elif reason == 'leisure' and marital_status == 'married':
        return random.choice([1,1,2,2,2,2,3,3,4,4,5,6])
    elif reason == 'family':
        return random.choice([1,2,2,2,3,3,3,3,4,4,4,5,5,6,6,7])


def get_marital_status():
    return random.choice(['single', 'married'])


def get_priority(reason, income):
    if income > 200000 and reason == 'business':
        return "time"
    elif income > 200000:
        return 'luxury'
    elif reason == 'family' or reason == 'leisure' and income > 100000:
        return 'comfort'
    else:
        return 'budget'


def get_travel_frequency(reason, income):
    if reason == "business" and income > 200000:
        return random.randint(10, 50)
    elif income > 200000:
        return random.randint(5, 40)
    elif reason == "business":
        return random.randint(5, 30)
    else:
        return random.randint(2, 10)

def get_income():
    weights = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,5,6,7,8,9,10,11,12]
    base = random.randint(40000, 60000)
    multiplier = random.choice(weights)
    return base * multiplier

def get_car_rental_company():
    return random.choice(['Carlux','Rent Pad','Chakra','Capsule','Rentio'])

def get_hotel_chain():
    return random.choice(['Urban Lifestyle','Elegant Enigma Alliance','Nimbus Elites'])

def get_airline():
    return random.choice(['MilkyWay Airlanes','Spartan Airlines','Phoenix Airlines','Liberty Airlines'])

def get_frequently_visited_cities(reason, frequency, destinations):
    count = 0
    if reason == 'business' and frequency > 25:
        count = random.randint(5, 40)

    elif (reason == 'leisure' or reason == 'family') and frequency > 25:
        count = random.randint(int(frequency / 2), frequency)

    else:
        count = random.randint(min(3, frequency), max(10, frequency))

    result = []

    for _ in range(count):
        result.append(random.choice(destinations))
    return result

def map_destinations(destination):
    return destination["city"]

def get_destinations():
    r = requests.get("https://bee-travels.v2.ibmdeveloper.net/api/v1/destinations")
    return r.json()

fake = Faker()

users = []

destinations = get_destinations()

for _ in range(100):
    reason = get_reason()
    income = get_income()
    marital_status = get_marital_status()
    travel_frequency = get_travel_frequency(reason, income)
    user = {
        "name": fake.name(),
        "income": income,
        "address": fake.address(),
        "car_rental_loyalty": get_car_rental_company(),
        "hotel_chain_loyalty": get_hotel_chain(),
        "airlines_loyalty": get_airline(),
        "travel_frequency": travel_frequency,
        "priority": get_priority(reason, income),
        "frequently_visited_cities": get_frequently_visited_cities(reason, travel_frequency, destinations),
        "marital_status": marital_status,
        "party_size": get_party_size(reason, marital_status),
        "main_reason_for_travel": reason
    }
    users.append(user)

write_json_to_file(users, 'user.json')


