from datetime import datetime, timedelta
from functools import wraps
import cv2
import logging
import signal
import numpy as np
from flask import Flask, jsonify, request, send_from_directory, Response
from flask_cors import CORS
from flask_socketio import SocketIO
from firebase_admin import db
from server import Server
from time import time

socketio = SocketIO(logger=True, engineio_logger=True, async_mode='eventlet', cors_allowed_origins="*")

last_received_motor_positions = {}
last_received_time_till_match = {}


def handle_device_command(event_name, success_message, _server: Server, error_message="Device not connected"):
    print(f"{event_name} command received")
    data = request.get_json()
    deviceId = data['deviceId']
    if deviceId in _server.connections:
        socketio.emit(event_name, room=_server.connections[deviceId])
        return jsonify({"message": success_message}), 200
    else:
        return jsonify({"message": error_message}), 400


def create_app():
    app = Flask(__name__, static_folder='./build/static', template_folder='./build')
    app.logger.setLevel(logging.INFO)
    CORS(app, resources={r'/*': {'origins': '*'}})

    socketio.init_app(app)

    server = Server()

    @socketio.on('device_id')
    def handle_device_id(device_id):
        print(f"Device {device_id} has connected.")  # For debugging
        app.logger.info(f"Device {device_id} has connected.")  # For debugging
        server.connections[device_id] = request.sid

    @socketio.on('disconnect')
    def handle_disconnect():
        for device_id, sid in server.connections.items():
            if sid == request.sid:
                del server.connections[device_id]
                print(f"Device {device_id} has disconnected.")  # For debugging
                break

    @app.route('/api/status', methods=['GET'])
    def get_status():
        return jsonify(server.status)

    @app.route('/api/status', methods=['POST'])
    def post_status():
        print("Received status dawg")
        data = request.get_json()
        deviceId = data['deviceId']
        server.status[deviceId] = {
            'status': data,
            'last_seen': datetime.now().isoformat()
        }

        print(f"Received data: {server.status[deviceId]}")  # For debugging
        app.logger.info(f"Received data: {server.status[deviceId]}")
        return jsonify({"message": "Data received"}), 200


    @app.route('/api/command', methods=['POST'])
    def post_command():
        data = request.get_json()
        deviceId = data['deviceId']
        command = data['command']
        print(f"Received command: {command} and deviceID: {deviceId}")  # For debugging
        app.logger.info(f"Received command: {command} and deviceID: {deviceId}")  # For debugging
        if deviceId in server.connections:
            print("Server connections1: ", server.connections)
            socketio.emit('command', command, room=server.connections[deviceId])
            return jsonify({"message": "Command sent"}), 200
        else:
            print("Server connections2: ", server.connections)
            return jsonify({"message": "Device not connected"}), 400

    @app.route('/api/start-camera', methods=['POST'])
    def handle_start_camera_control():
        return handle_device_command('start_camera_control', "Camera control start command sent", server=server)

    @app.route('/api/stop-camera', methods=['POST'])
    def handle_stop_camera_control():
        return handle_device_command('stop_camera_control', "Camera control stop command sent", server=server)

    @app.route('/api/start-camera-stream', methods=['POST'])
    def handle_start_camera_stream():
        return handle_device_command('start_camera_stream', "Camera stream start command sent", server=server)

    @app.route('/api/stop-camera-stream', methods=['POST'])
    def handle_stop_camera_stream():
        return handle_device_command('stop_camera_stream', "Camera stream stop command sent", server=server)
    
    @app.route('/api/start-record-video', methods=['POST'])
    def handle_start_record_video():
        return handle_device_command('start_record_video', "Record video start command sent", server=server)

    @app.route('/api/stop-record-video', methods=['POST'])
    def handle_stop_record_video():
        return handle_device_command('stop_record_video', "Record video stop command sent", server=server)
        
    @app.route('/api/start-s3-sync', methods=['POST'])
    def handle_start_s3_sync():
        return handle_device_command('start_s3_sync', "Record video start command sent", server=server)

    @app.route('/api/stop-s3-sync', methods=['POST'])
    def handle_stop_s3_sync():
        return handle_device_command('stop_s3_sync', "Record video stop command sent", server=server)
    
    # TODO: not sure what this func does
    @app.route('/api/send-input', methods=['POST'])
    def handle_send_input():
        data = request.get_json()
        deviceId = data['deviceId']
        input_data = data['input']
        if deviceId in server.connections:
            socketio.emit('send_input', input_data, room=server.connections[deviceId])
            return jsonify({"message": "Input sent"}), 200
        else:
            return jsonify({"message": "Device not connected"}), 400

    @app.route('/api/image', methods=['GET'])
    def get_image():
        image_data = server.stream_manager.get_image()
        if image_data is None:
            return 'No image available', 404
        return Response(image_data, mimetype='image/jpeg')

    @app.route('/api/image', methods=['POST'])
    def new_streaming_method():
        nparr = np.fromstring(request.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        _, img_encoded = cv2.imencode('.jpg', img)
        image_data = img_encoded.tobytes()

        server.stream_manager.update_image(image_data)

        return '', 200

    @app.route('/api/motor-positions', methods=['POST'])
    def get_motor_positions():
        global last_received_motor_positions
        try:
            data = request.get_json()
            if not data or 'deviceId' not in data:
                raise ValueError("Invalid request data")
            deviceId = data['deviceId']
            print("Motor positions: \n", data)
            last_received_motor_positions[deviceId] = data  # save data for this device
            return jsonify(data), 200
        except Exception as e:
            print(f"Error in get_motor_positions: {e}")
            return jsonify({"status": "failure", "message": str(e)}), 400

    @app.route('/api/get-motor-positions/<device_id>', methods=['GET'])
    def send_motor_positions(device_id):
        global last_received_motor_positions
        if device_id in last_received_motor_positions:
            return jsonify(last_received_motor_positions[device_id]), 200
        else:
            return jsonify(
                {"status": "failure", "message": f"No motor positions received yet for device {device_id}"}), 400
    
    @app.route('/api/time-till-match', methods=['POST'])
    def get_time_till_match():
        global last_received_time_till_match
        try:
            data = request.get_json()
            if not data or 'deviceId' not in data:
                raise ValueError("Invalid request data")
            deviceId = data['deviceId']
            print("Time till match: \n", data)
            last_received_time_till_match[deviceId] = data  # save data for this device
            return jsonify(data), 200
        except Exception as e:
            print(f"Error in get_time_till_match: {e}")
            return jsonify({"status": "failure", "message": str(e)}), 400

    @app.route('/api/get-time-till-match/<device_id>', methods=['GET'])
    def send_time_till_match(device_id):
        global last_received_time_till_match
        if device_id in last_received_time_till_match:
            return jsonify(last_received_time_till_match[device_id]), 200
        else:
            return jsonify(
                {"status": "failure", "message": f"No time till match data received yet for device {device_id}"}), 400

    @socketio.on('frame')
    def handle_frame(data):
        image_data = data['image']
        nparr = np.fromstring(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        _, img_encoded = cv2.imencode('.jpg', img)
        image_data = img_encoded.tobytes()

        server.stream_manager.update_image(image_data)

    @app.route('/', methods=['GET'])
    def serve():
        return send_from_directory('build', 'index.html')

    def send_status_updates():
        while True:
            items = list(server.status.items())
            # print("server.stop_event: ", server.stop_event)
            # print(items)
            for deviceId, device in items:
                if server.stop_event.is_set():
                    print("Stop event set, breaking loop.")  # For debugging
                    app.logger.info("Stop event set, breaking loop.")  # For debugging
                    break
                last_seen = datetime.fromisoformat(device['last_seen'])
                if datetime.now() - last_seen > timedelta(seconds=10):
                    print(f"Device {deviceId} is disconnected.")  # For debugging
                    app.logger.info(f"Device {deviceId} is disconnected.")  # For debugging
                    device['status']['wifiStatus'] = False
                    if server.enable_socketio:
                        socketio.emit('status', {deviceId: device['status']})
                else:
                    if server.enable_socketio:
                        print(f"Sending status update for device {deviceId}.")  # For debugging
                        app.logger.info(f"Sending status update for device {deviceId}.")  # For debugging
                        socketio.emit('status', {deviceId: device['status']})
                if server.enable_db_uploading:
                    # Push the status update to Firebase
                    print(f"Pushing status update for device {deviceId} to Firebase.")  # For debugging
                    app.logger.info(f"Pushing status update for device {deviceId} to Firebase.")  # For debugging
                    # server.db.reference('statuses').child(deviceId).set(device)  # Note: commenting out to speed up dev. Code is getting stuck initializing db

            socketio.sleep(5)  # Sleep for 2 seconds

    socketio.start_background_task(send_status_updates)

    return app


def signal_handler(signal, frame):
    print('Stopping the server...')
    exit(0)  # Exit the program


application = create_app()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Register the signal handler
    try:
        print("About to run socketio.run")
        socketio.run(application, host='0.0.0.0', port=5000)
        # socketio.run(application)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)