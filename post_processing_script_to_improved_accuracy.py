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

from xailient import roi_bbox
import cv2 as cv

#By default Low resolution DNN for face detector will be loaded.
#To load the high resolution Face detector please comment the below lines.
def main():
	detectum = roi_bbox.ROIBBoxModel()

	im = cv.imread('../data/beatles.jpg')
	# opencv reads BGR format so we have to convert this to RGB
	im = cv2.cvtColor(im, cv.COLOR_BGR2RGB)

	bboxes = detectum.process_image(im)


	# --- uncomment to utilise post-processing --- #
	# 1.
	# Post-processing to remove any bboxes whose coordinates are inside larger bboxes.
	# bboxes = remove_inside_bboxes(bboxes) # uncomment me!!!
	# 2.
	# Post-processing that combines any two overlapping bboxes into one larger bbox.
	# bboxes = combine_bboxes(bboxes) # uncomment me!!!


	# Loop through list (if empty this will be skipped) and overlay green bboxes
	# Format of bboxes is: xmin, ymin (top left), xmax, ymax (bottom right)
	for bbox in bboxes:
		pt1 = (bbox.xmin, bbox.ymin)
		pt2 = (bbox.xmax, bbox.ymax)
		cv.rectangle(im, pt1, pt2, (0, 255, 0))	

	# conver it back to RGB
	im = cv.cvtColor(im, cv.COLOR_RGB2BGR)
	cv.imwrite('../data/beatles_output.jpg', im)


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
		not_matched_bboxes = []

	return bboxes



if __name__ == "__main__":
	main()


