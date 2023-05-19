from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import time
import pyrebase
import json
from functools import wraps

with open('firebase_config.json') as f:
    firebase_config = json.load(f)

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

app = Flask(__name__)
CORS(app) # This allows cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*") # Enable SocketIO and allow cross-origin requests

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

status = {
    'deviceId': 'jetson_nano_1',
    'wifiStatus': True,
    'batteryLevel': 91,
    'temperature': 40
}

@app.route('/api/status')
@authenticate
def get_status(user): # User's data is now available as parameter
    return jsonify(status)

def send_status_updates():
    while True:
        for i in range(0, 100):
            status['batteryLevel'] = i
            status['temperature'] = i
            status['wifiStatus'] = not status['wifiStatus']
            socketio.sleep(1) # Sleep for 1 second
            socketio.emit('status', status) # Emit the status data on the 'status' channel

if __name__ == '__main__':
    socketio.start_background_task(send_status_updates) # Start sending status updates in the background
    socketio.run(app, port=5000)

