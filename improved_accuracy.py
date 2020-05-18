#!/usr/bin/python3

from xailient import dnn
import cv2 as cv

#By default Low resolution DNN for face detector will be loaded.
#To load the high resolution Face detector please comment the below lines.
def main()
	detectum = dnn.Detector()
	THRESHOLD = 0.4 # Value between 0 and 1 for confidence score

	im = cv.imread('../data/beatles.jpg')

	_, bboxes = detectum.process_frame(im, THRESHOLD)
	
	
	# --- uncomment to utilise post-processing --- #
	# 1.
	# post-processing to remove any smaller bboxes appearing inside larger ones
	# -- remove_inside_bboxes(bboxes)
	# 2. 
	# post-processing to combine any larger bboxes
	# -- 2. combine_bboxes(bboxes)
	
	
	# Loop through list (if empty this will be skipped) and overlay green bboxes
	# Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
	for i in bboxes:
		cv.rectangle(im, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)

	cv.imwrite('../data/beatles_output.jpg', im)

	
# post-processing to remove any smaller bboxes appearing inside larger ones	
def remove_inside_bboxes(bboxes):
	filtered_bboxes = []
	for test_bbox in bboxes:
		if not smaller_bbox(test_bbox, bboxes):
			filtered_bboxes.append(test_bbox)
	bboxes = filtered_bboxes

def smaller_bbox(test_bbox, bboxes):
	t_xmin = test_bbox[0]
	t_ymin = test_bbox[1]
	t_xmax = test_bbox[2]
	t_ymax = test_bbox[3]

	for bbox in bboxes:
	
		if list(test_bbox) == list(bbox):
			continue
			
		b_xmin = bbox[0]
		b_ymin = bbox[1]
		b_xmax = bbox[2]
		b_ymax = bbox[3]
		
		if b_xmin <= t_xmin <= b_xmax and b_xmin <= t_xmax <= b_xmax \
		and b_ymin <= t_ymin <= b_ymax and b_ymin <= t_ymax <= b_ymax:
			return 1
			
	return 0
	
	
# post-processing
# Given a number of bboxes the aim is to combine any which are overlapping
def combine_bboxes(bboxes):
	filtered = []
	combined = []
	not_stop = 1
	match = 0
	while(not_stop):
		not_stop = 0
		
		for bboxA in bboxes:
			bboxA = list(bboxA)
			for bboxB in bboxes:
				bboxB = list(bboxB)
				if bboxA != bboxB:
					# determine the (x, y)-coordinates of the intersection rectangle
					xmin = max(bboxA[0], bboxB[0])
					ymin = max(bboxA[1], bboxB[1])
					xmax = min(bboxA[2], bboxB[2])
					ymax = min(bboxA[3], bboxB[3])
					
					# compute the area of intersection rectangle
					interArea = max(0, xmax - xmin) * max(0, ymax - ymin)
					
					# compute coordinates if larger bbox
					if interArea != 0:
						xmin = min(bboxA[0], bboxB[0])
						ymin = min(bboxA[1], bboxB[1])
						xmax = max(bboxA[2], bboxB[2])
						ymax = max(bboxA[3], bboxB[3])
						
						if [xmin,ymin,xmax,ymax] not in combined:
							combined.append([xmin,ymin,xmax,ymax])
							
						match = 1
						not_stop = 1
			
			if match == 0:
				if bboxA not in filtered:
					filtered.append(bboxA)
			match = 0
			
		bboxes = combined.copy()
		combined = []
				
	return filtered
	
	
	
if __name__ == "__main__":
	main()
	

