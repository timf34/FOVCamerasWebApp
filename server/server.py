import threading    
import json
import logging
import numpy as np
from stream_manager import StreamManager

last_received_motor_positions = {}


class Server:
    """Server"""
    def __init__(self, enable_socketio: bool=True, developing_react_locally: bool = False):
        self.connections = {}
        self.developing_react_locally: bool = developing_react_locally
        self.status = {}
        print("Before threading")
        self.stop_event = threading.Event()
        print("After threading")
        self.enable_socketio = enable_socketio
        self.stream_manager = StreamManager()