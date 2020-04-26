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
        exit("error: unable to create db")
        print(e)


def get_db(couch, db_name):
    try:
        logging.debug("trying to find db : ", db_name)
        db = couch[db_name]
        logging.info("DB found")
        return db
    except Exception as e:
        logging.warning("DB not found")
        logging.info("will creat db")
        print(e)
    return create_db(couch, db_name)


def bulk_load_data(db, json_data, upload_name):
    print(upload_name)
    for data in json_data:
        db.save(data)
    print(upload_name + " completed")


def upload_data(couch, data, db_name):
    db = get_db(couch, db_name)
    bulk_load_data(db, data, db_name)


def main():
    try:
        couch = couchdb.Server(os.environ["COUCH_CONNECTION_URL"])
        car_data = utils.load_json("cars.json")
        car_info = utils.load_json("car-info.json")

        upload_data(couch, car_data, "cars")
        upload_data(couch, car_info, "car_info")
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()
