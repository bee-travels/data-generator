import utils
import datetime



def array_to_id_map(items):
    res = {}
    for item in items:
        res[item["id"]] = item
    return res

def travel_group_by_days(days):
    if days < 3:
        return 1
    elif days < 7:
        return 2
    elif days < 15:
        return 3
    elif days < 30:
        return 4
    else:
        return 5

def kebab_case(input):
    return "-".join(input.lower().split(" "))

def process_transaction(transactions, hotel_map, car_map):
    hotels = []
    cars = []
    for transaction in transactions:
        if type(transaction) is str:
            continue
        booking_time = datetime.datetime.strptime(transaction.get("time_stamp"), '%Y-%m-%dT%H:%M:%S.%f')



        for cart_item in transaction.get("cartItems"):
            if cart_item["type"] == "Car":
                travel_time = datetime.datetime.strptime(cart_item.get("startDate"), "%m %d %Y")
                traveing_in_days = abs((travel_time - booking_time).days)
                group = travel_group_by_days(traveing_in_days)
                car = car_map[cart_item["uuid"]]
                city = car["city"]
                country = car["country"]
                id = kebab_case(city)+"-"+kebab_case(country)
                rental_company = car["rental_company"]
                body_type = car["body_type"]
                style = car["style"]
                data = {
                    "id": id,
                    "group": group,
                    kebab_case("Rent Pad"): 1 if rental_company == "Rent Pad" else 0,
                    kebab_case("Capsule"): 1 if rental_company == "Capsule" else 0,
                    kebab_case("Rentio"): 1 if rental_company == "Rentio" else 0,
                    kebab_case("Chakra"): 1 if rental_company == "Chakra" else 0,
                    kebab_case("Carlux"): 1 if rental_company == "Carlux" else 0,
                    "sedan": 1 if body_type == "sedan" else 0,
                    "suv": 1 if body_type == "suv" else 0,
                    "hatchback": 1 if body_type == "hatchback" else 0,
                    "muscle": 1 if body_type == "muscle" else 0,
                    "crossover": 1 if body_type == "crossover" else 0,
                    "convertible": 1 if body_type == "convertible" else 0,
                    "sports": 1 if body_type == "sports" else 0,
                    "basic": 1 if style == "basic" else 0,
                    "premium": 1 if style == "premium" else 0,
                    "luxury": 1 if style == "luxury" else 0
                }
                cars.append(data)
            else:
                travel_time = datetime.datetime.strptime(cart_item["startDate"], "%m %d %Y")
                traveing_in_days = abs((travel_time - booking_time).days)
                group = travel_group_by_days(traveing_in_days)
                hotel = hotel_map[cart_item["uuid"]]
                city = hotel["city"]
                country = hotel["country"]
                id = kebab_case(city)+"-"+kebab_case(country)
                superchain = hotel["superchain"]
                style = hotel["type"]
                data = {
                    "id": id,
                    "group": group,
                    kebab_case("Nimbus Elites"): 1 if superchain == "Nimbus Elites" else 0,
                    kebab_case("Elegant Enigma Alliance"): 1 if superchain == "Elegant Enigma Alliance" else 0,
                    kebab_case("Urban Lifestyle"): 1 if superchain == "Urban Lifestyle" else 0,
                    "budget": 1 if style == "budget" else 0,
                    "comfort": 1 if style == "comfort" else 0,
                    "luxury": 1 if style == "luxury" else 0
                }
                hotels.append(data)
    
    utils.write_csv_to_file("cars_recommender.csv", cars, cars[0].keys())
    utils.write_csv_to_file("hotels_recommender.csv", hotels, hotels[0].keys())
        

def main():
    hotels = utils.load_json("hotel-data.json")
    cars = utils.load_json("cars.json")
    transactions = utils.load_json("minify.json")


    hotel_map = array_to_id_map(hotels)
    car_map = array_to_id_map(cars)
    process_transaction(transactions, hotel_map, car_map)

if __name__ == "__main__":
    main()