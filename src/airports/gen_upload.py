import os
import couchdb_upload_data
import mongo_upload_data
import postgres_upload_data
import airport_data_gen
import utils
import logging


def get_data():
    if os.environ["GENERATE_DATA"] != "false":
        return airport_data_gen.generate_data()
    logging.info("using local data")
    airport = utils.load_json("airports.json")
    flights = utils.load_json("flight_data.json")
    return flights, airport


def upload_to_db():
    flights, airports = get_data()

    database = os.environ["DATABASE"]
    if database == "couchdb":
        couchdb_upload_data.populate_couch(flights, airports)
    elif database == "mongodb":
        mongo_upload_data.populate_mongo(flights, airports)
    elif database == "postgresdb":
        postgres_upload_data.populate_postgres(flights, airports)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    upload_to_db()
