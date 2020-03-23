import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json

try:
    conn = psycopg2.connect("user='{}' host='{}' password='{}'".format(sys.argv[2], sys.argv[1], sys.argv[3]))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    curr = conn.cursor()
    curr.execute("CREATE DATABASE beetravels")
    curr.close()
    conn.close()
    conn = psycopg2.connect("dbname='beetravels' user='{}' host='{}' password='{}'".format(sys.argv[2], sys.argv[1], sys.argv[3]))
    curr = conn.cursor()
except:
    exit("Error: Unable to connect to the database")

def populate_postgres():
    hotel_data = get_generated_data()

    try:
        schema = open('schema.sql','r')
        curr.execute(schema.read())
                    
        curr.executemany("""INSERT INTO hotels VALUES (%(city)s, %(name)s, %(country)s, %(superchain)s, %(cost)s, %(images)s, %(type)s)""", hotel_data)

        conn.commit()

    except:
        print("Error: Unable to create and populate database")
    
    curr.close()
    conn.close()

def get_generated_data():
    with open("hotel-data.json", "r") as hotel_file:
        raw_data = hotel_file.read()
    
    hotel_data = json.loads(raw_data)
    return hotel_data

if __name__ == "__main__":
    populate_postgres()
