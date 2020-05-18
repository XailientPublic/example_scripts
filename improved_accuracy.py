#!/usr/bin/python3

from xailient import dnn
import cv2 as cv

#By default Low resolution DNN for face detector will be loaded.
#To load the high resolution Face detector please comment the below lines.
def main():
	detectum = dnn.Detector()
	THRESHOLD = 0.4 # Value between 0 and 1 for confidence score

	im = cv.imread('../data/party.jpeg')

	_, bboxes = detectum.process_frame(im, THRESHOLD)


	# --- uncomment to utilise post-processing --- #
	# 1.
	# Post-processing to remove any bboxes whose coordinates are inside larger bboxes.
	# bboxes = remove_inside_bboxes(bboxes) # uncomment me!!!
	# 2.
	# Post-processing that combines any two overlapping bboxes into one larger bbox.
	# bboxes = combine_bboxes(bboxes) # uncomment me!!!


	# Loop through list (if empty this will be skipped) and overlay green bboxes
	# Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
	for i in bboxes:
		cv.rectangle(im, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 3)

	cv.imwrite('../data/party_remove_output.jpeg', im)


#######################
### POST-PROCESSING ###
#######################

# 1. Post-processing to remove any bboxes whose coordinates are inside larger bboxes.	
def remove_inside_bboxes(bboxes):
	filtered_bboxes = []
	for test_bbox in bboxes:
		if not smaller_bbox(test_bbox, bboxes):
			filtered_bboxes.append(test_bbox)
	return filtered_bboxes

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

		# Return True if test_bbox coordinates is inside another bounding box
		if b_xmin <= t_xmin <= b_xmax and b_xmin <= t_xmax <= b_xmax \
		and b_ymin <= t_ymin <= b_ymax and b_ymin <= t_ymax <= b_ymax:
			return True
	return False


# 2. Post-processing that combines any two overlapping bboxes into one larger bbox.
def combine_bboxes(bboxes):
	not_matched_bboxes = []
	combined = []
	loop_again = True
	match = False

	while(loop_again):
		loop_again = False

		for bboxA in bboxes:
			for bboxB in bboxes:

				if bboxA != bboxB: # ignore the same bbox
					# determine the (x, y)-coordinates of the intersection rectangle
					xmin = max(bboxA[0], bboxB[0])
					ymin = max(bboxA[1], bboxB[1])
					xmax = min(bboxA[2], bboxB[2])
					ymax = min(bboxA[3], bboxB[3])

					# compute the area of intersection rectangle
					interArea = max(0, xmax - xmin) * max(0, ymax - ymin)

					# If intersection > 0, compute coordinates of combined bbox
					if interArea > 0:
						xmin = min(bboxA[0], bboxB[0])
						ymin = min(bboxA[1], bboxB[1])
						xmax = max(bboxA[2], bboxB[2])
						ymax = max(bboxA[3], bboxB[3])

						if [xmin,ymin,xmax,ymax] not in combined:
							combined.append([xmin,ymin,xmax,ymax])

						match = True
						loop_again = True # We need to loop again to ensure this combined bbox
								  # is not overlapping with another bbox

			if match == False: # if bboxA doesn't overlap with any other bbox in this current interation
				if bboxA not in not_matched_bboxes:
					not_matched_bboxes.append(bboxA)
			match = False

		bboxes = combined.copy()
		bboxes.extend(not_matched_bboxes)
		combined = []

	return bboxes



if __name__ == "__main__":
	main()


