from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import time

app = Flask(__name__)
CORS(app) # This allows cross-origin requests

status = {
    'deviceId': 'jetson_nano_1',
    'wifiStatus': True,
    'batteryLevel': 91,
    'temperature': 40
}

socketio = SocketIO(app, cors_allowed_origins="*") # Enable SocketIO and allow cross-origin requests

@app.route('/api/status')
def get_status():
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
