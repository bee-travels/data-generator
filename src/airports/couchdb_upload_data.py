import couchdb
import json
import sys
import os
import utils
import logging
import requests


def create_db(couch, db_name):
    try:
        logging.debug("trying to create db : "+db_name)
        db = couch.create(db_name)
        logging.info("DB created")
        return db
    except Exception as e:
        logging.warning("DB Not created")
        exit("error: unable to create db")
        print(e)


def get_db(couch, db_name):
    try:
        logging.debug("trying to find db : "+db_name)
        db = couch[db_name]
        logging.info("DB found")
        return db
    except Exception as e:
        logging.warning("DB not found")
        logging.info("will creat db")
        print(e)
    return create_db(couch, db_name)


def delete_db(couch, db_name):
    try:
        logging.debug("trying to delete db "+db_name)
        del couch[db_name]
        logging.debug("deleted db " + db_name)
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
    r = requests.post(url, json=data, headers={
                      "Content-Type": "application/json", "Accept": "application/json"})
    if r.status_code == 201:
        logging.info("data upload succeeded")
    else:
        logging.error("failed to upload data")


def upload_data(couch, data, db_name):
    db = get_db(couch, db_name)
    bulk_upload_data(db_name, data)


def populate_couch(data, info):
    try:
        couch = couchdb.Server(os.environ["COUCH_CONNECTION_URL"])

        delete_db(couch, "airports")
        delete_db(couch, "flights")

        logging.info("starting data upload")
        upload_data(couch, data, "flights")
        upload_data(couch, info, "airports")
        logging.info("data upload complete")
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    flights = utils.load_json("flight_data.json")
    airports = utils.load_json("airports.json")
    populate_couch(flights, airports)
