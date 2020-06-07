import urllib.request
import json
import os

api_endpoint = "http://api.openweathermap.org/data/2.5/weather"

# city = input('Enter city:\n')
city = 'Springfield'
api_key = os.getenv('api_key')

url = api_endpoint + "?q=" + city + "&appid=" + api_key
response = urllib.request.urlopen(url)

parseResponse = json.loads(response.read())

print(parseResponse)
