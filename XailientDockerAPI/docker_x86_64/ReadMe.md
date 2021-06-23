This works is Xailient Python-x86_64 SDK version 1.0.9.

## What is inside this folder

1. [ReadMe.md](ReadMe.md) - This file
2. [Dockerfile](Dockerfile) - Dockerfile to build the docker container
3. [detection_api.py](detection_api.py) - Example python script that sits inside the docker container
4. [reference_implementation.py](reference_implementation.py) - Example python script to send image to API and get back result.

## Preparation

1. Build [Xailient SDK for x86_64](https://xailient-docs.readthedocs.io/en/latest/buildSdk.html) target device.

2. Download and place the Xailient SDK python wheel file into the XailientDockerAPI/docker_x86_64 directory.

3. Add an image on which you want to run inference on to the XailientDockerAPI/docker_x86_64 directory.

4. Download and install [Docker](https://docs.docker.com/get-docker/)

## Build the docker image

1. Copy the XailientDockerAPI/docker_x86_64 folder to the device that you want to build the docker image for.

2. From terminal, go to XailientDockerAPI/docker_x86_64 directory.

3. Ensure that Docker is running.

4. Build the docker image using the following command.

    ``` bash
    docker build -t xailient/detectorsdk:1.0 .
    ```

## Run the docker container that exposes an API for detection

1. Run the docker image for testing using the following command.

    ``` bash
    docker run -p 5001:5001 --name DetectorSDK xailient/detectorsdk:1.0 
    ```

2. Start docker container thereafter

    ``` bash
    docker start -a DetectorSDK
    ```

3. After you have tested end-to-end, you can export the docker image using.

    ``` bash
    docker save xailient/detectorsdk:1.0 > detectorsdk.1.tar
    ```

## Inference on images

1. Run reference_implementation.py python script.