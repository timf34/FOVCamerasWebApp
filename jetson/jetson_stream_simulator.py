import cv2
import requests 

# Capture video from the webcam
cap = cv2.VideoCapture(f'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=60/1 ! '
                f'nvvidconv ! video/x-raw, width={str(1920)}, height={str(1080)}, format=BGRx ! '
                f'videoconvert ! video/x-raw, format=BGR ! appsink')

while True:
    # Read a frame from the camera
    print("Reading frame...")
    ret, frame = cap.read()
    
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
    response = requests.post('http://192.168.253.1:5000/api/image', data=jpeg.tobytes(), headers={'content-type': 'image/jpeg'})
    
    if response.status_code != 200:
        print("Failed to send frame.")
        break
