import couchdb
import json
import sys
import os
import utils


def create_db(couch, db_name):
    try:
        db = couch.create(db_name)
        return db
    except Exception as e:
        print("DB Not created")
        print(e)


def get_db(couch, db_name):
    try:
        db = couch[db_name]
        return db
    except Exception as e:
        print("DB not found")
        print(e)
    return create_db(couch, db_name)

def bulk_load_data(db, json_data, upload_name):
    print(upload_name)
    for data in json_data:
        db.save(data)
    print(upload_name + " completed")


def main():
    couch = couchdb.Server(os.environ["COUCH_CONNECTION_URL"])
    car_db = get_db(couch, "car_rental")
    car_data = utils.load_json("cars.json")
    bulk_load_data(car_db, car_data, "Car Data")
    car_info = utils.load_json("car-info.json")
    info_db = get_db(couch, "car-info")
    bulk_load_data(info_db, car_info, "Car Info")

if __name__ == "__main__":
    main()
