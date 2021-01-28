from gremlin_python import statics
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import Cardinality
from gremlin_python.process.traversal import Column
from gremlin_python.process.traversal import Direction
from gremlin_python.process.traversal import Operator
from gremlin_python.process.traversal import P
from gremlin_python.process.traversal import Pop
from gremlin_python.process.traversal import Scope
from gremlin_python.process.traversal import Barrier
from gremlin_python.process.traversal import Bindings
from gremlin_python.process.traversal import WithOptions
import sys
import json
import os
import utils
import logging


def get_connection():
    try:
        g = traversal().withRemote(DriverRemoteConnection(os.environ["JANUS_HOST"], "g"))
        return g
    except Exception as e:
        logging.warning("Error: Unable to connect to the database")
        logging.info(e)
        exit(e)


def drop_graph(g):
    try:
        g.V().drop()
        logging.info("dropped graph")
    except Exception as e:
        logging.warning("drop unsuccessful")
        logging.info(e)


def populate_janus(flights, airports):
    g = get_connection()

    airport_vertices = {}

    drop_graph(g)

    try:
        logging.info("creating airport vertices")

        for airport in airports:
            airport_vertex = g.addV("airport").property(
                "id", airport["id"]
            ).property(
                "name", airport["name"]
            ).property(
                "is_hub", airport["is_hub"]
            ).property(
                "is_destination", airport["is_destination"]
            ).property(
                "type", airport["type"]
            ).property(
                "country", airport["country"]
            ).property(
                "city", airport["city"]
            ).property(
                "latitude", airport["latitude"]
            ).property(
                "longitude", airport["longitude"]
            ).property(
                "gps_code", airport["gps_code"]
            ).property(
                "iata_code", airport["iata_code"]
            ).next()

            airport_vertices[airport["id"]] = airport_vertex

        logging.info("creating flight vertices")

        for flight in flights:
            flight_vertex = g.addV("flight").property(
                "id", flight["id"]
            ).property(
                "source_airport_id", flight["source_airport_id"]
            ).property(
                "destination_airport_id", flight["destination_airport_id"]
            ).property(
                "flight_time", flight["flight_time"]
            ).property(
                "flight_duration", flight["flight_duration"]
            ).property(
                "cost", flight["cost"]
            ).property(
                "airlines", flight["airlines"]
            ).next()

            g.addE("departing").from_(flight_vertex).to(airport_vertices[flight["source_airport_id"]]).iterate()
            g.addE("arriving").from_(flight_vertex).to(airport_vertices[flight["destination_airport_id"]]).iterate()

    except Exception as e:
        logging.error("Error: Unable to create and populate database")
        logging.error(e)

    logging.info("data generated")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    flights = utils.load_json("flight_data.json")
    airports = utils.load_json("airports.json")
    populate_janus(flights, airports)
