# TODO: refactor this file soon. 

from datetime import datetime, timedelta
import cv2
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from flask_socketio import SocketIO
import firebase_admin
from firebase_admin import credentials, auth, db
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
            decoded_token = auth.verify_id_token(id_token)
            # user = auth.get_user(decoded_token['uid'])
            # Convert decoded token to a dictionary
            decoded_token = decoded_token.items()
            # for key, value in decoded_token:
            #     print(f"{key}: {value}")
            return f(decoded_token, *args, **kws)
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"message": "Invalid token"}), 401
    return decorated_function


class Server:

    def __init__(self, enable_socketio: bool=True, enable_db_uploading: bool=False):
        with open('firebase_config.json') as f:
            self.firebase_config = json.load(f)

        # self.firebase = pyrebase.initialize_app(self.firebase_config)
        cred = firebase_admin.credentials.Certificate("../keys/fov-cameras-web-app-firebase-adminsdk-az1vf-8396208820.json")
        default_app = firebase_admin.initialize_app(cred, options=self.firebase_config)

        self.auth = auth
        self.db = db
        self.connections = {}
        self.app = Flask(__name__)
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.status = {}
        self.stop_event = threading.Event()
        self.enable_socketio = enable_socketio
        self.enable_db_uploading = enable_db_uploading

        try:
            self.db.reference('statuses').get()
        except:
            self.db.reference('statuses').document().set({})



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


def video():
    print("Sending video")
    return send_from_directory(directory='../data/', path='sample_vid.mp4', mimetype='video/mp4')


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
    print(f"Received command: {command} and deviceID: {deviceId}")  # For debugging
    if deviceId in server.connections:
        print("Server connections1: ", server.connections)
        server.socketio.emit('command', command, room=server.connections[deviceId])
        return jsonify({"message": "Command sent"}), 200
    else:
        print("Server connections2: ", server.connections)
        return jsonify({"message": "Device not connected"}), 400


def register_routes() -> None:
    server.socketio.on('device_id')(handle_device_id)
    server.socketio.on('disconnect')(handle_disconnect)
    server.app.route('/api/status', methods=['GET'])(get_status)
    server.app.route('/api/status', methods=['POST'])(post_status)
    server.app.route('/api/command', methods=['POST'])(post_command)
    server.app.route('/api/video', methods=['GET'])(video)
    server.app.route('/api/video_feed', methods=['GET'])(video_feed)



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
                server.db.reference('statuses').child(deviceId).set(device)

            server.socketio.sleep(5)  # Sleep for 2 seconds


def signal_handler(signal, frame):
    print('Stopping the server...')
    server.stop_event.set()
    exit(0)  # Exit the program


def gen_frames():
    # Connect to the video stream
    print("gen frames")
    # cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp,media=video,payload=96,encoding-name=H264 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! appsink', cv2.CAP_GSTREAMER)
    print("cap is open: ", cap.isOpened())
    while True:
        success, frame = cap.read()  # read the camera frame
        print("success: ", success)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def video_feed():
    print("Sending video feed")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    server = Server(enable_socketio=True)
    register_routes()
    server.socketio.start_background_task(send_status_updates)
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler
    try:
        server.socketio.run(server.app, port=5000)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
