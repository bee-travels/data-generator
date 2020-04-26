import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json
import os
import utils
import logging

def get_connection():
    try:
        conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port="5432")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE beetravels;")
        logging.debug("create beetravels database")
        cur.close()
        conn.close()
    except Exception as e:
        logging.warning("Error: Unable to create to the database")
        logging.info(e)

    try:
        conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"],
                                password=os.environ["PG_PASSWORD"], port="5432", database="beetravels")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        logging.warning("Error: Unable to connect to the database")
        logging.info(e)
        exit(e)


def populate_postgres():
    car_data = utils.load_json("cars.json")
    car_info = utils.load_json("car-info.json")
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        logging.info("creating car info DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CAR_INFO (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                NAME VARCHAR(255) NOT NULL,
                BODY_TYPE VARCHAR(255) NOT NULL,
                STYLE VARCHAR(255) NOT NULL,
                IMAGE VARCHAR(255) NOT NULL
            );        
        """)
        logging.info("writing to car info DB")
        cur.executemany("""
            INSERT INTO car_info VALUES (%(id)s, %(name)s, %(body_type)s, %(style)s, %(image)s);
        """, car_info)

        logging.info("creating car DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS CARS (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                CAR_ID VARCHAR(255) REFERENCES car_info(id),
                CITY VARCHAR(255) NOT NULL,
                COUNTRY VARCHAR(255) NOT NULL,
                RENTAL_COMPANY VARCHAR(255) NOT NULL,
                COST DECIMAL NOT NULL
            );
        """)

        logging.info("writing to car DB")
        cur.executemany("""
            INSERT INTO cars VALUES (%(id)s, %(car_id)s, %(city)s, %(country)s, %(rental_company)s, %(cost)s);
        """, car_data)

        conn.commit()

    except Exception as e:
        print("Error: Unable to create and populate database", e)

    logging.info("data generated")
    cur.close()
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    populate_postgres()
