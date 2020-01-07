import csv
import os
import json

car_data = {}

with open ('cars.csv') as csvFile:
  csv_reager = csv.reader(csvFile, delimiter=',')
  for row in csv_reager:
    vehicle_type = "basic"
    if int(row[3]) > 50:
      vehicle_type = "luxury"
    elif int(row[3]) > 30:
      vehicle_type = "premium"
    
    if not car_data.get(vehicle_type):
      car_data[vehicle_type] = {}
    
    if not car_data[vehicle_type].get(row[2]):
      car_data[vehicle_type][row[2]] = []
    
    car_info = {"name": row[0], "image": row[1], "price_multiplier": row[3]}
    car_data[vehicle_type][row[2]].append(car_info)

with open('cars.json', 'w', encoding='utf-8') as f:
  json.dump(car_data, f, ensure_ascii=True, indent=2)
