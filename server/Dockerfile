# Set the base image
FROM ubuntu:20.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository and install required packages
RUN apt update && apt install -y \
    python3 python3-pip \
    build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libopenexr-dev 

# Add the installed libs to the linker search paths
RUN ldconfig

# Set work directory to /app
WORKDIR /app

# Install the requirements
RUN pip3 install Flask flask-cors flask-socketio firebase-admin opencv-python

# Expose the necessary port
EXPOSE 5000

CMD ["python3", "application.py"]
