import couchdb
import json
import sys


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


def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)


def bulk_load_data(db, json_data):
    for data in json_data:
        print("Inserrting data for %s, %s" % (data["city"], data["country"]))
        db.save(data)


def main():
    couch = couchdb.Server("http://127.0.0.1:5985/")
    hotel_db = get_db(couch, "hotel")
    hotel_data = load_json("hotel-data.json")
    bulk_load_data(hotel_db, hotel_data)
    hotel_info = load_json("hotel-info.json")
    info_db = get_db(couch, "hotel-info")
    bulk_load_data(info_db, hotel_info)
    # print(db.index())
    # city = {'selector': {'city': 'Durban'},
    #          'fields': ['city', 'country'],
    #          'sort': [{'name': 'asc'}]}
    # for row in db.find(city):
    #     print(row)


if __name__ == "__main__":
    main()
