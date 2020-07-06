import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
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
        logging.warning("Unable to create to the database")
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


def create_postgres_tables():
    conn = get_connection()
    cur = conn.cursor()
    
    drop_table(cur, "cart_items")
    drop_table(cur, "transactions")
    
    try:
        logging.info("creating transactions table")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                CONFIRMATION_ID VARCHAR(32) PRIMARY KEY NOT NULL,
                First_Name VARCHAR(255) NOT NULL,
                Last_Name VARCHAR(255) NOT NULL,
                Email VARCHAR(255),
                Address1 VARCHAR(255) NOT NULL,
                Address2 VARCHAR(255),
                Postal_Code VARCHAR(255) NOT NULL,
                State VARCHAR(255) NOT NULL,
                Country VARCHAR(255) NOT NULL,
                Cost decimal NOT NULL,
                Currency_Code CHAR(3) NOT NULL,
                Time_Stamp TIMESTAMPTZ NOT NULL
            );        
        """)

        logging.info("creating cart_items table")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                CONFIRMATION_ID VARCHAR(32) NOT NULL,
                Type VARCHAR(255) NOT NULL,
                ID VARCHAR(255) NOT NULL,
                Description VARCHAR(255) NOT NULL,
                Cost decimal NOT NULL,
                Currency_Code CHAR(3) NOT NULL,
                Start_Date DATE NOT NULL,
                End_Date DATE NOT NULL,
                FOREIGN KEY (CONFIRMATION_ID) REFERENCES transactions(CONFIRMATION_ID) ON UPDATE CASCADE
            );
        """)

        conn.commit()

    except Exception as e:
        logging.error("Error: Unable to create database")
        logging.error(e)

    logging.info("database created")
    cur.close()
    conn.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    create_postgres_tables()
