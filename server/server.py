import threading    
import json
import logging
import numpy as np
import firebase_admin
from firebase_admin import auth, db
from stream_manager import StreamManager

last_received_motor_positions = {}


class Server:
    """Server"""
    def __init__(self, enable_socketio: bool=True, enable_db_uploading: bool=False, developing_react_locally: bool = False):
        self.auth = auth
        self.db = db
        self.connections = {}
        self.developing_react_locally: bool = developing_react_locally
        self.status = {}
        print("Before threading")
        self.stop_event = threading.Event()
        print("After threading")
        self.enable_socketio = enable_socketio
        self.enable_db_uploading = enable_db_uploading
        self.stream_manager = StreamManager()
        self.load_firebase_config()

    def load_firebase_config(self):
        with open('firebase_config.json') as f:
            self.firebase_config = json.load(f)
        cred = firebase_admin.credentials.Certificate("./keys/fov-cameras-web-app-firebase-adminsdk-az1vf-8396208820.json")