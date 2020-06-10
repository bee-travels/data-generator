import os
import couchdb_upload_data
import mongo_upload_data
import postgres_upload_data
import destination_data_gen
import utils
import logging


def get_data():
    if os.environ["GENERATE_DATA"] != "false":
        return destination_data_gen.generate_data()
    logging.info("using local data")
    destination_data = utils.load_json("destination.json")
    return destination_data


def upload_to_db():
    destination_data = get_data()

    database = os.environ["DATABASE"]
    if database == "couchdb":
        couchdb_upload_data.populate_couch(destination_data)
    elif database == "mongodb":
        mongo_upload_data.populate_mongo(destination_data)
    elif database == "postgres":
        postgres_upload_data.populate_postgres(destination_data)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    upload_to_db()
