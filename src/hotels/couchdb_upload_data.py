import couchdb
import json
import sys
import os
import utils
import logging

def create_db(couch, db_name):
    try:
        logging.debug("trying to create db : ", db_name)
        db = couch.create(db_name)
        logging.info("DB created")
        return db
    except Exception as e:
        logging.warning("DB Not created")
        logging.error(e)

def get_db(couch, db_name):
    try:
        logging.debug("trying to find db : ", db_name)
        db = couch[db_name]
        logging.info("DB found")
        return db
    except Exception as e:
        logging.warning("DB not found")
        logging.info("will creat db")
        logging.warning(e)
    return create_db(couch, db_name)

def bulk_load_data(db, json_data, upload_name):
    print(upload_name)
    for data in json_data:
        db.save(data)
    print(upload_name + " completed")

def upload_data(couch, data, db_name):
    db = get_db(couch, db_name)
    bulk_load_data(db, data, db_name)

def populate_db():
    try:
        couch = couchdb.Server(os.environ["COUCH_CONNECTION_URL"])
        hotel_data = utils.load_json("hotel-data.json")
        hotel_info = utils.load_json("hotel-info.json")
        upload_data(couch, hotel_data, "hotels")
        upload_data(couch, hotel_info, "hotel_info")
    except Exception as e:
        logging.error(e)

def main():
    populate_db()

if __name__ == "__main__":
    main()
