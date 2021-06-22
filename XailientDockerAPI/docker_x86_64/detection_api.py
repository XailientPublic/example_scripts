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

    

