GStreamer script for streaming to laptop via GStreamer from laptop:

*Note that you need to run it from Powershell! Not CMD!*

` gst-launch-1.0 -ev videotestsrc pattern=ball ! video/x-raw,width=1280,height=720 ! x264enc speed-preset=ultrafast tune=zerolatency ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=192.168.110.1 port=1234`

gst-launch-1.0 -ev videotestsrc pattern=ball ! video/x-raw,width=1280,height=720 ! x264enc speed-preset=ultrafast tune=zerolatency ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=5000

Sample code for sending and receiving in my terminal, on a separate port:
Sending:
gst-launch-1.0 -ev videotestsrc pattern=ball ! video/x-raw,width=1280,height=720 ! x264enc speed-preset=ultrafast tune=zerolatency ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=5001 

Receiving:
gst-launch-1.0 -v udpsrc port=5001 ! application/x-rtp,encoding-name=H264,payload=96 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! autovideosink



**Docker commands:**

`docker build -t opencv-gstreamer:latest .`


`docker run -it --name opencv_container opencv-gstreamer:latest bash`

`docker run -it -v ${PWD}:/app -p 5000:5000 opencv-gstreamer:latest bash`


`docker run -p 5000:5000 opencv-gstreamer:latest`


**Notes for using Docker**

1. Build Docker image
    - `docker build -t opencv-gstreamer:latest .`
1. Run Docker image
    - `docker run -p 5000:5000 opencv-gstreamer:latest`
      - Note that this command assumes that you are running the server on port 5000. It also assumes you have a `CMD` in 
        your Dockerfile that runs the server.

We will now have the server running, we will still need to set up the client in a separate terminal running `npm start`. 


