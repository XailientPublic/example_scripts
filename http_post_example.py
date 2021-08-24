"""
Copyright 2021 Xailient Inc.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without 
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import required libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
from xailient import roi_bbox
import cv2 as cv
import requests
import base64
import os
import json
import numpy as np

#By default Low resolution DNN for face detector will be loaded.
#To load the high resolution Face detector please comment the below lines.
detectum = roi_bbox.ROIBBoxModel()

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
    # opencv reads BGR format so we have to convert this to RGB 
    im = cv.cvtColor(im, cv.COLOR_BGR2RGB)

    bboxes = detectum.process_image(im)

    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    for bbox in bboxes:
        pt1 = (bbox.xmin, bbox.ymin)
        pt2 = (bbox.xmax, bbox.ymax)
        cv.rectangle(im, pt1, pt2, (0, 255, 0))

    # If any object detected, send result to API using HTTP post
    if len(bboxes) > 0:
        send_results(im, bboxes)

    # conver it back to RGB
    im = cv.cvtColor(im, cv.COLOR_RGB2BGR)
    cv.imwrite('../data/beatles_output.jpg', im)


main()