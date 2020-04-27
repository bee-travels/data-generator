import os
import couchdb_upload_data
import mongo_upload_data
import postgres_upload_data
import car_rental_data_gen
import utils
import logging


def get_data():
    if os.environ["GENERATE_DATA"] != "false":
        return car_rental_data_gen.generate_data()
    logging.info("using local data")
    car_data = utils.load_json("cars.json")
    car_info = utils.load_json("car-info.json")
    return car_data, car_info


def upload_to_db():
    car_data, car_info = get_data()

    database = os.environ["DATABASE"]
    if database == "couchdb":
        couchdb_upload_data.populate_couch(car_data, car_info)
    elif database == "mongodb":
        mongo_upload_data.populate_mongo(car_data, car_info)
    elif database == "postgresdb":
        postgres_upload_data.populate_postgres(car_data, car_info)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    upload_to_db()
