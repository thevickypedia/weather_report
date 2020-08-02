import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime

import certifi
import geopy.geocoders
import pytemperature
from bs4 import BeautifulSoup as bs
from geopy.geocoders import Nominatim

# city = input('Enter city:\n')
city = 'Springfield'


def parseResponse(api_key):
    """This function gets the raw weather information"""
    api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
    url = api_endpoint + "?q=" + city + "&appid=" + api_key  # creates an url
    try:
        response = urllib.request.urlopen(url)  # sends request to the url created
        parse_response = json.loads(response.read())  # loads the response in a json
        return parse_response
    except:
        if len(city) < 1:
            print('Please enter a city name to continue.')
            exit()
        else:
            # passes headers to access browser
            headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686)"}
            # stores incorrect city value in the format that can combined to an url
            values = {'q': f'{city}'}
            # parses the stored value and generates a url code
            data = urllib.parse.urlencode(values)
            url = f'https://www.google.com/search?{data}'
            req = urllib.request.Request(url, headers=headers)  # sends a request tot he url
            resp = urllib.request.urlopen(req)
            resp_data = resp.read()  # reads the response
            soup = bs(resp_data, 'html.parser')  # html parsing
            data = soup.find_all('div', {'class': 'Pg70bf Uv67qb'})  # looks for the right class under div
            raw = data[0].find_all('a')  # looks for tag <a></a>
            url_ = raw[0].get('href')  # gets the href url eg: https://maps.google.com/search?q:{suggestion}
            suggested_city = (url_.split('=')[1].replace('&source', '').replace('&um', ''))  # extracts value from url
            print(f"Trying '{suggested_city}' instead of '{city}'\n")
            try:
                api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
                api_key = os.getenv('api_key')
                url = api_endpoint + "?q=" + suggested_city + "&appid=" + api_key  # creates an url
                response = urllib.request.urlopen(url)  # sends request to the url created
                parse_response = json.loads(response.read())  # loads the response in a json
                return parse_response
            except:
                print('Please try with a valid city name.')
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
    try:
        county = f'{c_l[-5]}, {c_l[-4]}, {c_l[-3]}, {c_l[-1]}'  # gets only the county, state and/or country information
    except IndexError:
        county = current_location  # if raised index error stores the entire address here
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
    temp_feel_f = float(round(pytemperature.k2f(feels_like), 2))
    temp_min = float(round(pytemperature.k2f(temp_mn), 2))
    temp_max = float(round(pytemperature.k2f(temp_mx), 2))

    output = (f'{location}, {country}\n\nCurrent Temperature: {temp_f}°F\n'
              f'Feels Like: {temp_feel_f}°F\nHigh: {temp_max}°F Low: {temp_min}°F\n'
              f'Condition: {weather}')

    return output


if __name__ == '__main__':
    api_key = os.getenv('api_key')
    if not api_key:
        print('API Key not found in environment variables. Exiting..')
        exit(1)
    now = datetime.now()
    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")
    parseResponse = parseResponse(api_key)
    location = location()
    print(f'{dt_string}\n')
    print(result())
