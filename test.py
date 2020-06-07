import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.accuweather.com/en/us/springfield/65806/daily-weather-forecast/329438'

r = requests.get(url)
scrapped = bs(r.text, "html.parser")
print(scrapped)
