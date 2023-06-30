import cv2
import os
import requests
import time
from utils.utility_funcs import load_env

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

while True:
    # Read a frame from the camera
    print("Reading frame...")
    # Before reading the frame
    start_time = time.time()
    ret, frame = cap.read()
    end_time = time.time()
    print("Time taken to read frame: ", end_time - start_time)


    if not ret:
        print("Failed to read frame.")
        break

    # Encode the frame as JPEG
    ret, jpeg = cv2.imencode('.jpg', frame)

    if not ret:
        print("Failed to encode frame.")
        break

    # cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # close on 'q' key press
        print("Received 'q' key press. Exiting...")
        break

    # Send the JPEG image to the server
    start_time = time.time()
    response = requests.post(f'{URL}/api/image', data=jpeg.tobytes(), headers={'content-type': 'image/jpeg'})
    end_time = time.time()
    print("Time taken to send frame: ", end_time - start_time)

    if response.status_code != 200:
        print("Failed to send frame.")
        print("Response code: ", response.status_code)
        break