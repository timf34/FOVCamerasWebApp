from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import pyrebase
import json
import signal
import threading
from functools import wraps

with open('firebase_config.json') as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable SocketIO and allow cross-origin requests

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
            user = auth.verify_id_token(id_token)
            return f(user, *args, **kws)
        except:
            return jsonify({"message": "Invalid token"}), 401
    return decorated_function

# Initialize status dictionary
status = {}

# Initialize stop_event
stop_event = threading.Event()

@app.route('/api/status', methods=['GET'])
@authenticate
def get_status(user):  # User's data is now available as parameter
    return jsonify(status)

@app.route('/api/status', methods=['POST'])
def post_status():
    global status
    data = request.get_json()
    deviceId = data['deviceId']
    status[deviceId] = {
        'status': data,
        'last_seen': datetime.now()
    }

    print(f"Received data: {status[deviceId]}")  # For debugging
    # db.child("statuses").child(status['deviceId']).set(status)  # Push the status update to Firebase
    return jsonify({"message": "Data received"}), 200

def send_status_updates():
    while not stop_event.is_set():
        # Make a copy of the items
        items = list(status.items())
        for deviceId, device in items:
            if stop_event.is_set():
                print("Stop event set, breaking loop.")  # For debugging
                break
            if datetime.now() - device['last_seen'] > timedelta(seconds=10):
                # If we haven't heard from the device in more than 10 seconds,
                # mark it as disconnected and send a status update
                print(f"Device {deviceId} is disconnected.")  # For debugging
                device['status']['wifiStatus'] = False
                socketio.emit('status', {deviceId: device['status']})
            else:
                # If the device is still connected, update its status as before
                print(f"Sending status update for device {deviceId}.")  # For debugging
                socketio.emit('status', {deviceId: device['status']})
            socketio.sleep(1)  # Sleep for 1 second



def signal_handler(signal, frame):
    print('Stopping the server...')
    stop_event.set()  # Signal the background task to stop
    exit(0)  # Exit the program

signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler

if __name__ == '__main__':
    socketio.start_background_task(send_status_updates)  # Start sending status updates in the background
    try:
        socketio.run(app, port=5000)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
