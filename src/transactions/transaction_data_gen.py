import utils
import time
import random
import datetime
from urllib.parse import urlparse, parse_qsl, urlencode
import requests
# use postgres, put results in database. Send everything to checkout service which will automatically put it into the checkout service
import json
import os

users = utils.load_json("user.json")
destinations = utils.load_json("destination.json")
hotel = "http://169.63.175.87:32461/api/v1/hotels"
cars = "http://169.63.175.87:30505/api/v1/cars"
# flight = "http://localhost:9103/api/v2/flights"


def get_reason(reason):
    chance = random.randint(0, 100)
    if chance > 85:
        return random.choice(["business", "leisure", "family"])

    return reason


def get_carhotel_loyalty_status(priority, main_reason, frequency, randnum):
    val = 1
    if priority == "comfort":
        val = val * 7
    elif priority == "luxury":
        val = val * 6
    elif priority == "time":
        val = val * 5
    else:
        val = val * 4

    if frequency >= 24:
        val = val * 7
    elif (frequency < 24 and frequency >= 12):
        val = val * 6
    else:
        val = val * 4

    if main_reason == "business":
        val = val * 8
    elif main_reason == "family":
        val = val*4
    else:
        val = val * 6

    if val > randnum:
        return True

    return False


def get_flight_loyalty_status(priority, main_reason, frequency, randnum):
    val = 1
    if priority == "comfort":
        val = val * 8
    elif priority == "luxury":
        val = val * 6
    elif priority == "time":
        val = val * 3
    else:
        val = val * 4

    if frequency >= 24:
        val = val * 8
    elif (frequency < 24 and frequency >= 12):
        val = val * 6
    else:
        val = val * 4

    if main_reason == "business":
        val = val * 5
    elif main_reason == "family":
        val = val * 4
    else:
        val = val * 6

    if val > randnum:
        return True

    return False


def get_random_num():
    randnum = float(random.randint(0, 100))/100.0
    return randnum


def get_group_size(usual):  # usual: whatever num they usually travel with, 80/20 split chance
    rand = random.randint(0, 100)
    if rand > 80:
        return random.randint(1, 6)
    return usual


def get_travel_day_offset(reason, priority):
    chance = random.randint(0, 100)
    if reason == "business":
        if chance < 60:
            return random.randint(1, 14)
        elif chance < 90:
            return random.randint(15, 24)
        else:
            return random.randint(25, 30)
    else:
        if priority == "budget":
            return random.randint(30, 60)
        else:
            return random.randint(15, 50)

        # more likely to be leisure if (1. leaving 20-60 days in advanced (2. also 2 people or more
        # if traveling 1-19 days in advance, 15% chance of being leisure. if also income > 200,000 then only 10% chance of leisure
        # if traveling 20-30 days in advance and 1 person, only 40% chance of being leisure
        # if traveling 20-30 days in advance and 2-3 people, 60% chance of being leisure
        # if traveling 20-30 days in advance and 4 or more people, 90% chance of being leisure
        # if traveling 30-60 days in advanced, 85% chance of leisure


def get_travel_duration(reason, priority):  # generate date based on reason
    timed = 0
    if reason == "business":  # I could also do 80% of the time select 1-7
        if priority == "time":
            timed = random.choice([1, 1, 2, 2, 2, 3, 3, 3, 4, 5, 6, 7])
        else:
            timed = random.choice(
                [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9, 10])
    else:
        if priority != "budget":
            timed = random.choice([2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 8, 8,
                                   8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 11, 12, 13, 14, 14, 15, 16, 16, 16, 17, 18])
        else:
            timed = random.choice(
                [2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 8, 9, 10, 12, 13, 14])
    return timed


def query_gen(query):
    q = ""
    for key, val in query.items():
        if q != "":
            q = q + "&"
        else:
            q = "?"
        q = q + key + "=" + val.replace(" ", "%20")
    return q


def kebab_case(val):
    return val.lower().replace(" ", "-")


def get_destination(usual, destinations):  # list of frequenty traveled locaitons
    chance = random.randint(0, 100)
    if chance > 80:
        return random.choice(destinations)
    return random.choice(usual)


