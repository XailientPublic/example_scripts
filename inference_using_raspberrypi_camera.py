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

# This script has been tested using a Raspberry Pi Camera Modeule v1.3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import math
from xailient import roi_bbox
import numpy as np

detectum = roi_bbox.ROIBBoxModel()

# initialize the camera and grab a reference to the raw camera capture
RES_W = 640 # 1280 # 640 # 256 # 320 # 480 # pixels
RES_H = 480 # 720 # 480 # 144 # 240 # 360 # pixels

camera = PiCamera()
camera.resolution = (RES_W, RES_H)
camera.framerate = 30 # FPS
rawCapture = PiRGBArray(camera, size=(RES_W, RES_H))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    im = np.copy(image) # Create copy since cant modify orig

    # Return's list of bounding box co-ordinates
    bboxes = detectum.process_image(im)

    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    for bbox in bboxes:
        pt1 = (bbox.xmin, bbox.ymin)
        pt2 = (bbox.xmax, bbox.ymax)
        cv.rectangle(im, pt1, pt2, (0, 255, 0))

    # show the frame
    cv.imshow("Frame", im)
    key = cv.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break