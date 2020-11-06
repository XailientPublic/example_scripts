from copy import copy
import shutil
from tqdm import tqdm
import argparse
import pandas as pd
import cv2
import numpy as np
import os
import json


def process_platerecog_json(json_path, output_dir, labels_df):
    """
        Given a json file from alpr recognition, this function will read and convert
        the json response to xailient dataframe format and append to labels_df

        :Param json_path: path of the .json file
        :Param output_dir: path of the image file to be saved
        :Param labels_df: Dataframe in xailient format

        :Return labels_df: Dataframe in xailient format with addition row from json file
    """
    image_dir = os.path.dirname(json_path)
    processed_images = {}
    with open(json_path, "r") as json_file:
        result_json = json.load(json_file)
        for result in result_json:
            filepath = result["filename"]
            filename = os.path.basename(filepath)

            if filename not in processed_images:
                out_filename = filename.replace(".jpg", "_0.jpg")
                # Ensure duplicating image names are not overwriting eachother
                image_path = os.path.join(image_dir, filename)
                output_path = os.path.join(output_dir, out_filename)
                while os.path.isfile(output_path):
                    base_filename, extension = os.path.splitext(out_filename)
                    index = int(base_filename.split("_")[-1])
                    index += 1
                    out_filename = base_filename[:-2] + "_{}".format(index) + extension
                    output_path = os.path.join(output_dir, out_filename)
                shutil.copyfile(image_path, output_path)
                processed_images[filename] = out_filename
                filename = out_filename
            else:
                filename = processed_images[filename]

            try:
                plate_info = result["results"]
            except KeyError:
                continue

            plate_number = plate_info[0]["plate"]
            bounding_box = plate_info[0]["box"]

            labels_df = labels_df.append({"image_name": filename, "class": "plate", "xmin": bounding_box["xmin"],
                                        "ymin": bounding_box["ymin"], "xmax": bounding_box["xmax"], "ymax": bounding_box["ymax"], "text": plate_number},
                                       ignore_index=True)
    return labels_df


def iterate_through_dirs(curr_dir, output_dir, labels_df):
    """
        This function iterate through all the subdirectories with given main directory
        All the image under the subdirectories are processed and move to output_dir
        All the json file under the subdirectories are processed and append to the labels_df in xailient format

        :Param curr_dir: The current directory used to iterate its subdirectory
        :Param output_dir: The output directory where the processed image should locate, ideally should be 'dataset_name/data'

        :Return labels_df: Dataframe in xailient format
    """
    if curr_dir.endswith(".json"):
        labels_df = process_platerecog_json(curr_dir, output_dir, labels_df)
        print("processed: ", curr_dir)
        return labels_df

    elif os.path.isdir(curr_dir):
        sub_dirs = os.listdir(curr_dir)
        for item in sub_dirs:
            directory = os.path.join(curr_dir, item)
            labels_df = iterate_through_dirs(directory, output_dir, labels_df)
        return labels_df

    else:
        return labels_df


def convert_platerecog_to_xailient(input_dataset_path, output_dataset_path):
    print("start processing...")
    columns = ["image_name", "class", "xmin", "ymin", "xmax", "ymax", "text"]
    xailient_dataset_df = pd.DataFrame(columns=columns)

    output_dataset_image_path = os.path.join(output_dataset_path, "data")
    output_dataset_label_path = os.path.join(output_dataset_path, "labels.csv")
    os.makedirs(output_dataset_image_path, exist_ok=True)

    xailient_dataset_df = iterate_through_dirs(input_dataset_path,
                                               output_dataset_image_path,
                                               xailient_dataset_df)
    xailient_dataset_df.to_csv(output_dataset_label_path, index=False)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", dest="input_dir")
    parser.add_argument("--output_dir", dest="output_dir")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    # input dataset directory info
    convert_platerecog_to_xailient(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
