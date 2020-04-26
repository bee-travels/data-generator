from pymongo import MongoClient
import sys
import json
import os
import utils

def get_mongo_client():
    try:
        mongoHotels = MongoClient(os.environ["MONGO_CONNECTION_URL"])
        return mongoHotels
    except:
        exit("Error: Unable to connect to the database")

def populate_mongo():
    car_data = utils.load_json("cars.json")
    car_info_data = utils.load_json("car-info.json")
    
    mongoHotels = get_mongo_client()
    db = mongoHotels.beetravels

    db.car_info.insert_many(car_info_data)
    db.cars.insert_many(car_data)

if __name__ == "__main__":
    populate_mongo()
