import socket
from urllib.request import urlopen
import json


print('Your IP details:\n ')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(f'Origin IP: {s.getsockname()[0]}')

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
ip = data['ip']
org = data['org']
city = data['city']
country = data['country']
region = data['region']

print(f'Destination IP: {ip}\nCity: {city}\nState: {region}\nCountry: {country}\nISP: {org}')
