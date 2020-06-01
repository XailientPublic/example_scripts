import cv2 as cv
from xailient import dnn
import numpy as np

THRESHOLD = 0.4 # Value between 0 and 1 for confidence score

detectum = dnn.Detector()
cap = cv.VideoCapture("sample.mp4")

while True:
    _, next_frame = cap.read() # Reads the next video frame into memory
    _, bboxes = detectum.process_frame(next_frame, THRESHOLD) # Extract bbox coords

    # Loop through list (if empty this will be skipped) and overlay green bboxes
    # Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
    for i in bboxes:
        cv.rectangle(next_frame, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)

    cv.imshow("Rendered Video", next_frame)

    key = cv.waitKey(50)
    if key == 27: # Hit ESC key to stop
        break

cap.release()
cv.destroyAllWindows()
