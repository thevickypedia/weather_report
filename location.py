from urllib.request import urlopen
import json


def get_data():
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    data = json.load(response)
    city = data['city']
    region = data['region']

    return city, region