def convert_tuplelist_to_dict(query_tuple):
    result_dict = {}
    for k, v in query_tuple:
        result_dict[k] = v
    return result_dict


def delete_dict_key(dictionary, key):
    if key in dictionary:
        dictionary.pop(key)


def generate_user_hotel(hotel_full_url, priority, party_size):
    # print("\thotel_full_url: ", hotel_full_url)
    try:
        data = requests.get(hotel_full_url).json()
        if type(data) == list:
            if len(data) != 0:  # if the results do not come back empty
                if priority == "budget":
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2))
                    return sorted_data[0]
                elif priority == "comfort":
                    num = int(len(data)//2)-1
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return sorted_data[num]

                else:
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return sorted_data[0]
            else:
                parse_url = urlparse(hotel_full_url)
                #print("parse_url: ", parse_url)
                query_tuple = parse_qsl(parse_url.query)

                #print("\tquery_dict", convert_tuplelist_to_dict(query_tuple))
                query_dict = convert_tuplelist_to_dict(query_tuple)
                if "superchain" in query_dict:
                    #print("removing superchain...")
                    delete_dict_key(query_dict, "superchain")
                elif "type" in query_dict:
                    #print("removing type...")
                    delete_dict_key(query_dict, "type")
                else:
                    return "\tNo Results -- hotel json generation\n"
                new_hotel_url = parse_url.scheme + "://" + \
                    parse_url.netloc + parse_url.path + query_gen(query_dict)
                return generate_user_hotel(new_hotel_url, priority, party_size)
        else:
            return "\tNo Results -- hotel json generation\n"
    except:
        time.sleep(10)
        print("EXCEPTION HOTEL")
        return "\tNo Results -- car json generation"
        # http: // localhost: 9101/api/v1/hotels/indonesia/jakarta?superchain = Urban % 20Lifestyle & type = luxury & dateFrom = 2020-08-03 & dateTo = 2020-08-08


def generate_user_car(car_full_url, priority, party_size):
    try:
        data = requests.get(car_full_url).json()
        if type(data) == list:
            if len(data) != 0:  # if the results do not come back empty
                # http://localhost:9102/api/v1/cars/mexico/mexico-city?rental_company=Carlux&style=luxury&dateFrom=2020-07-25&dateTo=2020-07-26
                if priority == "budget":
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2))
                    return sorted_data[0]
                elif priority == "comfort":
                    num = int(len(data)//2)-1
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return sorted_data[num]

                else:  # if results do not come back empty AND budget/time
                    sorted_data = sorted(
                        data, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return sorted_data[0]
            else:  # first get request returns empty response, remove loyalty program parameter
                parse_url = urlparse(car_full_url)
                #print("parse_url: ", parse_url)
                query_tuple = parse_qsl(parse_url.query)
                #print("\tquery_dict", convert_tuplelist_to_dict(query_tuple))
                query_dict = convert_tuplelist_to_dict(query_tuple)
                if "rental_company" in query_dict:
                    #print("removing rental company...")
                    delete_dict_key(query_dict, "rental_company")
                elif party_size > 4 and priority != "budget" and "style" in query_dict:
                    #print("removing style for large party...")
                    delete_dict_key(query_dict, "style")
                elif "body_type" in query_dict:
                    #print("removing body_type...")
                    delete_dict_key(query_dict, "body_type")
                elif (party_size <= 4 or priority == "budget") and ("style" in query_dict):
                    #print("removing style for small party or budget users...")
                    delete_dict_key(query_dict, "body_type")
                else:
                    return "\tNo Results -- hotel json generation\n"
                new_hotel_url = parse_url.scheme + "://" + \
                    parse_url.netloc + parse_url.path + query_gen(query_dict)
                return generate_user_hotel(new_hotel_url, priority, party_size)
        else:
            return "\tNo Results -- car json generation\n"
    except:
        time.sleep(10)
        print("EXCEPTION CAR")
        return "\tNo Results -- car json generation"


# 1 luxury
#    # if no results remove rental_company=... before the first &
#    # if still no results, remove body_type if party size < 4 and if not then remove style
#    # if still no results, remove style
# 2 budget
#    # if no results remove rental_company=... before the first &
#    # if still no results, remove body_type if party size < 4 and if not then remove style
#    # if still no results, remove style
# 3 comfort
#    # if no results remove rental_company=... before the first &
#    # if still no results, remove body_type if party size < 4 and if not then remove style
#    # if still no results, remove style


def format_postgres(one_user_dict, hotel_full_url, car_full_url, priority, party_size):
    string = ""
    date_today = datetime.datetime.now()
    time_stamp = date_today.isoformat()
    initialized_dict = {"totalAmount": 0.00, "time_stamp": time_stamp, "currency": "USD", "status": "unprocessed", "cartItems": [{}], "billingDetails": {
    }, "paymentMethodDetails": {"type": "Card", "creditcardNumber": "0000 0000 0000 0000", "expMonth": 1, "expYear": 2050, "cvc": "0000"}}
    if "cars" in car_full_url:  # for the future in case we provide a blank string when people do not purchase hotel and car at same time
        carjson = generate_user_car(car_full_url, priority, party_size)
        if (type(carjson) is dict) and ("error" not in carjson):
            initialized_dict["cartItems"][0]["type"] = "Car"
            cartItemsCar_dict = initialized_dict["cartItems"][0]
            cartItemsCar_dict['uuid'] = carjson['id']
            cartItemsCar_dict["description"] = "description"
            cartItemsCar_dict["cost"] = carjson["cost"]
            cartItemsCar_dict["currency"] = "USD"
            dateTo = car_full_url.split(
                "&")[-1].split("=")[1].replace("-", " ")
            yearTo, monthTo, dayTo = dateTo.split(" ")
            string = monthTo + "-" + dayTo + "-" + yearTo
            cartItemsCar_dict["endDate"] = string
            dateFrom = car_full_url.split(
                "&")[-2].split("=")[1].replace("-", " ")
            yearFrom, monthFrom, dayFrom = dateFrom.split(" ")
            string = monthFrom + "-" + dayFrom + "-" + yearFrom
            cartItemsCar_dict["startDate"] = string
            billingDetails = initialized_dict["billingDetails"]
            # CAN WE ASSUME NAMES ARE ALWAYS JUST 2 WORDS???)
            billingDetails["firstName"] = one_user_dict["name"].split(" ")[0]
            billingDetails["lastName"] = one_user_dict["name"].split(" ")[-1]
            billingDetails["address"] = {}
            billingDetails["address"]["line1"] = "00 Non"
            billingDetails["address"]["city"] = one_user_dict["city"]
            billingDetails["address"]["postalCode"] = "00000"
            billingDetails["address"]["state"] = "Non"
            billingDetails["address"]["country"] = one_user_dict["country"]

    if "hotels" in hotel_full_url:  # set up so a user does not need to purchase both a hotel and car
        hoteljson = generate_user_hotel(hotel_full_url, priority, party_size)
        if (type(hoteljson) == dict) and ("error" not in hoteljson):
            initialized_dict["cartItems"].append({})
            initialized_dict["cartItems"][1]["type"] = "Hotel"
            cartItemsHotel_dict = initialized_dict["cartItems"][1]
            cartItemsHotel_dict['uuid'] = hoteljson["id"]
            cartItemsHotel_dict['description'] = "description"
            cartItemsHotel_dict["currency"] = "USD"
            cartItemsHotel_dict['cost'] = hoteljson["cost"]
            dateTo_hotel = car_full_url.split(
                "&")[-1].split("=")[1].replace("-", " ")
            yearTo, monthTo, dayTo = dateTo_hotel.split(" ")
            string = monthTo + "-" + dayTo + "-" + yearTo
            cartItemsHotel_dict["endDate"] = string
            dateFrom_hotel = car_full_url.split(
                "&")[-2].split("=")[1].replace("-", " ")
            yearFrom, monthFrom, dayFrom = dateFrom_hotel.split(" ")
            string = monthFrom + "-" + dayFrom + "-" + yearFrom
            cartItemsHotel_dict["startDate"] = string

        try:
            initialized_dict["totalAmount"] += initialized_dict["cartItems"][0]["cost"] + \
                initialized_dict["cartItems"][1]["cost"]
            # print(initialized_dict)
            return initialized_dict

        except:
            return "Error"
    return "Error"


def posting(params):
    # set dynamic environment var that is sent in
    base_url = 'http://localhost:9402' if "CHECK_OUT_URL" not in os.environ else os.environ["CHECK_OUT_URL"]
    response = requests.post(base_url+'/api/v1/checkout/cart', json=params)

    # terminal with export CHECK_OUT_URL= http:// xxxxx. Default to local host port you are using if no envir variable
    # is provided


def main():
    counter = 0
    result = []
    for _ in range(10000):  # change back to 100
        total = 0
        for user in users:
            get = user.get
            willTravel = random.randint(0, 100)
            if willTravel > get("travel_frequency"):
                continue
            # print((willTravel, get("travel_frequency")))
            total = total + 1
            priority = user["priority"]
            main_reason = user["main_reason_for_travel"]
            reason = get_reason(main_reason)
            frequency = user["travel_frequency"]
            income = user["income"]

            randnum = random.randint(96, 192)
            carLoyal = get_carhotel_loyalty_status(
                priority, main_reason, frequency, randnum)
            hotelLoyal = get_carhotel_loyalty_status(
                priority, main_reason, frequency, randnum)
            flightLoyal = get_flight_loyalty_status(
                priority, main_reason, frequency, randnum)
            carFilter = {}
            flightFilter = {}
            hotelFilter = {}
            party_size = get_group_size(get("party_size"))

            if carLoyal:
                carFilter["rental_company"] = user["car_rental_loyalty"]
            if priority != 'budget' and party_size > 4:
                carFilter["body_type"] = "suv"
            # body_type, style

            if priority == "budget":
                carFilter["style"] = "basic"
            elif priority == "comfort":
                carFilter["style"] = "premium"
            else:
                carFilter["style"] = "luxury"

            if hotelLoyal:
                hotelFilter = {"superchain": user["hotel_chain_loyalty"]}

            if priority == "budget":
                hotelFilter["type"] = "budget"
            elif priority == "comfort":
                hotelFilter["type"] = "comfort"
            else:
                hotelFilter["type"] = "luxury"

            if flightLoyal:
                flightFilter = {"airlines": user["airlines_loyalty"]}

            destination = get_destination(
                get("frequently_visited_cities"), destinations)
            offset = get_travel_day_offset(reason, priority)
            duration = get_travel_duration(reason, priority)
            dateFrom = datetime.date.today() + datetime.timedelta(days=offset)
            dateTo = dateFrom + datetime.timedelta(days=duration)

            hotelFilter["dateFrom"] = str(dateFrom)
            hotelFilter["dateTo"] = str(dateTo)

            carFilter["dateFrom"] = str(dateFrom)
            carFilter["dateTo"] = str(dateTo)

            path_params = "/" + \
                kebab_case(destination["country"]) + \
                "/" + kebab_case(destination["city"])

            hotel_full_url = hotel + path_params + query_gen(hotelFilter)
            # HOTEL_FULL_URL: http://localhost:9101/api/v1/hotels/romania/bucharest?superchain=Nimbus%20Elites&type=luxury&dateFrom=2020-07-29&dateTo=2020-07-31

            car_full_url = cars + path_params + query_gen(carFilter)
            # CAR_FULL_URL: http://localhost:9102/api/v1/cars/turkey/istanbul?rental_company=Capsule&style=luxury&dateFrom=2020-08-27&dateTo=2020-09-04
            postgres = format_postgres(
                user, hotel_full_url, car_full_url, priority, party_size)
            # POSTGRES SETS DATA INTO READABLE FORMAT FOR THE POSTGRES DATABASE
            result.append(postgres)
            # posting(postgres)
            # POSTS TO POSTGRES DATABASE
        counter += 1
        if counter == 1:
            print("iteration: 1")
        if counter % 100 == 0:
            print("iteration: ", counter)
    utils.write_json_to_file(result, "transactions.json")
    # date depending on reason -> 3 - 30 days for business, 20 - 60 for leisure
###########################Generation################################################
    # business: 65% of time traveling 1-19 days in advanced,
    # ^^^5/9 of time is 1 person
    # so, 13% of time 20-30 days in advance with 1 person
    # 11% of time 20-30 days in advanced with 2-3 people
    # 5% of the time 20-30 days in advanced with 4 or more people
    # 6% of the time 30-60 days in advanced

    # leisure: 35% of time traveling 1-19 days in advanced
    #
# Extra criteria for leisure:
# if traveling more than 1 week then leisure
#####################################################################################


#########################Recommendation################################################
    # buisness:
    # --> will choose recommendation based on what most business people choose. Based on income >200000, will choose the fastest option for
    # for inbetween, randomly select OR choose middle priced options
    # flights and most expensive option for time/luxury.. For budget (<100000), choose least expensive recommendations

    # business tags for hotel/car:

    # more likely to be buisness if traveling with (1. leaving within 3-30 days in advance (2. also, 1 person
    # if traveling 1-19 days in advanced, 85% chance business.
    #           unless income > 200,000, 90% chance of being time (time is a rich business man); select highest price
    # if traveling 20-30 days in advanced 60% chance business and 1 person
    #           income > 200,000, 60% chance of being time (time is a rich business man)
    # elif traveling 20-30 days in advanced 40% chance business and 2-3 people
    #           income > 200,000, still 40% chance of being time (time is a rich business man)
    # elif traveling 20-30 days in advanced 10% chance business and 4 or more people
    #           income > 200,000, still 40% chance of being time (time is a rich business man)
    # if traveling 30-60 days in advanced, 15% chance of business

    # leisure:
    # --> will choose recommendation based on what most leisure people choose. Based on income >200000, will choose the luxury option
    # for inbetween, randomly select OR choose middle priced options
    # For budget (<100000), choose least expensive recommendations

    # more likely to be leisure if (1. leaving 20-60 days in advanced (2. also 2 people or more
    # if traveling 1-19 days in advance, 15% chance of being leisure. if also income > 200,000 then only 10% chance of leisure
    # if traveling 20-30 days in advance and 1 person, only 40% chance of being leisure
    # if traveling 20-30 days in advance and 2-3 people, 60% chance of being leisure
    # if traveling 20-30 days in advance and 4 or more people, 90% chance of being leisure
    # if traveling 30-60 days in advanced, 85% chance of leisure

    # time
    # leave also 7-14 days in advanced with high income > 200000: will select highest priced hotel within a 2 week timeline.
    #    Will select the shortest duration flight, then most expensive
    # luxury
    # leave 30-60 days in
    # budget
    # will select cheapest

    # using same randnum for each selection
    # carRatio = (float(carloyal) / total) * 100.0
    # flightRatio = (float(flightloyal) / total) * 100.0

    # print("Car Ratio: ", carRatio)
    # print("Flight Ratio: ", flightRatio)
    # print()

main()

# for time look at the income for the type they are looking at

##############Loyalty Rules#####################
# hotel and car
# priority:
# comfort
# least frequent (baseline): 0.45
# luxury
# least frequent (baseline): 0.4
# time
# least frequent (baseline): 0.35
# budget
# least frequent (baseline): 0.3
# frequency weight: 2x, 1.5x, 1x

# comfort = 8
# luxury = 6
# time = 5
# budget = 4

# frequent = 8
# moderate = 6
# infrequet = 4

# business = 8
# leisure = 6
# family = 4

# 256
# 64

# randomnum
# the highest range 72 and lowest is 18, so 36 is inbetween for a scorecomparison

# -----------------------------------------------------------
# flight
# priority:
# comfort
# least frequent (baseline): 0.45
# luxury
# least frequent (baseline): 0.4
# time
# least frequent (baseline): 0.15
# budget
# least frequent (baseline): 0.3
# frequency weight: 2x, 1.5x, 1.5x, 1x

# threshold, random number to compare with threshold
