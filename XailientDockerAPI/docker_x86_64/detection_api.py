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

# import the necessary packages
import time
import numpy as np
import base64
import json
import cv2
import os
import io
import flask
from xailient import dnn
from flask import Flask, jsonify, request
import numpy

app = Flask(__name__)
detectum = dnn.Detector()

@app.route("/v1/detector", methods=["POST"])
def detector():

    try:
        data = request.files['upload']
        if data != None:
            print("Received image as file byte")
            # check if file was uploaded as filebyte or base64 string
            img = cv2.imdecode(numpy.frombuffer(data.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    except:
        print("Received image as base64 string")
        data = json.loads(request.data)

        base64_encoded_img = data['upload']

        img = decode(base64_encoded_img)

    _, bboxes = detectum.process_frame(img)
    
    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    response = {}
    results = []

    for bbox_ in bboxes:
        bbox = {}
        bbox["xmin"] = int(bbox_[0])
        bbox["ymin"] = int(bbox_[1])
        bbox["xmax"] = int(bbox_[2])
        bbox["ymax"] = int(bbox_[3])

        results.append(
            {"bbox": bbox}
        )

    response["results"] = results

    return jsonify(response)

def decode(base64_img):
    filename = 'decoded_image.png'
    base64_img_bytes = base64_img.encode('utf-8')
    with open(filename, 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)

    decoded_img = cv2.imread(filename)
    try:
        os.remove(filename)
    except Exception as ex:
        print("Exception removing temp file {}".format(ex))
        
    return decoded_img

if __name__=="__main__":
    app.run("0.0.0.0", port=5001)
    # app.run()

    

