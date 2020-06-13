import json
import os
import ssl
import urllib.request
import urllib.parse
from datetime import datetime

import certifi
import geopy.geocoders
import pytemperature
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
# city = input('Enter city:\n')
city = 'Springfld'


def parseResponse():
    """This function gets the raw weather information"""
    api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
    api_key = os.getenv('api_key')
    url = api_endpoint + "?q=" + city + "&appid=" + api_key  # creates an url
    try:
        response = urllib.request.urlopen(url)  # sends request to the url created
        parse_response = json.loads(response.read())  # loads the response in a json
        return parse_response
    except:
        if len(city) < 2:
            print('Please enter a city name to continue.')
        else:
            headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686)"}
            values = {'q': f'{city}'}
            data = urllib.parse.urlencode(values)
            url = 'https://www.google.com/search?' + data
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            resp_data = resp.read()
            soup = bs(resp_data, 'html.parser')
            suggest = f"Try this instead of {city}:\n"
            for data in soup.find_all('div', {'class': 'Pg70bf Uv67qb'}):
                for a in data.find_all('a'):
                    url_ = (a.get('href'))
                    # print(a.text)
                    if url_.startswith('https'):
                        suggest += (url_.split('=')[1].strip('&um'))
            print(suggest)
        exit()


def location():
    """This function gets the location information using reverse geocoding"""
    # This is to ensure your request to geopy goes through a cert
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    # extracts latitude and longitude information
    coordinates = parseResponse['coord']
    lon = (coordinates['lon'])
    lat = (coordinates['lat'])
    # gets location information using the latitude and longitude values
    geo_locator = Nominatim(scheme='http', user_agent='test/1', timeout=3)
    locator = geo_locator.reverse(f'{lat}, {lon}')
    current_location = locator.address  # extracts the address part
    c_l = current_location.split(', ')
    county = f'{c_l[4]}, {c_l[5]}, {c_l[7]}'  # gets only the county, state and/or country information
    return county


def result():
    """This function is to get detailed weather information"""
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
    temp_min = float(round(pytemperature.k2f(temp_mn), 2))
    temp_max = float(round(pytemperature.k2f(temp_mx), 2))

    output = (f'{city}, {location}, {country}\n\nCurrent Temperature: {temp_f}°F\n'
              f'Feels Like: {temp_feel_f}°F\nHigh: {temp_max}°F Low: {temp_min}°F\n'
              f'Condition: {weather}')

    return output


if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")
    parseResponse = parseResponse()
    location = location()
    print(f'{dt_string}\n')
    print(result())
