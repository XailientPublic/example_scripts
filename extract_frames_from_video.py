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

'''
This tool allows developers to quickly split a video into frames, with the aim in create training data for model production.

This python script allows developers to either:

Go through each frame and manually save the frames you want (default).
$ python3 video_2_frames <path_to_video>

Save every ith frame in the video.
$ python3 video_2_frames --every <integer> <path_to_video>
'''

from tqdm import tqdm
import cv2 as cv
import argparse
from pathlib import Path

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('path_to_video', type=str, nargs=1,
                    help='Path to the video you want to split')
parser.add_argument('--every', type=int, nargs=1,
                    help='Save every ith frame')
parser.add_argument('--output_path', type=str, nargs=1,
                    help='output path for the directory with frames')        

args = parser.parse_args()
video_path = Path(args.path_to_video[0])
video_name = video_path.stem

if args.every:
    every_ith_frame = args.every[0]

    if every_ith_frame < 1:
        print('Usage Error: --every takes an integer > 0')
        exit(1)

else:
    every_ith_frame = 'None'

# Setup
if args.output_path:
    output_path = Path(args.output_path[0])
else:
    output_path = Path.cwd()

output_path = output_path / video_name
try:
    output_path.mkdir()
except FileExistsError:
    print('Error: Directory ' + video_name + ' already exists in current directory')
    exit(1)
print('Created a new directory called ' + str(video_name) + ' in the current directory')

# Instructions
if every_ith_frame == 'None':
    print('''You are manually choosing the frames to save.
    Press q to exit
    Press s to save a frame
    Press any other key to see next frame
    
If you would like to save every ith frame instead run:
python3 video_2_frames --every <integer> <path_to_video>
''')

# Video Processing
cap = cv.VideoCapture(str(video_path))
vid_len = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

count = 0
for i in tqdm(range(vid_len)):

    ret_val, next_frame = cap.read() # Reads the next video frame into memory

    if ret_val == False:
        break

    if every_ith_frame != 'None':
        if i % every_ith_frame == 0:
            image_name = 'frame_' + str(count) + '.jpg'
            cv.imwrite(str(output_path / image_name), next_frame)
            count += 1
        continue

    cv.imshow('frame'+str(i),next_frame)

    key = cv.waitKey(0)
    if key == 113: # Hit q key to exit
        break
    elif key == 115: # Hit s key to save
        image_name = 'frame_' + str(count) + '.jpg'
        cv.imwrite(str(output_path / image_name), next_frame)
        count += 1
    else:
        pass

    cv.destroyAllWindows()
cap.release()