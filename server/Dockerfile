FROM ubuntu:20.04

# Avoid timezone prompt during packages installation
ARG DEBIAN_FRONTEND=noninteractive

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    qt5-default \
    unzip \
    yasm \
    pkg-config \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavformat-dev \
    libavcodec-dev \
    libavutil-dev \
    libpostproc-dev \
    libswscale-dev \
    libeigen3-dev \
    libtbb-dev \
    libgtk2.0-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libavresample-dev \
    && rm -rf /var/lib/apt/lists/*

# Download opencv and opencv_contrib
RUN wget https://github.com/opencv/opencv/archive/4.5.1.zip \
    && unzip 4.5.1.zip \
    && rm 4.5.1.zip \
    && mv opencv-4.5.1 OpenCV \
    && wget https://github.com/opencv/opencv_contrib/archive/4.5.1.zip \
    && unzip 4.5.1.zip \
    && rm 4.5.1.zip \
    && mv opencv_contrib-4.5.1 OpenCV/opencv_contrib

WORKDIR OpenCV
# Prepare build 
RUN mkdir build
WORKDIR build
RUN cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D WITH_TBB=ON \
    -D WITH_V4L=ON \
    -D WITH_QT=ON \
    -D WITH_OPENGL=ON \
    -D WITH_VTK=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_PC_FILE_NAME=opencv.pc \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_PYTHON3_INSTALL_PATH=/usr/local/lib/python3.8/site-packages \
    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    -D WITH_GSTREAMER=ON ..

# Compile and install OpenCV with contrib modules
RUN make -j4 && make install && ldconfig

WORKDIR /
# Cleanup
RUN rm -rf OpenCV

# ...
# After building and installing OpenCV

# Set working directory
WORKDIR /app

# # Copy requirements file
# COPY requirements.txt ./

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . .

# Expose Flask port
EXPOSE 5000

# # Set the default command to run your application
# CMD ["python", "server.py"]
