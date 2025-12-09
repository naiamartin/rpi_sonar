import requests
import random
import json

API_URL = "http://0.0.0.0:8000" 

print(requests.post(f"{API_URL}/sensor/update", json=97.0).text)
print(requests.post(f"{API_URL}/led/update", json={"led_r":True, "led_v":False}).text)
print(requests.get(f"{API_URL}/sensor/current").text)
leds = requests.get(f"{API_URL}/led/current").content.decode('utf-8')

leds = json.loads(leds)

led_v = leds["led_v"]
led_r = leds["led_r"]
print(led_v)
print(led_r)