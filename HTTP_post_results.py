# Import required libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
from xailient import dnn
import cv2 as cv
import requests
import base64
import os
import json
import numpy as np

#By default Low resolution DNN for face detector will be loaded.
#To load the high resolution Face detector please comment the below lines.
detectum = dnn.Detector()

THRESHOLD = 0.45 # Value between 0 and 1 for confidence score

# api-endpoint
API_ENDPOINT = "<ENTER YOUR API ENDPOINT HERE>"
API_KEY = "<ENTER YOUR API KEY HERE, IF THERE IS NO API KEY, LEAVE THIS EMPY>"

def send_results(frame, bboxes):
    """
    This function is to send results to a web API using HTTP post.

    Parameters:
    
    frame: image as numpy array

    bboxes: list of list
    """

    # prepare headers for http request
    content_type = "application/json"
    headers = {}
    headers["content-type"] = content_type

    if API_KEY != "":
        headers["x-api-key"] = API_KEY

    # encode image to base64 string
    base64_string_image = encode(frame)

    # data to be sent to api 
    data = {
        "message" : "Object detected",
        "image": base64_string_image,
        "bboxes": bboxes
    }

    # convert the data to be sent to json
    data_json = json.dumps(data)

    print("Data to send to API: {}".format(data_json))

    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data_json, headers = headers) 

    print("Response: {}".format(r))
    print("Response body: {}".format(r.text))

    if r.status_code == 200:
        print("Data sent to API successfully!")
        return True
    else:
        print("Failed to send data to API!")
        return False

def encode(image):
    """
    Encode image as base64 string.
    """

    file_name = "temp.png"
    base64_message = ""
    
    cv.imwrite(file_name, image)

    with open(file_name, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_message = base64_encoded_data.decode('utf-8')
    
    if os.path.isfile(file_name):
        print("Delete temp file")
        os.remove(file_name)
    
    return base64_message

def main():
    im = cv.imread('../data/beatles.jpg')

    _, bboxes = detectum.process_frame(im, THRESHOLD)

    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    for i in bboxes:
        cv.rectangle(im, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)
    
    # If any object detected, send result to API using HTTP post
    if len(bboxes) > 0:
        send_results(im, bboxes)

    cv.imwrite('../data/beatles_output.jpg', im)

main()