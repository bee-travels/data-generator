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
        logging.warning("Error: Unable to create the database")
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

def populate_postgres(data):
    conn = get_connection()
    cur = conn.cursor()

    drop_table(cur, "destination")
    
    try:
        logging.info("creating destination DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS DESTINATION (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                CITY VARCHAR(255) NOT NULL,
                COUNTRY VARCHAR(255) NOT NULL,
                POPULATION INTEGER NOT NULL,
                LATITUDE DECIMAL NOT NULL,
                LONGITUDE DECIMAL NOT NULL,
                DESCRIPTION TEXT NOT NULL,
                Images TEXT []
            );
        """)

        logging.info("writing to destination DB")
        cur.executemany("""
            INSERT INTO DESTINATION VALUES (%(id)s, %(city)s, %(country)s, %(population)s, %(latitude)s, %(longitude)s, %(description)s, %(images)s);
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
    destination_data = utils.load_json("destination.json")
    populate_postgres(destination_data)
