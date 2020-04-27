import csv
import logging
import utils
from math import sin, cos, radians, atan2, sqrt


def generate_data():
    connection = {}
    airports = get_airports()

    for i in range(len(airports)):
        start = airports[i]
        connection[start["iata_code"]] = []
        limit = 3000
        if start["is_hub"]:
            limit = 5000
        for j in range(len(airports)):
            current = airports[j]
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
        
    utils.write_json_to_file(connection, "connection.json")
  

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
