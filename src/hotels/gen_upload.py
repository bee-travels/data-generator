import os
import couchdb_upload_data
import mongo_upload_data
import postgres_upload_data
import hotels_data_gen
import utils
import logging


def get_data():
    if os.environ["GENERATE_DATA"] != "false":
        return hotels_data_gen.generate_data()
    logging.info("using local data")
    hotel_data = utils.load_json("hotel-data.json")
    hotel_info = utils.load_json("hotel-info.json")
    return hotel_data, hotel_info


def upload_to_db():
    hotel_data, hotel_info = get_data()

    database = os.environ["DATABASE"]
    if database == "couchdb":
        couchdb_upload_data.populate_couch(hotel_data, hotel_info)
    elif database == "mongodb":
        mongo_upload_data.populate_mongo(hotel_data, hotel_info)
    elif database == "postgres":
        postgres_upload_data.populate_postgres(hotel_data, hotel_info)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    upload_to_db()
