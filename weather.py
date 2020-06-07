import urllib.request
import json
import pytemperature
import os
import ssl
import certifi
import geopy.geocoders
from geopy.geocoders import Nominatim

api_endpoint = "http://api.openweathermap.org/data/2.5/weather"

# city = input('Enter city:\n')
city = 'Springfield'
api_key = os.getenv('api_key')

url = api_endpoint + "?q=" + city + "&appid=" + api_key
response = urllib.request.urlopen(url)

parseResponse = json.loads(response.read())

country = parseResponse['sys']['country']
temperature = parseResponse['main']['temp']
weather = parseResponse['weather'][0]['description']
feels_like = parseResponse['main']['feels_like']
temp_mn = parseResponse['main']['temp_min']
temp_mx = parseResponse['main']['temp_max']

temp_f = float(round(pytemperature.k2f(temperature), 2))
temp_c = float(round(pytemperature.k2c(temperature), 2))
temp_feel_f = float(round(pytemperature.k2f(feels_like), 2))
temp_feel_c = float(round(pytemperature.k2c(feels_like), 2))
temp_min = float(round(pytemperature.k2c(temp_mn), 2))
temp_max = float(round(pytemperature.k2c(temp_mx), 2))


def location():
    # This is to ensure your request to geopy goes through a cert
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx

    coordinates = parseResponse['coord']
    lon = (coordinates['lon'])
    lat = (coordinates['lat'])
    geo_locator = Nominatim(scheme='http', user_agent='test/1', timeout=3)
    locator = geo_locator.reverse(f'{lat}, {lon}')
    current_location = locator.address
    c_l = current_location.split(', ')
    county = f'{c_l[4]}, {c_l[5]}, {c_l[7]}'
    return county


output = (f'{city}, {location()}, {country}\n\nCurrent Temperature: {temp_f}°F\n'
          f'Feels Like: {temp_feel_f}°F\nMinimum: {temp_min}°F Maximum: {temp_max}°F\n'
          f'Condition: {weather}')

print(output)
