import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json
import os

def get_connection():
    try:
        conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port="5432")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE beetravels")
        cur.close()
        conn.close()
        conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"],
                                password=os.environ["PG_PASSWORD"], port="5432", database="beetravels")
        # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except:
        exit("Error: Unable to connect to the database")


def populate_postgres():
    hotel_data = load_json("hotel-data.json")
    hotel_info = load_json("hotel-info.json")
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hotel_info (
                ID INTEGER PRIMARY KEY NOT NULL,
                NAME VARCHAR(255) NOT NULL,
                Superchain VARCHAR(255) NOT NULL,
                Type VARCHAR(255) NOT NULL
            );        
        """)

        cur.executemany("""
            INSERT INTO hotel_info VALUES (%(id)s, %(name)s, %(superchain)s, %(type)s);
        """, hotel_info)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS hotels (
                ID INTEGER PRIMARY KEY NOT NULL,
                HOTEL_ID INTEGER REFERENCES hotel_info(id),
                City VARCHAR(255) NOT NULL,
                Country VARCHAR(255) NOT NULL,
                Cost decimal NOT NULL,
                Images TEXT []
            );
        """)

        cur.executemany("""
            INSERT INTO hotels VALUES (%(id)s, %(hotel_id)s, %(city)s, %(country)s, %(cost)s, %(images)s);
        """, hotel_data)

        conn.commit()

    except Exception as e:
        print("Error: Unable to create and populate database", e)

    cur.close()
    conn.close()


def load_json(file_name):
    with open(file_name) as json_data:
        return json.load(json_data)


def get_generated_data():
    with open("hotel-data.json", "r") as hotel_file:
        raw_data = hotel_file.read()

    hotel_data = json.loads(raw_data)
    return hotel_data


if __name__ == "__main__":
    populate_postgres()
