from pymongo import MongoClient
import sys
import json
import os
import utils
import logging


def get_mongo_client():
    try:
        mongoHotels = MongoClient(os.environ["MONGO_CONNECTION_URL"])
        return mongoHotels
    except:
        exit("Error: Unable to connect to the database")


def delete_existing_collection(db, collection_name):
    try:
        logging.debug("trying to delete collection "+collection_name)
        for collection in db.list_collection_names():
            if collection == collection_name:
                db[collection].drop()
                logging.info("dropped collection " + collection)
                return
        logging.info("collection not found for deletion")
    except Exception as e:
        logging.warning("could not delete db ", collection_name)


def populate_mongo(data, info_data):
    client = get_mongo_client()
    db = client.beetravels
    delete_existing_collection(db, "flights")
    delete_existing_collection(db, "airports")

    logging.info("inserting data")
    db.airports.insert_many(info_data)
    db.flights.insert_many(data)
    logging.info("done inserting documents")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    flights = utils.load_json("flight_data.json")
    airports = utils.load_json("airports.json")
    populate_mongo(flights, airports)
