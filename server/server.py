from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import pyrebase
import json
import signal
import threading
from functools import wraps

# A decorator to authenticate requests
def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        id_token = None
        if 'Authorization' in request.headers:
            id_token = request.headers['Authorization'].split(' ').pop()
        if not id_token:
            return jsonify({"message": "Token required"}), 401
        try:
            user = Server.auth.verify_id_token(id_token)
            return f(user, *args, **kws)
        except:
            return jsonify({"message": "Invalid token"}), 401
    return decorated_function

class Server:

    with open('firebase_config.json') as f:
        firebase_config = json.load(f)
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()
    db = firebase.database()

    def __init__(self, enable_socketio: bool=True):
        self.app = Flask(__name__)
        CORS(self.app) 
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")  
        self.status = {}
        self.stop_event = threading.Event()

        self.enable_socketio = enable_socketio

        # Create the 'statuses' child node if it doesn't exist
        try:
            Server.db.child("statuses").get()
        except:
            Server.db.child("statuses").set({})


        @self.app.route('/api/status', methods=['GET'])
        @authenticate
        def get_status(user): 
            return jsonify(self.status)

        @self.app.route('/api/status', methods=['POST'])
        def post_status():
            data = request.get_json()
            deviceId = data['deviceId']
            self.status[deviceId] = {
                'status': data,
                'last_seen': datetime.now().isoformat()
            }

            print(f"Received data: {self.status[deviceId]}")  # For debugging
            return jsonify({"message": "Data received"}), 200

    def send_status_updates(self):
        while not self.stop_event.is_set():
            items = list(self.status.items())
            for deviceId, device in items:
                if self.stop_event.is_set():
                    print("Stop event set, breaking loop.")  # For debugging
                    break
                last_seen = datetime.fromisoformat(device['last_seen'])
                if datetime.now() - last_seen > timedelta(seconds=10):
                    print(f"Device {deviceId} is disconnected.")  # For debugging
                    device['status']['wifiStatus'] = False
                    if self.enable_socketio:
                        self.socketio.emit('status', {deviceId: device['status']})
                else:
                    if self.enable_socketio:
                        print(f"Sending status update for device {deviceId}.")  # For debugging
                        self.socketio.emit('status', {deviceId: device['status']})

                # Push the status update to Firebase
                print(f"Pushing status update for device {deviceId} to Firebase.")  # For debugging
                Server.db.child("statuses").child(deviceId).set(device)
                self.socketio.sleep(1)  # Sleep for 1 second


def signal_handler(signal, frame):
    print('Stopping the server...')
    server.stop_event.set()
    exit(0)  # Exit the program

signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler

if __name__ == '__main__':
    server = Server(enable_socketio=True)
    server.socketio.start_background_task(server.send_status_updates)
    try:
        server.socketio.run(server.app, port=5000)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
