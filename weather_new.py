import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, date

import certifi
import geopy.geocoders
import pytemperature
from geopy.geocoders import Nominatim

city = 'Springfield'
state = 'Missouri'


def today_parse():
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geo_locator = Nominatim(scheme='http', user_agent='test/1', timeout=3)
    try:
        location = geo_locator.geocode(f'{city}, {state}')
        lat = location.latitude
        lon = location.longitude
        city_info = location.address
        api_endpoint = "http://api.openweathermap.org/data/2.5/"
        api_key = os.getenv('api_key')
        url = f'{api_endpoint}onecall?lat={lat}&lon={lon}&exclude=daily,minutely&appid={api_key}'
        r = urllib.request.urlopen(url)  # sends request to the url created
        parse_response = json.loads(r.read())  # loads the response in a json

        return parse_response, city_info
    except AttributeError:
        print('Make sure the city and state combination is correct.\nIf you are unsure of either of it you may leave '
              'it blank rather incorrect.')
        exit(1)
    except NameError:
        print('Make sure either city or state is entered.')
        exit(1)


def today():
    import time
    hourly_data = (response['hourly'])
    output = ''
    for data in hourly_data:
        epoch = data['dt']
        timestamp = time.strftime('%m-%d %H Hrs', time.localtime(epoch))
        today = date.today().strftime('%m-%d')
        if today in timestamp:
            temperature = data['temp']
            weather = data['weather'][0]['description']
            feels_like = data['feels_like']
            temp_f = float(round(pytemperature.k2f(temperature), 2))
            temp_feel_f = float(round(pytemperature.k2f(feels_like), 2))
            output += (f'{timestamp}: Actual: {temp_f}°F '
                       f'Feels Like: {temp_feel_f}°F Condition: {weather}\n')
    output_ = f'{Weather_location}\n{output}'

    return output_


def current_result():
    temperature = response['current']['temp']
    weather = response['current']['weather'][0]['description']
    feels_like = response['current']['feels_like']
    temp_f = float(round(pytemperature.k2f(temperature), 2))
    temp_feel_f = float(round(pytemperature.k2f(feels_like), 2))
    output = (f'{Weather_location}\nCurrent Temperature: {temp_f}°F\n'
              f'Feels Like: {temp_feel_f}°F\nCondition: {weather}')

    return output


if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")
    response, Weather_location = today_parse()
    print(f'{dt_string}\n')
    print(current_result())
    user_input = input('\nPress y to view the detailed weather report for today:\n')
    if 'Y' or 'y' in user_input:
        print(f"Today's Report with per hour interval:\n{today()}")
