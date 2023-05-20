"""
Simulate the Jetsons sending status updates to the server.

Run from multiple terminals as follows:

`python script.py jetson_nano_1`

`python script.py jetson_nano_2`

`python script.py jetson_nano_3`

`python script.py jetson_nano_4`
"""


import requests
import json
import time
import random

def get_wifi_status():
    # randomly return True or False
    return True

def get_battery_level():
    # randomly return a number between 0 and 100
    return random.randint(0, 100)

def get_temperature():
    # randomly return a number between 0 and 100
    return random.randint(0, 100)

# Device ID as a command line argument
import sys
if len(sys.argv) != 2:
    print('Usage: python script.py <device_id>')
    sys.exit(1)

deviceId = sys.argv[1]

while True:
    try:
        data = {
            'deviceId': deviceId,
            'wifiStatus': get_wifi_status(),
            'batteryLevel': get_battery_level(),
            'temperature': get_temperature()
        }
        
        response = requests.post('http://localhost:5000/api/status', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print('Data sent successfully')
            print(data)
        else:
            print('Failed to send data')
    
    except Exception as e:
        print(f"Error: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

    time.sleep(5)  # Wait for 10 seconds before sending the next status update
