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

def drop_table(cursor, table_name):
    try:
        cursor.execute("""
            DROP TABLE %s;
        """ % table_name)
        logging.info("dropped table "+table_name)
    except Exception as e:
        logging.warning("drop unsuccessful")
        logging.info(e)

def populate_postgres(data, info):
    conn = get_connection()
    cur = conn.cursor()

    drop_table(cur, "airports")
    drop_table(cur, "flights")
    
    try:
        logging.info("creating airports DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS AIRPORTS (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                NAME VARCHAR(255) NOT NULL,
                IS_HUB BOOLEAN NOT NULL,
                IS_DESTINATION BOOLEAN NOT NULL,
                TYPE VARCHAR(63) NOT NULL,
                COUNTRY VARCHAR(255) NOT NULL,
                CITY VARCHAR(255) NOT NULL,
                LATITUDE DECIMAL NOT NULL,
                LONGITUDE DECIMAL NOT NULL,
                GPS_CODE VARCHAR(15) NOT NULL,
                IATA_CODE VARCHAR(15) NOT NULL
            );        
        """)
        logging.info("writing to airports DB")
        cur.executemany("""
            INSERT INTO AIRPORTS VALUES (%(id)s, %(name)s, %(is_hub)s, %(is_destination)s, %(type)s, %(country)s, %(city)s, %(latitude)s, %(longitude)s, %(gps_code)s, %(iata_code)s);
        """, info)


        logging.info("creating Flights DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS FLIGHTS (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                SOURCE_AIRPORT_ID VARCHAR(255) REFERENCES AIRPORTS(id),
                DESTINATION_AIRPORT_ID VARCHAR(255) REFERENCES AIRPORTS(id),
                FLIGHT_TIME INTEGER NOT NULL,
                FLIGHT_DURATION DECIMAL NOT NULL,
                COST DECIMAL NOT NULL,
                AIRLINES VARCHAR(255) NOT NULL
            );
        """)

        logging.info("writing to Flights DB")
        cur.executemany("""
            INSERT INTO FLIGHTS VALUES (%(id)s, %(source_airport_id)s, %(destination_airport_id)s, %(flight_time)s, %(flight_duration)s, %(cost)s, %(airlines)s);
        """, data)

        conn.commit()

    except Exception as e:
        logging.error("Error: Unable to create and populate database")
        logging.error(e)

    logging.info("data generated")
    cur.close()
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    flights = utils.load_json("flight_data.json")
    airports = utils.load_json("airports.json")
    populate_postgres(flights, airports)
