import json
import os
from urllib.request import urlopen
from datetime import datetime, date

import pytemperature


def get_location():
    url = 'http://ipinfo.io/json'
    resp = urlopen(url)
    data = json.load(resp)

    return data['city'], data['region'], data['country'], data['loc']


def today_parse():
    lat = coordinates.split(',')[0]
    lon = coordinates.split(',')[1]
    api_endpoint = "http://api.openweathermap.org/data/2.5/"
    api_key = os.getenv('api_key')
    url = f'{api_endpoint}onecall?lat={lat}&lon={lon}&exclude=daily,minutely&appid={api_key}'
    r = urlopen(url)  # sends request to the url created
    parse_response = json.loads(r.read())  # loads the response in a json

    return parse_response


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
    city, state, country, coordinates = get_location()
    Weather_location = f'{city}, {state}, {country}'
    response = today_parse()
    print(f'{dt_string}\n')
    print(current_result())
    # user_input = input('\nPress y to view the detailed weather report for today:\n')
    # if user_input == 'Y' or user_input == 'y':
    print(f"\nToday's Report with per hour interval:\n{today()}")
