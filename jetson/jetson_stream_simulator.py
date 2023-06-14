import cv2
import os 
import socketio
from utils import load_env


load_env()
URL = os.environ.get('REACT_APP_URL')

# Check the operating system
if os.name == 'nt':
    cap = cv2.VideoCapture(0)  # Windows 
else:
    cap = cv2.VideoCapture(
        f'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
        f'nvvidconv ! video/x-raw, width={str(640)}, height={str(640)}, format=BGRx ! '
        f'videoconvert ! video/x-raw, format=BGR ! appsink'
    )
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the server.")

@sio.event
def disconnect():
    print("Disconnected from the server.")

sio.connect(URL)  # replace with the URL of your server

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame.")
        break

    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("Failed to encode frame.")
        break

    # cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # close on 'q' key press
        print("Received 'q' key press. Exiting...")
        break

    sio.emit('frame', {'image': jpeg.tobytes()})

sio.disconnect()
