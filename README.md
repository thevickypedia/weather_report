# weather_report
This is a fun project using [openweathermap](https://openweathermap.org/api) api

## Setup:

1. git clone this repository

2. Run this command in your terminal to install necessary packages<br/>pip3 install -r requirements.txt

3. Add the env variable: api_key - The api key which was generated from [openweathermap](https://openweathermap.org/api)

This project includes reverse geocoding as an add-on, since the api does not return state/county information of the city.

Click to learn more about [pytemperature](https://pypi.org/project/pytemperature/) and [geopy](https://pypi.org/project/geopy/)

## Extras:

[Old Weather](weather_old.py) uses reverse geo coding to get the location of the city which is hardcoded. 
The old weather application will only fetch that day's weather info.

[Weather](weather.py) uses reverse geo coding to get the location of the city and state which is hardcoded. 
The old weather application will fetch that week's weather info.

[Weather by Location](weather_by_location.py) sends a request to [ipinfo](http://ipinfo.io/) to get the ip and location of
 the request machine. Using these information, it fetches that week's weather info. While running [this](weather_by_location.py) application
from an unverified network might require api key from [ipinfo](http://ipinfo.io/) through a [sign up](https://ipinfo.io/signup)  

## License & copyright

&copy; Vignesh Sivanandha Rao, Weather Report

Licensed under the [MIT License](LICENSE)
