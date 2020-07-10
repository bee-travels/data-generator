# # 100 users
# # start 100 timerTask
# from threading import Timer
# import atexit

# class Repeat(object):

#     count = 0
#     @staticmethod
#     def repeat(rep, delay, func):
#         "repeat func rep times with a delay given in seconds"

#         if Repeat.count < rep:
#             # call func, you might want to add args here
#             func()
#             Repeat.count += 1
#             # setup a timer which calls repeat recursively
#             # again, if you need args for func, you have to add them here
#             timer = Timer(delay, Repeat.repeat, (rep, delay, func))
#             # register timer.cancel to stop the timer when you exit the interpreter
#             atexit.register(timer.cancel)
#             timer.start()


#   {
#     "name": "Kyle Mendoza",
#     "income": 508662,
#     "address": "24254 Kirby Villages Suite 395\nEast Ronaldburgh, PA 76524",
#     "car_rental_loyalty": "Rentio",
#     "hotel_chain_loyalty": "Elegant Enigma Alliance",
#     "airlines_loyalty": "Phoenix Airlines",
#     "travel_frequency": 23,
#     "priority": "luxury",
#     "marital_status": "married",
#     "party_size": 4,
#     "main_reason_for_travel": "family"
#   },

# {
#     "name": "Raymond Smith",
#     "income": 116670,
#     "address": "460 Kyle Roads Suite 638\nHubermouth, KS 79286",
#     "car_rental_loyalty": "Capsule",
#     "hotel_chain_loyalty": "Urban Lifestyle",
#     "airlines_loyalty": "MilkyWay Airlanes",
#     "travel_frequency": 2,
#     "priority": "comfort",
#     "marital_status": "married",
#     "party_size": 2,
#     "main_reason_for_travel": "leisure"
#   },

import utils
import time
import random

users = utils.load_json("user.json")

# while True:

# for user in users:
#     get = user.get
#     willTravel = random.randint(0,100)
#     if willTravel > get("travel_frequency"):
#         continue
#     # print((willTravel, get("travel_frequency")))
#     print(get("name"))

#     priority = get("priority")
#     if priority == "luxury":

#     elif priority == "comfort":

#     elif priority == "budget":

#     else:

# def get_car_loyalty_status(priority, main_reason, frequency, randnum): 
#         #Car
#     if randnum > 0.7:
#         if frequency<12 and priority == 'budget':
#             return True
#     elif randnum > 0.5:
#         if (frequency<24 and frequency>=12) and priority =='budget':
#             return True
#         elif frequency<12 and (priority == 'luxury' or priority =='comfort'):
#             return True 
#     elif randnum > 0.4:
#         if (frequency<24 and frequency>=12) and priority =='luxury':
#             return True
#     elif randnum > 0.3:
#         if priority == 'time':
#             return True
#         elif frequency >=24 and priority == 'luxury':
#             return True
#         elif (frequency<24 and frequency>=12) and priority =='comfort':
#             return True 
#         elif frequency >=24 and priority == 'comfort':
#             return True
#     return False


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


    if frequency >=24:
        val = val * 7
    elif (frequency < 24 and frequency >=12):
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


    if frequency >=24:
        val = val * 8
    elif (frequency < 24 and frequency >=12):
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
    randnum = float(random.randint(0,100))/100.0
    # print("Randnum: " + str(randnum))
    return randnum

        

def main():
    for _ in range(100):
        carloyal = 0
        flightloyal = 0
        total = 0
        for user in users:
            get = user.get
            willTravel = random.randint(0,100)
            if willTravel > get("travel_frequency"):
                continue
            # print((willTravel, get("travel_frequency")))
            total = total + 1
            priority = user["priority"]
            main_reason = user["main_reason_for_travel"]
            frequency = user["travel_frequency"]
            # print("frequency:: " +str(frequency))
            # print("priority:: " + priority)
            randnum= random.randint(96, 192)
            carLoyal = get_carhotel_loyalty_status(priority, main_reason, frequency, randnum)
            flightLoyal = get_flight_loyalty_status(priority, main_reason, frequency, randnum)
            carFilter = {"rental_company": user["car_rental_loyalty"]}
            flightFilter = {"airlines": user["airlines_loyalty"]}
            if carLoyal:
                carFilter = {"rental_company": user["car_rental_loyalty"]}
            if flightLoyal:
                flightFilter = {"airlines": user["airlines_loyalty"]}

            # destination
            # 
            # date depending on reason -> 3 - 30 days for business, 20 - 60 for leisure

        ####buisness:
        # more likely to be buisness if traveling with 1. leaving within 3-30 days in advance 2. also, 1 person 
        ######leisuire:
        # more likely to be leisure if 1. leaving 20-60 days in advanced 2. also 2 people or more
        # Will select the  
        #######time
        #leave also 7-14 days in advanced with high income > 200000: will select highest priced hotel within a 2 week timeline.
        #    Will select the shortest duration flight, then most expensive
        #######luxury
        #leave 30-60 days in
        #######budget
        #will select cheapest



        #using same randnum for each selection
        # carRatio = (float(carloyal) / total) * 100.0
        # flightRatio = (float(flightloyal) / total) * 100.0

        # print("Car Ratio: ", carRatio)
        # print("Flight Ratio: ", flightRatio)
        # print()
        
main()

##for time look at the income for the type they are looking at

##############Loyalty Rules#####################
##hotel and car
#priority:
###comfort
#least frequent (baseline): 0.45
###luxury
#least frequent (baseline): 0.4
###time
#least frequent (baseline): 0.35
###budget
#least frequent (baseline): 0.3
#######frequency weight: 2x, 1.5x, 1x

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
#the highest range 72 and lowest is 18, so 36 is inbetween for a scorecomparison

#-----------------------------------------------------------
##flight
#priority:
###comfort
#least frequent (baseline): 0.45
###luxury
#least frequent (baseline): 0.4
###time
#least frequent (baseline): 0.15
###budget
#least frequent (baseline): 0.3
#######frequency weight: 2x, 1.5x, 1.5x, 1x

#threshold, random number to compare with threshold