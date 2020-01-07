import csv
import requests as req
import json
import os

api_url = "https://pixabay.com/api/?key=3332357-97f8d1bfe8d362810421e949d&q={}&image_type=photo&per_page=20&safesearch=true"

with open('cities.csv', 'rt') as csvfile:
  reader = csv.reader(csvfile, delimiter=',')

  for row in reader:
    print(row[0], row[3])

    response = req.get(api_url.format(row[0]))
    data = json.loads(response.text)

    folder_name = "{}-{}".format("-".join(row[0].split(' ')), "-".join(row[3].split(' '))) 
    os.mkdir(folder_name)

    if len(data["hits"]) < 5:
      print("Did not find enough images for {}, searching for {} instead".format(row[0], row[3]))
      response = req.get(api_url.format(row[3]))
      data = json.loads(response.text)

    for image in data["hits"]:
      url = image["largeImageURL"]
      filename = url.split("/")[-1]
      response = req.get(url)
      output = open(folder_name+"/"+filename, "wb")
      output.write(response.content)
      output.close()