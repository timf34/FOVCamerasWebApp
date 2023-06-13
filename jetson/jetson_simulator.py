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
import os 
import random
import time
import subprocess
import threading
from socketio import Client
from typing import Dict

from utils import load_env


URL = load_env()


def get_wifi_status() -> bool:
    # randomly return True or False
    return True


def get_battery_level() -> int:
    # randomly return a number between 0 and 100
    return random.randint(0, 100)


def get_temperature() -> int:
    # randomly return a number between 0 and 100
    return random.randint(0, 100)


class NamespaceHandler(Client):
    def __init__(self):
        super().__init__()
        self.process: Dict[str, subprocess.Popen] = {}  # key: command, value: subprocess.Popen object
        self.pid_file_path = './camera_control_pid.txt'

    @staticmethod
    def on_connect() -> None:
        print('Connected to the server')

    @staticmethod
    def on_disconnect() -> None:
        print('Disconnected from the server')

    @staticmethod
    def on_message(data) -> None:
        print('Received message:', data)

    @staticmethod
    def on_command(data) -> None:  # This function listens for the 'command' event
        print('Received command:', data)
    
    def on_start_camera_control(self) -> None:
        print('Received start camera control command')
        if "start_camera_control" not in self.process or self.process["start_camera_control"].poll() is not None:
            self.process["start_camera_control"] = subprocess.Popen(['python3', './stepperTests.py'], stdin=subprocess.PIPE)
            time.sleep(1)
            if self.process["start_camera_control"].poll() is not None:
                print('Failed to start process')
                return
            else:
                print('Process started successfully')
            with open(self.pid_file_path, 'w') as pid_file:
                pid_file.write(str(self.process["start_camera_control"].pid))

    def on_stop_camera_control(self) -> None:
        print('Received stop camera control command')
        if "start_camera_control" in self.process and self.process["start_camera_control"].poll() is None:
            self.process["start_camera_control"].terminate()
            self.process["start_camera_control"].wait()
            if os.path.exists(self.pid_file_path):
                os.remove(self.pid_file_path)

    def on_send_input(self, data) -> None:
        print('Received input:', data)
        # if process is running, send input to it
        if self.process is not None and self.process["start_camera_control"].poll() is None:
            input_data = data + '\n'  # Add a newline character at the end, because readline() reads until it encounters a newline
            self.process["start_camera_control"].stdin.write(input_data.encode())  # stdin expects bytes, so encode the string as bytes
            self.process["start_camera_control"].stdin.flush()  # flush the buffer to make sure the data is actually sent to the subprocess

    def on_start_camera_stream(self) -> None:
        print('Received start camera stream command')
        if "start_camera_stream" not in self.process or self.process["start_camera_stream"].poll() is not None:
            self.process["start_camera_stream"] = subprocess.Popen(['python3', './jetson_stream_simulator.py'], stdin=subprocess.PIPE)
            time.sleep(1)
            if self.process["start_camera_stream"].poll() is not None:
                print('Failed to start process')
                return
            else:
                print('Process started successfully')
            with open(self.pid_file_path, 'w') as pid_file:
                pid_file.write(str(self.process["start_camera_stream"].pid))

    def on_stop_camera_stream(self) -> None:
        print('Received stop camera stream command')
        if "start_camera_stream" in self.process and self.process["start_camera_stream"].poll() is None:
            self.process["start_camera_stream"].terminate()
            self.process["start_camera_stream"].wait()
            if os.path.exists(self.pid_file_path):
                os.remove(self.pid_file_path)
  

# Device ID as a command line argument
import sys
if len(sys.argv) != 2:
    print('Usage: python script.py <device_id>')
    sys.exit(1)

deviceId = sys.argv[1]

# TODO: add error handling here!
with open('ip_address.txt', 'r') as file:
    ip_address = file.read().strip()

sio = NamespaceHandler()

# Connect to the server using the IP address read from the file
sio.connect(f'{URL}')

# Register event handlers
sio.on('connect', sio.on_connect)
sio.on('disconnect', sio.on_disconnect)
sio.on('message', sio.on_message)
sio.on('command', sio.on_command)  # Listen for 'command' event
sio.on('start_camera_control', sio.on_start_camera_control)
sio.on('stop_camera_control', sio.on_stop_camera_control)
sio.on('send_input', sio.on_send_input)
sio.on('start_camera_stream', sio.on_start_camera_stream)
sio.on('stop_camera_stream', sio.on_stop_camera_stream)

# Emit the device_id event
sio.emit('device_id', deviceId)


# Start a new thread for periodically sending status updates
def send_status_updates() -> None:
    while True:
        try:
            data = {
                'deviceId': deviceId,
                'wifiStatus': get_wifi_status(),
                'batteryLevel': get_battery_level(),
                'temperature': get_temperature()
            }
            
            # response = requests.post(f'http://{ip_address}:5000/api/status', data=json.dumps(data), headers={'Content-Type': 'application/json'})
            response = requests.post('http://fovcameraswebappv2.eu-west-1.elasticbeanstalk.com/api/status', data=json.dumps(data), headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                print('Data sent successfully')
                print(data)
            else:
                print('Failed to send data')
        
        except Exception as e:
            print(f"Error: {e}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")

        time.sleep(5)  # Wait for 5 seconds before sending the next status update


status_thread = threading.Thread(target=send_status_updates)
status_thread.start()

try:
    sio.wait()
finally:
    sio.disconnect()
