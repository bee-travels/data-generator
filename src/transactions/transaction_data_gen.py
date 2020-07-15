import utils
import time
import random
import datetime
import urllib.parse
import requests
# import requests_cache  # cache the results
import json

users = utils.load_json("user.json")
destinations = utils.load_json("destination.json")
hotel = "http://localhost:9101/api/v1/hotels"
cars = "http://localhost:9102/api/v1/cars"
# flight = "http://localhost:9103/api/v1/flights"


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
    # print("Randnum: " + str(randnum))
    return randnum


def get_group_size(usual):  # usual: whatever num they usually travel with, 80/20 split
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


def generate_user_hotel(hfull_urlq, priority, party_size, income):
    # print(priority)
    # requests_cache.install_cache('beetravels_cache')
    data = requests.get(hfull_urlq).json()
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
        num1 = hfull_urlq.find("?") + 1
        num2 = hfull_urlq.find("&") + 1
        b_hurlq = hfull_urlq[:num1]
        e_hurlq = hfull_urlq[num2:]
        new = b_hurlq + e_hurlq
        data2 = requests.get(new).json()
        # n2 = new.find("&") + 1
        # e2_hurlq = new[n2:]
        # print(b_hurlq + e2_hurlq)
        if len(data2) != 0:
            if priority == "budget":
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2))
                return s_data[0]
            elif priority == "comfort":
                n = int(len(data2)//2)-1
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                return s_data[n]

            else:
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                return s_data[0]
        else:
            n2 = new.find("&") + 1
            e2_hurlq = new[n2:]
            a_urlq = b_hurlq + e2_hurlq
            data3 = requests.get(a_urlq).json()
            if len(data3) != 0:
                if priority == "budget":
                    lst_data = sorted(data3, key=lambda x: round(float(
                        x["cost"]), 2))  # prices might be 199.99
                    return lst_data[0]
                elif priority == "comfort":
                    nu = int(len(data3)//2)-1
                    lst_data = sorted(
                        data3, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return lst_data[nu]

                else:
                    lst_data = sorted(
                        data3, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                    return lst_data[0]
    print(a_urlq)
    return "\tNo Results -- hotel json generation\n"


#####################FIX SO PARTY SIZE > 4 IS CONSIDERED!!!!#############################


def generate_user_car(cfull_urlq, priority, party_size, income):
    # requests_cache.install_cache('beetravels_cache')
    data = requests.get(cfull_urlq).json()
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
        num1 = cfull_urlq.find("?") + 1
        num2 = cfull_urlq.find("&") + 1
        b_curlq = cfull_urlq[:num1]
        # print(b_curlq)
        e_curlq = cfull_urlq[num2:]
        # print(e_curlq)
        new = b_curlq + e_curlq
        data2 = requests.get(new).json()
        if len(data2) != 0:
            if priority == "budget":
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2))
                return s_data[0]
            elif priority == "comfort":
                n = int(len(data2)//2)-1
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                return s_data[n]
            else:
                s_data = sorted(
                    data2, key=lambda x: round(float(x["cost"]), 2), reverse=True)
            return s_data[0]

        else:
            if party_size <= 4 or priority == "budget":
                n2 = new.find("body_type=")
                if n2 != -1:  # if body_type= is available in the url
                    bsub = new[:n2]
                    substr = new[n2:]
                    n3 = substr.find("&") + 1
                    e_curlq = substr[n3:]
                    newer = bsub+e_curlq
                    data3 = requests.get(newer).json()
                    if len(data3) != 0:
                        if priority == "budget":
                            l_data = sorted(
                                data3, key=lambda x: round(float(x["cost"]), 2))
                            return l_data[0]
                        elif priority == "comfort":
                            n = int(len(data3)//2)-1
                            l_data = sorted(
                                data3, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                            return l_data[n]
                        else:
                            l_data = sorted(
                                data3, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                            return l_data[0]
                    else:
                        n4 = newer.find("style=")
                        b_urlq = newer[:n4]
                        n5 = b_urlq.find("&")+1
                        e_urlq = newer[n5:]
                        n_urlq = b_urlq + e_urlq
                        data4 = requests.get(n_urlq).json()
                        if len(data4) != 0:
                            if priority == "budget":
                                agh_data = sorted(
                                    data4, key=lambda x: round(float(x["cost"]), 2))
                                return agh_data[0]
                            elif priority == "comfort":
                                n = int(len(data4)//2)-1
                                agh_data = sorted(
                                    data4, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                                return agh_data[n]
                            else:
                                agh_data = sorted(
                                    data4, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                                return agh_data[0]
# MISTAKE!!! NEED TO HAVE ELSE FOR N2 != -1 AND ELSE FOR PARTY_SIZE<=4 OR "BUDGET" .. BOTH FOR REMOVING STYLE= FROM THE URL
            else:
                n6 = new.find("style=")
                beg_urlq = new[:n6]
                n7 = b_urlq.find("&")+1
                end_urlq = new[n7:]
                nw_urlq = beg_urlq + end_urlq
                data5 = requests.get(nw_urlq).json()
                if len(data5) != 0:
                    if priority == "comfort":
                        nmmy = int(len(data5)//2)-1
                        dlst = sorted(data5, key=lambda x: round(
                            float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                        return dlst[nmmy]
                    else:
                        dlst = sorted(
                            data5, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                        return dlst[0]
                else:
                    n8 = nw_urlq.find("body_type=")
                    if n8 != -1:  # if body_type= is available in the url
                        besub = nw_urlq[:n8]
                        sbstr = nw_urlq[n8:]
                        n9 = sbstr.find("&") + 1
                        en_curlq = substr[n9:]
                        newest = besub+en_curlq
                        data6 = requests.get(newest).json()
                        if len(data6) != 0:
                            if priority == "comfort":
                                n = int(len(data6)//2)-1
                                another_data = sorted(
                                    data6, key=lambda x: round(float(x["cost"]), 2), reverse=True)  # prices might be 199.99
                                return another_data[n]
                            else:
                                another_data = sorted(
                                    data6, key=lambda x: round(float(x["cost"]), 2), reverse=True)
                                return another_data[0]
    return "\tNo Results -- car json generation\n"
##########################FIX SO PARTY SIZE > 4 IS CONSIDERED!!!!######################################
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------
# ------------------------

#     data = requests.get(cfull_urlq).json()
#     if len(data) != 0:  # if the results do not come back empty
#         if priority == "budget":
#             sorted_data = sorted(data, key=lambda x: float(x["cost"]))
#             return sorted_data[0]
#         elif priority == "comfort":
#             num = int(len(data)//2)-1
#             sorted_data = sorted(
#                 data, key=lambda x: float(x["cost"]), reverse=True)
#             return sorted_data[num]

#         else:
#             sorted_data = sorted(
#                 data, key=lambda x: float(x["cost"]), reverse=True)
#             return sorted_data[0]
#     else:
#         non = cfull_urlq.find("&dateTo")+1
#         num1 = non + len("dateTo=xxxx-xx-xx&")
#         num2 = cfull_urlq[num1:].find("&") + 1
#         # FIX! NEED TO REDO THIS SECTION!
#         b_hurlq = cfull_urlq[:num1]
#         e_hurlq = cfull_urlq[num1:][num2:]
#         print("b_hurlq", b_hurlq)
#         print("e_hurlq", e_hurlq)

#     return
# #         new = b_hurlq + e_hurlq
# #         data2 = requests.get(new).json()
# #         # n2 = new.find("&") + 1
# #         # e2_hurlq = new[n2:]
# #         # print(b_hurlq + e2_hurlq)
# #         if len(data2) != 0:
# #             if priority == "budget":
# #                 s_data = sorted(data2, key=lambda x: float(x["cost"]))
# #                 return s_data[0]
# #             elif priority == "comfort":
# #                 n = int(len(data2)//2)-1
# #                 s_data = sorted(
# #                     data2, key=lambda x: float(x["cost"]), reverse=True)
# #                 return s_data[n]

# #             else:
# #                 s_data = sorted(
# #                     data2, key=lambda x: float(x["cost"]), reverse=True)
# #                 return s_data[0]
# #         else:
# #             #################
# #     elif party_size < 4:
# #         n2 = new.find("&style")
# #         e2_hurlq = new[:n2]
# #         a_urlq = b_hurlq + e2_hurlq
# #         data3 = requests.get(a_urlq).json()
# #         if len(data3) != 0:
# #             if priority == "budget":
# #                 lst_data = sorted(data3, key=lambda x: float(x["cost"]))
# #                 return lst_data[0]
# #             elif priority == "comfort":
# #                 nu = int(len(data3)//2)-1
# #                 lst_data = sorted(
# #                     data3, key=lambda x: float(x["cost"]), reverse=True)
# #                 return lst_data[nu]
# #             else:
# #                 s_data = sorted(
# #                     data2, key=lambda x: float(x["cost"]), reverse=True)
# #                 return s_data[0]
# #         else:

# #         print("large party")

# #         else:
# #             lst_data = sorted(
# #                 data3, key=lambda x: float(x["cost"]), reverse=True)
# #             return lst_data[0]
# #     return "No results"

# this line initiallizes the cache with requests-cache module, prevents calling the API over and over

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


def main():
    for _ in range(30):  # change back to 100
        carloyal = 0
        flightloyal = 0
        total = 0
        for user in users[0:20]:
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
            # body_type, style,

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

            # print(hotel + path_params + query_gen(hotelFilter))
            hfull_urlq = hotel + path_params + query_gen(hotelFilter)
            # print(cars + path_params + query_gen(carFilter))
            cfull_urlq = cars + path_params + query_gen(carFilter)
            oneHotelJson = generate_user_hotel(
                hfull_urlq, priority, party_size, income)
            oneCarJson = generate_user_car(
                cfull_urlq, priority, party_size, income)
            # print(cfull_urlq)
            time.sleep(1)

            # http://localhost:9101/api/v1/hotels/united-states/new-york?dateFrom=2020-07-15&dateTo=2020-07-20&superchain=Nimbus%20Elites
            # "http://localhost:9102/api/v1/cars/united-states/new-york?dateFrom=07-12-2020&dateTo=07-15-2020"

            # destination
            #
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
