import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import json
import os
import utils
import logging


def get_connection():
    try:
        conn = psycopg2.connect(
            user=os.environ["PG_USER"], host=os.environ["PG_HOST"], password=os.environ["PG_PASSWORD"], port="5432")
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

    drop_table(cur, "flights")
    drop_table(cur, "airports")

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

        logging.info("dropping old stored procedures if available")
        cur.execute("drop function flight_two_stop(source_id varchar, layover_one_id varchar, destination_id varchar, departure_time integer, duration decimal, source_cost decimal, source_airlines varchar);")

        logging.info("creating stored procedure for 2 stop flights")
        cur.execute("""
        CREATE or REPLACE function flight_two_stop(source_id varchar, layover_one_id varchar, destination_id varchar,
                                           departure_time integer, duration decimal, source_cost decimal,
                                           source_airlines varchar)
    RETURNS TABLE
            (
                flight2id                  varchar,
                flight3id                  varchar(255),
                source_airport_id_ext      varchar(255),
                layover_one_airport_id     varchar(255),
                layover_two_airport_id     varchar(255),
                destination_airport_id_ext varchar(255),
                totalFlightTime            decimal,
                totalTime                  decimal,
                totalCost                  decimal,
                flight1time                integer,
                flight1duration            decimal,
                flight2time                integer,
                flight2duration            decimal,
                flight3time                integer,
                flight3duration            decimal
            )
as
$$
BEGIN
    RETURN QUERY select flight1.id                                                   as flight2id,
                        flight2.id                                                   as flight3id,
                        source_id                                                    as source_airport_id_ext,
                        layover_one_id                                               as layover_one_airport_id,
                        flight1.destination_airport_id                               as layover_two_airport_id,
                        destination_id                                               as destination_airport_id_ext,
                        duration + flight1.flight_duration + flight2.flight_duration as totalFlightTime,
                        duration + flight1.flight_time - departure_time + flight1.flight_duration +
                        flight2.flight_time - flight1.flight_time +
                        flight2.flight_duration                                      as totalTime,
                        source_cost + flight1.cost + flight2.cost                    as totalCost,
                        departure_time                                               as flight1time,
                        duration                                                     as flight1duration,
                        flight1.flight_time                                          as flight2time,
                        flight1.flight_duration                                      as flight2duration,
                        flight2.flight_time                                          as flight3time,
                        flight2.flight_duration                                      as flight3duration
                 from (select *
                       from flights
                       where flights.source_airport_id = layover_one_id
                         and flights.flight_time >= departure_time + duration) flight1
                          inner join (select *
                                      from flights
                                      where flights.destination_airport_id = destination_airport_id) flight2
                                     on flight1.destination_airport_id = flight2.source_airport_id
                 where flight1.airlines = flight2.airlines
                   and source_airlines = flight1.airlines
                   and flight2.flight_time >= (flight1.flight_time + flight1.flight_duration + 60)
                 order by totalTime
                 limit 10;
END;
$$
    LANGUAGE plpgsql;
        """)

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
