import requests as req
import json

api_url = "https://pixabay.com/api/?key=3332357-97f8d1bfe8d362810421e949d&q=hotel&image_type=photo&per_page=200&safesearch=true&page=3"

# url = "https://pixabay.com/get/57e8d1454857ad14f6da8c7dda79347d163ddde0544c704c722c7bdd954ec55c_1280.jpg"

# filename = url.split("/")[-1]
# print(filename)
response = req.get(api_url)

data = json.loads(response.text)

print(len(data["hits"]))

for image in data["hits"]:
  url = image["largeImageURL"]
  filename = url.split("/")[-1]
  response = req.get(url)
  output = open("hotel-rooms/"+filename, "wb")
  output.write(response.content)
  output.close()

# url = "https://pixabay.com/get/57e8d1454857ad14f6da8c7dda79347d163ddde0544c704c722c7bdd954ec55c_1280.jpg"


# response = req.get(url)

# output = open("hotel-rooms/image.jpg", "wb")
# output.write(response.content)

# output.close()