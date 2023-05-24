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
import random
import time
import websocket
import threading 

def get_wifi_status():
    # randomly return True or False
    return True

def get_battery_level():
    # randomly return a number between 0 and 100
    return random.randint(0, 100)

def get_temperature():
    # randomly return a number between 0 and 100
    return random.randint(0, 100)

def on_message(ws, message):
    print(f'Received command: {message}')
    # TODO: Handle command...

def on_error(ws, error):
    print(f'Error: {error}')

def on_close(ws):
    print('Connection closed')

def on_open(ws):
    def run():
        while True:
            time.sleep(1)
    thread = threading.Thread(target=run)
    thread.start()

# Device ID as a command line argument
import sys
if len(sys.argv) != 2:
    print('Usage: python script.py <device_id>')
    sys.exit(1)

deviceId = sys.argv[1]

# Create a new WebSocket connection
ws = websocket.WebSocketApp(
    f"ws://localhost:5000/{deviceId}",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close)

# Start the WebSocket connection in a new thread so it doesn't block the main loop
wst = threading.Thread(target=ws.run_forever)
wst.start()

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
