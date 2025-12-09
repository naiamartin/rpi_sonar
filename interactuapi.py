import requests
import random
import json

API_URL = "http://0.0.0.0:8000" 

print(requests.post(f"{API_URL}/sensor/update", json=5.0).text)
print(requests.get(f"{API_URL}/sensor/current").text)
print(requests.post(f"{API_URL}/game/playing", json=False).text)
