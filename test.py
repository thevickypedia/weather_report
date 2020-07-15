import socket
from urllib.request import urlopen
import json


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
print(data)
