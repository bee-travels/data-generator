from pymongo import MongoClient
import sys
import json

try:
    mongoHotels = MongoClient(sys.argv[1])
except:
    exit("Error: Unable to connect to the database")

def populate_mongo():
    hotel_data = get_generated_data()
    hotel_info_data = get_hotel_info()

    mongoHotels.beetravels.hotels.insert_one(hotel_info_data)

    for hotel in hotel_data:
        mongoHotels.beetravels.hotels.insert_one(hotel)

def get_generated_data():
    with open("hotel-data.json", "r") as hotel_file:
        raw_data = hotel_file.read()
    
    hotel_data = json.loads(raw_data)
    return hotel_data

def get_hotel_info():
    with open("hotel-info.json", "r") as hotel_info_file:
        raw_data = hotel_info_file.read()
    
    hotel_info_data = json.loads(raw_data)
    return hotel_info_data

if __name__ == "__main__":
    populate_mongo()
