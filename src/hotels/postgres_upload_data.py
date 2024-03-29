import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json
import os
import logging
import utils


def get_connection():
    try:
        if "DATABASE_CERT" in os.environ:
            with open("./cert.pem",'w') as cert_file:
                cert_file.write(os.environ["DATABASE_CERT"])
            os.environ["PGSSLROOTCERT"] = "./cert.pem"
            conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port=os.environ["PG_PORT"], sslmode="verify-full", dbname=os.environ["PG_DB"])
        else:
            conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port=os.environ["PG_PORT"])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("CREATE DATABASE beetravels;")
        logging.debug("create beetravels database")
        cur.close()
        conn.close()
    except Exception as e:
        logging.warning("Unable to create to the database")
        logging.info(e)

    try:
        if "DATABASE_CERT" in os.environ:
            conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port=os.environ["PG_PORT"], sslmode="verify-full", database="beetravels")
        else:
            conn = psycopg2.connect(user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port=os.environ["PG_PORT"], database="beetravels")
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
    
    drop_table(cur, "hotels")
    drop_table(cur, "hotel_info")

    try:
        logging.info("creating hotel info DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hotel_info (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                NAME VARCHAR(255) NOT NULL,
                Superchain VARCHAR(255) NOT NULL,
                Type VARCHAR(255) NOT NULL
            );        
        """)
        logging.info("writing to hotel info DB")
        cur.executemany("""
            INSERT INTO hotel_info VALUES (%(id)s, %(name)s, %(superchain)s, %(type)s);
        """, info)

        logging.info("creating hotel DB")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hotels (
                ID VARCHAR(255) PRIMARY KEY NOT NULL,
                HOTEL_ID VARCHAR(255) REFERENCES hotel_info(id),
                City VARCHAR(255) NOT NULL,
                Country VARCHAR(255) NOT NULL,
                Cost decimal NOT NULL,
                Images TEXT [],
                Tags TEXT []
            );
        """)

        logging.info("writing to hotel DB")

        cur.executemany("""
            INSERT INTO hotels VALUES (%(id)s, %(hotel_id)s, %(city)s, %(country)s, %(cost)s, %(images)s, %(tags)s);
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
    hotel_data = utils.load_json("hotel-data.json")
    hotel_info = utils.load_json("hotel-info.json")
    populate_postgres(hotel_data, hotel_info)
