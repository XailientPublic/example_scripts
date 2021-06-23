# Docker File v1.2

FROM python:3.7

# Download and install dependencies
RUN mkdir /app && \
apt-get update && \
apt-get install -y ffmpeg

RUN apt-get install -y python3.7 \
python3.7-dev \
python3-pip \
python3-setuptools \
gstreamer-1.0 \
v4l-utils \
libopus-dev \
libvpx-dev \
libsrtp2-dev \
libopencv-dev \
libatlas3-base \
libatlas-base-dev \
libavformat-dev \
libswscale-dev \
libqtgui4 \
libqt4-test \
libavdevice-dev \
libavfilter-dev \
libavcodec-dev \
liblapack3 

RUN python3.7 -m pip install https://dl.google.com/coral/python/tflite_runtime-1.14.0-cp37-cp37m-linux_x86_64.whl
RUN python3.7 -m pip install p_tqdm
RUN python3.7 -m pip install pathos

RUN python3.7 -m pip install wheel
RUN python3.7 -m pip install Flask

RUN apt-get install -q -y rsyslog
RUN apt-get install net-tools

RUN apt-get update && apt-get install -y lsb-release && apt-get clean all
RUN apt-get install -y curl

RUN python3.7 -m pip install opencv-python

RUN python3.7 -m pip install requests
RUN python3.7 -m pip install imutils

# set the working directory
WORKDIR "/app"

# Copy Xailient Detector SDK
COPY xailient-1.0.9-py3-none-linux_x86_64.whl .

# Install Xailient Detector SDK
RUN python3.7 -m pip install /app/xailient-1.0.9-py3-none-linux_x86_64.whl

# Copy server code
COPY start_server.sh .
COPY detection_api.py .

# provision environment
RUN ["chmod", "+x", "./start_server.sh"]
ENTRYPOINT ["/app/start_server.sh" ]