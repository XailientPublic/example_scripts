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

import cv2 as cv
from xailient import roi_bbox
import numpy as np

detectum = roi_bbox.ROIBBoxModel()
cap = cv.VideoCapture("sample.mp4")

while True:
    _, next_frame = cap.read() # Reads the next video frame into memory
    
    bboxes = detectum.process_image(next_frame)

    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    for bbox in bboxes:
        pt1 = (bbox.xmin, bbox.ymin)
        pt2 = (bbox.xmax, bbox.ymax)
        cv.rectangle(next_frame, pt1, pt2, (0, 255, 0))

    cv.imshow("Rendered Video", next_frame)

    key = cv.waitKey(50)
    if key == 27: # Hit ESC key to stop
        break

cap.release()
cv.destroyAllWindows()
