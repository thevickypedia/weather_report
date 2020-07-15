import socket
import urllib.request
import json


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])

response = urllib.request.urlopen("https://geolocation-db.com/json")
data = json.loads(response.read().decode())
print(data)
