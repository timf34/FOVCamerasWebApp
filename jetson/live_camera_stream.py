import cv2
import os
import sys
import requests
import signal
from utils.utility_funcs import load_env

# Function to handle cleanup
def clean_up(signal_received, frame):
    global cap
    print("Signal received. Closing resources...")
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

# Register signals to be caught
signal.signal(signal.SIGINT, clean_up)   # Signal 2 (CTRL+C)
signal.signal(signal.SIGTERM, clean_up)  # Signal 15 (terminate)

load_env()
URL = os.environ.get('REACT_APP_URL')

# Check the operating system
if os.name == 'nt':
    cap = cv2.VideoCapture(0)  # Windows
else:
    cap = cv2.VideoCapture(
        f'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
        f'nvvidconv ! video/x-raw, width={str(1920)}, height={str(1080)}, format=BGRx ! '
        f'videoconvert ! video/x-raw, format=BGR ! appsink'
    )

while True:
    # Read a frame from the camera
    print("Reading frame...")
    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame.")
        break

    frame = cv2.resize(frame, (1920, 1080))  # Resize frame to FHD
    ret, jpeg = cv2.imencode('.jpg', frame)
    data = jpeg.tobytes()

    if not ret:
        print("Failed to encode frame.")
        break

    # cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # close on 'q' key press
        print("Received 'q' key press. Exiting...")
        break

    response = requests.post(f'{URL}/api/image', data=data, headers={'content-type': 'image/jpeg'})

    if response.status_code != 200:
        print("Failed to send frame.")
        print("Response code: ", response.status_code)
        break

# Clean up resources if the loop ends naturally
cap.release()
cv2.destroyAllWindows()
