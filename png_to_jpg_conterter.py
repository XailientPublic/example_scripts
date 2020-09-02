'''A script to convert .png images into .jpg images

Example Usage:
python png_to_jpg_conterter.py --input_path /home/example/project/images --output_path /home/example/project/images_jpg
'''

import os
import glob
import os
from argparse import ArgumentParser
from tqdm import tqdm
import shutil

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
        new_file_name = output_path + "/" + txt_file.split('.')[0].split('/')[-1] + ".jpg"
        shutil.copy(txt_file, new_file_name)
        
if __name__ == '__main__':
    main()