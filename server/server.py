# TODO: refactor this file soon. 

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
            user = server.auth.verify_id_token(id_token)
            return f(user, *args, **kws)
        except:
            return jsonify({"message": "Invalid token"}), 401
    return decorated_function


class Server:

    def __init__(self, enable_socketio: bool=True, enable_db_uploading: bool=False):
        with open('firebase_config.json') as f:
            self.firebase_config = json.load(f)
        self.firebase = pyrebase.initialize_app(self.firebase_config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        self.connections = {}
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.status = {}
        self.stop_event = threading.Event()
        self.enable_socketio = enable_socketio
        self.enable_db_uploading = enable_db_uploading

        try:
            self.db.child("statuses").get()
        except:
            self.db.child("statuses").set({})


def handle_device_id(device_id):
    print(f"Device {device_id} has connected.")  # For debugging
    server.connections[device_id] = request.sid


def handle_disconnect():
    for device_id, sid in server.connections.items():
        if sid == request.sid:
            del server.connections[device_id]
            print(f"Device {device_id} has disconnected.")  # For debugging
            break


@authenticate
def get_status(user):
    return jsonify(server.status)


def post_status():
    data = request.get_json()
    deviceId = data['deviceId']
    server.status[deviceId] = {
        'status': data,
        'last_seen': datetime.now().isoformat()
    }

    print(f"Received data: {server.status[deviceId]}")  # For debugging
    return jsonify({"message": "Data received"}), 200


@authenticate
def post_command(user):
    data = request.get_json()
    deviceId = data['deviceId']
    command = data['command']
    if deviceId in server.connections:
        server.socketio.emit('command', command, room=server.connections[deviceId])
        return jsonify({"message": "Command sent"}), 200
    else:
        return jsonify({"message": "Device not connected"}), 400


def register_routes() -> None:
    server.socketio.on('device_id')(handle_device_id)
    server.socketio.on('disconnect')(handle_disconnect)
    server.app.route('/api/status', methods=['GET'])(get_status)
    server.app.route('/api/status', methods=['POST'])(post_status)
    server.app.route('/api/command', methods=['POST'])(post_command)


def send_status_updates():
    while not server.stop_event.is_set():
        items = list(server.status.items())
        for deviceId, device in items:
            if server.stop_event.is_set():
                print("Stop event set, breaking loop.")  # For debugging
                break
            last_seen = datetime.fromisoformat(device['last_seen'])
            if datetime.now() - last_seen > timedelta(seconds=10):
                print(f"Device {deviceId} is disconnected.")  # For debugging
                device['status']['wifiStatus'] = False
                if server.enable_socketio:
                    server.socketio.emit('status', {deviceId: device['status']})
            else:
                if server.enable_socketio:
                    print(f"Sending status update for device {deviceId}.")  # For debugging
                    server.socketio.emit('status', {deviceId: device['status']})
            if server.enable_db_uploading:
                # Push the status update to Firebase
                print(f"Pushing status update for device {deviceId} to Firebase.")  # For debugging
                server.db.child("statuses").child(deviceId).set(device)
            server.socketio.sleep(2)  # Sleep for 2 seconds


def signal_handler(signal, frame):
    print('Stopping the server...')
    server.stop_event.set()
    exit(0)  # Exit the program


if __name__ == '__main__':
    server = Server(enable_socketio=True)
    register_routes()
    server.socketio.start_background_task(send_status_updates)
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler
    try:
        server.socketio.run(server.app, port=5000)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
