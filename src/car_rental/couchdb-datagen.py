import couchdb
import json

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
    couch = couchdb.Server("http://127.0.0.1:5984/")
    db = get_db(couch, "cars")
    # data = load_json("cars.json")
    # bulk_load_data(db, data)

    mango = {"selector": {"city": {"$eq": "New York"}}}
    for row in db.find(mango):
        print(row["name"], row["cost"], row["rental_company"])


if __name__ == "__main__":
    main()