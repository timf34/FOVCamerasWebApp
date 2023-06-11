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


`docker run -p 5004:5004 opencv-gstreamer:latest`