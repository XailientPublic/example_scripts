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

'''A script to convert .png images into .jpg images

Example Usage:
python png_to_jpg_converter.py --input_path /home/example/project/images --output_path /home/example/project/images_jpg
'''

import os
import glob
import os
from argparse import ArgumentParser
from tqdm import tqdm
import shutil
import cv2

def main():
    args = parse_args()

    png_to_jpg(args.input_path, args.output_path)
    print("Converted images to .jpg")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--input_path', required=True)
    parser.add_argument('--output_path', required=True)
    args = parser.parse_args()
    return args

def png_to_jpg(input_path, output_path):

    png_images_list = glob.glob(input_path + '/*.png')

    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    print(type(png_images_list))
    for txt_file in tqdm(png_images_list, total=len(png_images_list)):
        img = cv2.imread(txt_file)
        new_file_name = output_path + "/" + txt_file.split('.')[0].split('/')[-1] + ".jpg"
        cv2.imwrite(new_file_name, img)
        
if __name__ == '__main__':
    main()