import csv
import logging
import json
import utils
from math import sin, cos, radians, atan2, sqrt


def iata_code_to_airport(airports):
    iata_code_map = {}
    for airport in airports:
        iata_code_map[airport["iata_code"]] = airport
    iata_code_map


def calculate_flight_time(*distances):
    totalTime = 0
    for distance in distances:
        totalTime += distance/13.5
        totalTime += 30
    return totalTime


def generate_data():
    airports = utils.load_json("airports.json")
    connection = utils.load_json("connection.json")
    # flights = get_flight_map(airports, connection)
    fligths = utils.load_json("flights.json")

def get_flight_map(airports, connection):
    # connection = get_connection(airports)
    destination_airports = get_destination_aiports(airports)
    # print(len(airports))
    # print(len(destination_airports))
    fligts = set()
    # destination_airports = destination_airports[:1]
    # airports = airports[:1]

    # print(f'connection from {airport["name"]} to {destination["name"]}')
    for destination in destination_airports:
        print(f'{destination["name"]} : {destination["iata_code"]}')
        for airport in airports:
            
            paths = []

            for c1 in connection.get(airport["iata_code"]):
                # found a path directly from airport
                if c1["iata_code"] == destination["iata_code"]:
                    paths.append({"path": [
                        airport["iata_code"], destination["iata_code"]], "duration": calculate_flight_time(c1["distance"])})
                    continue
                for c2 in connection.get(c1["iata_code"]):
                    if c2["iata_code"] == destination["iata_code"] and c1["is_hub"]:
                        paths.append({"path": [
                            airport["iata_code"], c1["iata_code"], destination["iata_code"]], "duration": calculate_flight_time(c1["distance"], c2["distance"])})
                        continue

                    for c3 in connection.get(c2["iata_code"]):
                        # found a 2 stop flight through hubs
                        if c3["iata_code"] == destination["iata_code"] and c1["is_hub"] and c2["is_hub"]:
                            paths.append({"path": [
                                airport["iata_code"], c1["iata_code"], c2["iata_code"], destination["iata_code"]], "duration": calculate_flight_time(c1["distance"], c2["distance"], c3["distance"])})
                            continue

            # for path in paths:
            paths.sort(key=lambda x: x["duration"])

            # print(len(paths))
            
            ps = []
            ps.extend(paths[:2])

            onestop = find_first_stop(paths[2:], 3)
            if onestop is not None:
                ps.append(onestop)
            twostop = find_first_stop(paths[2:], 4)
            if twostop is not None:
                ps.append(twostop)

            for path in ps:
                p = path.get("path")
                for i in range(0, len(p)-1):
                    fligts.add((p[i], p[i+1]))
            # print(json.dumps(ps, indent=2))
    # print(json.dumps(fligts, indent=2))
    print(len(fligts))
    flight_map = {}
    for flight in fligts:
        if flight[0] not in flight_map:
            flight_map[flight[0]] = []
        flight_map[flight[0]].append(flight[1])
    
    utils.write_json_to_file(flight_map, "flights.json")
    return flight_map
    

def find_first_stop(paths, stops):
    for path in paths:
        if len(path.get("path")) == stops:
            return path
    return None


def get_destination_aiports(airports):
    return [airport for airport in airports if airport["is_destination"] == True]


def flight_from_point_to_point(connection, start, finish):
    flights = []


def get_connection(airports):
    connection = {}
    print("generating connection data")
    for i in range(len(airports)):
        start = airports[i]
        connection[start["iata_code"]] = []
        limit = 3000
        if start["is_hub"]:
            limit = 6000
        for j in range(len(airports)):
            current = airports[j]
            if current["is_hub"]:
                limit = 6000
            if start["is_hub"]:
                limit = 9000
            if j == i:
                continue
            if current["is_hub"] or current["is_destination"]:
                distance = distance_between_location(
                    start["latitude"], start["longitude"], current["latitude"], current["longitude"])
                # we found a destination we can go to.

                if distance > 500 and distance < limit:
                    connection[start["iata_code"]].append({
                        "is_hub": current["is_hub"],
                        "iata_code": current["iata_code"],
                        "distance": distance,
                        "type": current["type"]
                    })
    print("done")
    utils.write_json_to_file(connection, "connection.json")
    return connection


def distance_between_location(lat1, lon1, lat2, lon2):
    r = 6371
    phi_1 = radians(lat1)
    phi_2 = radians(lat2)
    del_phi = radians(lat2-lat1)
    del_lambda = radians(lon2-lon1)

    a = sin(del_phi/2) * sin(del_phi/2) + cos(phi_1) * \
        cos(phi_2) * sin(del_lambda / 2) * sin(del_lambda / 2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = r * c
    return distance


def get_airports():
    airport_codes = open("airport-codes.csv", "rt")
    airport_reader = csv.reader(airport_codes, delimiter=',')

    hubs = open("hubs.csv")
    hubs_reader = csv.reader(hubs, delimiter=',')

    destination = open("cities.csv")
    dest_reader = csv.reader(destination, delimiter=",")

    count = 0
    airports = []
    hubs = []
    destinations = []

    countryMap = utils.load_json('country_codes.json')

    for row in hubs_reader:
        hubs.append(row[0])

    for row in dest_reader:
        destinations.append(row[0])

    for row in airport_reader:
        # is of type large_airport or medium_airport
        if row[1] == "large_airport" or row[1] == "medium_airport":
            # has iata_code or gps_code
            if row[8] != "" and row[9] != "":
                airportType = row[1]
                name = row[2]
                country = countryMap[row[5]]
                city = row[7]
                coordinate = row[11]
                latitude = float(coordinate.split(",")[0].strip())
                longitude = float(coordinate.split(",")[1].strip())
                gps_code = row[8]
                iata_code = row[9]
                is_hub = name in hubs
                is_destination = city in destinations
                airport = {
                    "name": name,
                    "is_hub": is_hub,
                    "is_destination": is_destination,
                    "type": airportType,
                    "country": country,
                    "city": city,
                    "latitude": latitude,
                    "longitude": longitude,
                    "gps_code": gps_code,
                    "iata_code": iata_code,
                    "connection": []
                }
                airports.append(airport)
    utils.write_json_to_file(airports, "airports.json")
    return airports


if __name__ == "__main__":
    generate_data()
