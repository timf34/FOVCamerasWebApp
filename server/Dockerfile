# Set the base image
FROM ubuntu:20.04

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update

# Install python3 and pip3
RUN apt install -y python3 python3-pip

# Install necessary build tools and libraries
RUN apt install -y build-essential cmake git pkg-config libgtk-3-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev \
    gfortran openexr libatlas-base-dev python3-dev python3-numpy \
    libtbb2 libtbb-dev libdc1394-22-dev libopenexr-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev \
    libgstreamer1.0-0 \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    libgstrtspserver-1.0-0 \
    libgstrtspserver-1.0-dev \
    pkg-config \
    libcairo2-dev \
    ffmpeg \
    libsm6 \
    libxext6 \

# Clone OpenCV's and OpenCV contrib's repositories
RUN git clone https://github.com/opencv/opencv.git
RUN git clone https://github.com/opencv/opencv_contrib.git

# Build and install OpenCV
WORKDIR opencv
RUN mkdir build
WORKDIR build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
    -D WITH_GSTREAMER=ON \
    -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
    -D BUILD_EXAMPLES=OFF ..
RUN make -j$(nproc)
RUN make install

# Add the installed libs to the linker search paths
RUN ldconfig

# Set work directory to /app
WORKDIR /app

# Copy requirements.txt and install the requirements
RUN pip3 install Flask flask-cors flask-socketio firebase-admin

# Expose the necessary port
EXPOSE 5000

# Set up command to run your server.py script using Python 3
# CMD ["flask", "run","--host","0.0.0.0","--port","5000"]
# CMD ["python3", "app.py"]

CMD ["python3", "server.py"]
