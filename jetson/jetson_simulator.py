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
import sys
import threading
from socketio import Client
from typing import Dict, List

from utils.utility_funcs import load_env


load_env()
URL = os.environ.get('REACT_APP_URL')
# Check if it contains http or https
if URL.startswith('https'):
    print("Warning: URL starts with https. We are generally using http for local development.")

TIME_TILL_MATCH_TXT_FILE: str = "./time_till_match.txt"


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
        self.commands: Dict[str, List[str]] = {
            'start_camera_control': ['./camera_stepper_motors_control.py', deviceId],
            'start_high_computation': ['./high_power_torch_script.py'],
            'start_record_video': ['./record_video.py'],
            'start_camera_stream': ['./live_camera_stream.py'],
            'start_s3_sync': ['./sync_videos_to_s3.py']
        }
    
    @staticmethod
    def on_connect() -> None:
        sio.emit('device_id', deviceId)  # Send the device ID to the server; this is called when we reconnect to server
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
    
    def start_command(self, command: str) -> None:
        print(f'Received {command} command')
        if command not in self.process or self.process[command].poll() is not None:
            self.process[command] = subprocess.Popen(['python3'] + self.commands[command], stdin=subprocess.PIPE)
            time.sleep(1)
            if self.process[command].poll() is not None:
                print(f'Failed to start {command}')
                return
            else:
                print(f'{command} started successfully')
            with open(self.pid_file_path, 'w') as pid_file:
                pid_file.write(str(self.process[command].pid))

    def stop_command(self, command: str) -> None:
        print(f'Received stop {command} command')
        if command in self.process and self.process[command].poll() is None:
            self.process[command].terminate()
            self.process[command].wait()
            if os.path.exists(self.pid_file_path):
                os.remove(self.pid_file_path)
                
    def on_start_camera_control(self) -> None:
        self.start_command('start_camera_control')

    def on_stop_camera_control(self) -> None:
        self.stop_command('start_camera_control')

    def on_start_record_video(self) -> None:
        self.start_command("start_record_video")

    def on_stop_record_video(self) -> None:
        self.stop_command("start_record_video")

    def on_start_camera_stream(self) -> None:
        self.start_command("start_camera_stream")

    def on_stop_camera_stream(self) -> None:
        self.stop_command("start_camera_stream")
    
    def on_start_s3_sync(self) -> None:
        self.start_command("start_s3_sync")

    def on_stop_s3_sync(self) -> None:
       self.stop_command("start_s3_sync")

    # TODO: not entirely sure what this is doing
    def on_send_input(self, data) -> None:
        print('Received input:', data)
        # if process is running, send input to it
        if self.process is not None and self.process["start_camera_control"].poll() is None:
            input_data = data + '\n'  # Add a newline character at the end, because readline() reads until it encounters a newline
            self.process["start_camera_control"].stdin.write(
            input_data.encode())  # stdin expects bytes, so encode the string as bytes
            self.process["start_camera_control"].stdin.flush()  # flush the buffer to make sure the data is actually sent to the subprocess

    @staticmethod
    def on_fetch_time_till_match():
        print('Received fetch_time_till_match command')
        try:
            with open(TIME_TILL_MATCH_TXT_FILE, 'r') as file:
                time_till_match = file.read().strip()
            sio.emit('time_till_match_response', {
                'deviceId': deviceId,
                'time_till_match': time_till_match
            })
        except Exception as e:
            print(f"Error reading time till match: {e}")


    @staticmethod
    def send_time_till_match(self) -> None:
        """
        Reads TIME_TILL_MATCH_TXT_FILE and sends the contents to the server once
        """
        if os.path.exists(TIME_TILL_MATCH_TXT_FILE):
            with open(TIME_TILL_MATCH_TXT_FILE, 'r') as f:
                time_till_match = f.read()
                sio.emit('time_till_match', time_till_match)


# Device ID as a command line argument
if len(sys.argv) != 2:
    print('Usage: python script.py <device_id>')
    sys.exit(1)

deviceId = sys.argv[1]

sio = NamespaceHandler()

# Connect to the server using the IP address read from the file
print(f"Socketio connecting to {URL}...")
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
sio.on('start_record_video', sio.on_start_record_video)
sio.on('stop_record_video', sio.on_stop_record_video)
sio.on('start_s3_sync', sio.on_start_s3_sync)
sio.on('stop_s3_sync', sio.on_stop_s3_sync)
sio.on('fetch_time_till_match', sio.on_fetch_time_till_match)


# Emit the device_id event
sio.emit('device_id', deviceId)  # This is called when the server is running already when we connect

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
            
            response = requests.post(f'{URL}/api/status', data=json.dumps(data), headers={'Content-Type': 'application/json'})
            
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
