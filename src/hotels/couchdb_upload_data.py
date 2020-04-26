import couchdb
import json
import sys
import os
import utils
import logging
import requests

def create_db(couch, db_name):
    try:
        logging.debug("trying to create db : "+ db_name)
        db = couch.create(db_name)
        logging.info("DB created")
        return db
    except Exception as e:
        logging.warning("DB Not created")
        logging.error(e)

def get_db(couch, db_name):
    try:
        logging.debug("trying to find db : "+ db_name)
        db = couch[db_name]
        logging.info("DB found")
        return db
    except Exception as e:
        logging.warning("DB not found")
        logging.info("will creat db")
        logging.warning(e)
    return create_db(couch, db_name)


def delete_db(couch, db_name):
    try:
        logging.debug("trying to delete db "+db_name)
        del couch[db_name]
        logging.debug("deleted db "+ db_name)
    except Exception as e:
        logging.warning("db not deleted")
        logging.error(e)

def bulk_load_data(db, json_data, upload_name):
    print(upload_name)
    for data in json_data:
        db.save(data)
    print(upload_name + " completed")

def bulk_upload_data(db_name, json_data):
    url = f'{os.environ["COUCH_CONNECTION_URL"]}/{db_name}/_bulk_docs'

    data = {'docs': json_data}
    r = requests.post(url, json=data, headers = {"Content-Type": "application/json", "Accept": "application/json"})
    if r.status_code == 201:
        logging.info("data upload succeeded")
    else:
        logging.error("failed to upload data")

def upload_data(couch, data, db_name):
    db = get_db(couch, db_name)
    bulk_upload_data(db_name, data)

def populate_db():
    try:
        couch = couchdb.Server(os.environ["COUCH_CONNECTION_URL"])
        car_data = utils.load_json("hotel-data.json")
        car_info = utils.load_json("hotel-info.json")

        delete_db(couch, "hotels")
        delete_db(couch, "hotel_info")

        logging.info("starting data upload")
        upload_data(couch, car_data, "hotels")
        upload_data(couch, car_info, "hotel_info")
        logging.info("data upload complete")
    except Exception as e:
        logging.error(e)

def main():
    populate_db()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
