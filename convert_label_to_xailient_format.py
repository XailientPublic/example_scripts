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

'''A script to convert different annotations formats to the format required by the Xailient Console.
Currently supported formats for this conversion script are pascalvoc/labelimg, labelme, coco, yolo, and aws formats.
Choices for input_format argument are 'voc', 'coco', 'labelme', 'yolo', 'aws'
For annotations present in a single file (e.g. COCO), input_path represents the path to the JSON file,
while for separate annotations for each image (e.g. Pascal VOC, yolo, labelme, aws), input_path represents
the path to the folder where the annotations reside.
The output_path is the path and name of the converted xailient annotations.
Example Usage:
python convert_label_to_xailient_format.py --input_path /home/example/project/data --input_format voc --output_path /home/example/project/data/xailient_labels.csv
python convert_label_to_xailient_format.py --input_path /home/example/project/data/coco_annotations.json --input_format coco --output_path /home/example/project/data/xailient_labels.csv
python convert_label_to_xailient_format.py --input_path /home/example/project/data/output.manifest --input_format aws --output_path /home/example/project/data/xailient_labels.csv --aws_labeling_job_name my_labeling_job --is_labeling_adjustment_job False'''

import csv
import json
import re

import os
from argparse import ArgumentParser

from PIL import Image

import pandas as pd
from tqdm import tqdm

from xml.etree import ElementTree


def main():
    args = parse_args()

    if args.input_format == 'voc':
        convert_pascal_voc_to_xailient(args.input_path, args.output_path)

    elif args.input_format == 'coco':
        convert_coco_to_xailient(args.input_path, args.output_path)

    elif args.input_format == 'labelme':
        convert_labelme_to_xailient(args.input_path, args.output_path)

    elif args.input_format == 'yolo':
        convert_yolo_to_xailient(args.input_path, args.output_path)

    elif args.input_format == 'aws':
        convert_aws_to_xailient(args.input_path, args.output_path, args.aws_labeling_job_name, True if args.is_labeling_adjustment_job else False)

    elif args.input_format == 'hasty':
        convert_hasty_to_xailient(args.input_path, args.output_path)

    elif args.input_format == 'xailient' and args.output_format == 'coco':
        convert_xailient_to_coco(args.input_path, args.output_path, args.image_dir if "image_dir" in args else None)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--input_path', required=True)
    parser.add_argument('--input_format', required=True, choices=['voc', 'coco', 'labelme', 'yolo', 'aws', 'hasty', 'txt', 'xailient'])
    parser.add_argument('--output_format', required=True, choices=['coco', 'xailient'], default='xailient')
    parser.add_argument('--output_path', required=True)
    parser.add_argument('--image_dir', required=False, default="")
    parser.add_argument('--is_labeling_adjustment_job', required=False, default=False)
    parser.add_argument('--aws_labeling_job_name', required=False)
    args = parser.parse_args()
    return args

def convert_xailient_to_coco(input_path, output_path, image_dir):
    """
    This function converts xailient label format to coco label format
    """
    data = pd.read_csv(input_path)

    images = []
    categories = []
    annotations = []

    category = {}

    data['fileid'] = data['image_name'].astype('category').cat.codes
    data['categoryid']= pd.Categorical(data['class'],ordered= True).codes
    data['categoryid'] = data['categoryid']+1
    data['annid'] = data.index
    data['filename'] = data['image_name']
    data['image_dir'] = image_dir

    def get_image_dimensions(image_dir, filename):
        """
        Returns height, width of image
        """
        if image_dir is not None and os.path.isdir(image_dir):
            image_full_path = os.path.join(image_dir, filename)
            im = Image.open(image_full_path)
            w, h = im.size
            return h, w
        else:
            return 0, 0

    def attributes(occluded=False):
        attributes = {}
        attributes["occluded"] = occluded
        attributes["rotation"] = 0.0
        return attributes

    def image(row):
        image = {}
        image["height"], image["width"] = get_image_dimensions(row.image_dir, row.filename)
        image["id"] = row.fileid
        image["file_name"] = row.filename
        return image

    def category(row):
        category = {}
        category["supercategory"] = 'None'
        category["id"] = row.categoryid
        category["name"] = row[2]
        return category

    def annotation(row):
        annotation = {}
        area = (row.xmax -row.xmin)*(row.ymax - row.ymin)
        annotation["segmentation"] = []
        annotation["iscrowd"] = 0
        annotation["attributes"] = attributes()
        annotation["area"] = area
        annotation["image_id"] = row.fileid

        annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]

        annotation["category_id"] = row.categoryid
        annotation["id"] = row.annid
        return annotation

    for row in data.itertuples():
        annotations.append(annotation(row))

    imagedf = data.drop_duplicates(subset=['fileid']).sort_values(by='fileid')
    for row in imagedf.itertuples():
        images.append(image(row))

    catdf = data.drop_duplicates(subset=['categoryid']).sort_values(by='categoryid')
    for row in catdf.itertuples():
        categories.append(category(row))

    data_coco = {}
    data_coco["images"] = images
    data_coco["categories"] = categories
    data_coco["annotations"] = annotations
    json.dump(data_coco, open(output_path, "w"), indent=4)

def convert_hasty_to_xailient(input_path, output_path):

    with open(input_path) as f:
        data = json.load(f)

    xailient_df_annotation = pd.DataFrame(columns=['image_name', 'class', 'xmin', 'xmax', 'ymin', 'ymax'])

    for i in data['images']:
        image_id = i['image_name']
        labels = i['labels']

        print(len(labels))
        for label in labels:
            category_id = label['class_name']
            x_min = label['bbox'][0]
            y_min = label['bbox'][1]
            x_max = label['bbox'][2]
            y_max = label['bbox'][3]

            x_min = int(x_min)
            y_min = int(y_min)
            x_max = int(x_max)
            y_max = int(y_max)
            print("{} -> {} {} {} {}".format(label['bbox'], x_min, x_max, y_min, y_max))
            
            xailient_df_annotation = xailient_df_annotation.append(
                {'image_name': image_id, 'class': category_id, 'xmin': x_min, 'xmax': x_max, 'ymin': y_min,
                'ymax': y_max}, ignore_index=True)

    xailient_df_annotation.to_csv(output_path, index=False)

def convert_pascal_voc_to_xailient(input_xml_folder, output_csv_file):

    with open(output_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(
            ['image_name', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])

        # Reads all xml files in single folder
        for file in os.listdir(input_xml_folder):
            tree = ElementTree.parse(input_xml_folder + '/' + file)
            root = tree.getroot()

            # Grab boundary box and class data for each object in file
            for child in root.findall('object'):

                boundary_box = child.find('bndbox')

                filename = root.find('filename').text

                currentClass = child.find('name').text

                xmin = boundary_box.find('xmin').text
                ymin = boundary_box.find('ymin').text
                xmax = boundary_box.find('xmax').text
                ymax = boundary_box.find('ymax').text

                writer.writerow(
                    [filename, currentClass, xmin, ymin, xmax, ymax])

def convert_aws_to_xailient(input_path, output_path, labeling_job_name, islabellingAdjustmentJob=False):

    if islabellingAdjustmentJob:
        labeling_job_name = labeling_job_name + "-label-adjustment"

    with open(input_path) as f:
        lines = f.readlines() 

    columns = ['image_name', 'xmin', 'xmax', 'ymin', 'ymax', 'class']
    xailient_df_annotation = pd.DataFrame(columns=columns)

    for line in tqdm(lines, total=len(lines)): 

        # Convert string to json
        json_data = json.loads(line.strip()) 
        
        # Get image file name from source-ref
        source_ref = json_data['source-ref']
        file_name = source_ref.split("/")[-1]

        if labeling_job_name in json_data:
            if 'annotations' in json_data[labeling_job_name]:
                if len(json_data[labeling_job_name]['annotations']) == 0:
                    print("no annotation")
                    class_name = ""
                    x_min = 0
                    y_min = 0
                    x_max = 0
                    y_max = 0
                    x_min = int(x_min)
                    y_min = int(y_min)
                    x_max = int(x_max)
                    y_max = int(y_max)

                    xailient_df_annotation = xailient_df_annotation.append(
                        {'image_name': file_name, 'class': class_name, 'xmin': x_min, 'xmax': x_max, 'ymin': y_min,
                        'ymax': y_max}, ignore_index=True)

                else:
                    for i in json_data[labeling_job_name]['annotations']:
                        class_id = i['class_id']
                        x_min = i['left']
                        y_min = i['top']
                        x_max = x_min + i['width']
                        y_max = y_min + i['height']
                        x_min = int(x_min)
                        y_min = int(y_min)
                        x_max = int(x_max)
                        y_max = int(y_max)

                        # Get class name from class mapping
                        class_name = json_data[labeling_job_name + "-metadata"]['class-map'][str(class_id)]
                        
                        xailient_df_annotation = xailient_df_annotation.append(
                            {'image_name': file_name, 'class': class_name, 'xmin': x_min, 'xmax': x_max, 'ymin': y_min,
                            'ymax': y_max}, ignore_index=True)

        elif labeling_job_name+"-metadata" in json_data:
            if 'failure-reason' in json_data[labeling_job_name+"-metadata"]:
                print(json_data[labeling_job_name+"-metadata"]['failure-reason'])

    final_df = xailient_df_annotation[columns]
    final_df.to_csv(output_path, index=False)


def convert_labelme_to_xailient(input_json_folder, output_csv_file):

    with open(output_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['image_name', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])

        for file in os.listdir(input_json_folder):

            with open(input_json_folder + '/' + file) as json_file:

                data = json.load(json_file)

                filename = os.path.basename(data['imagePath'])

                for rectangle in data['shapes']:

                    currentClass = rectangle['label']

                    xmin = rectangle['points'][0][0]
                    ymin = rectangle['points'][0][1]
                    xmax = rectangle['points'][1][0]
                    ymax = rectangle['points'][1][1]

                    writer.writerow([filename, currentClass, xmin, ymin, xmax, ymax])


def convert_coco_to_xailient(input_path, output_path):

    with open(input_path) as f:
        data = json.load(f)

    xailient_df_annotation = pd.DataFrame(columns=['image_id', 'category_id', 'xmin', 'xmax', 'ymin', 'ymax'])

    for i in data['annotations']:
        image_id = i['image_id']
        category_id = i['category_id']
        x_min = i['bbox'][0]
        y_min = i['bbox'][1]
        x_max = x_min + i['bbox'][2]
        y_max = y_min + i['bbox'][3]
        x_min = int(x_min)
        y_min = int(y_min)
        x_max = int(x_max)
        y_max = int(y_max)
        xailient_df_annotation = xailient_df_annotation.append(
            {'image_id': image_id, 'category_id': category_id, 'xmin': x_min, 'xmax': x_max, 'ymin': y_min,
             'ymax': y_max}, ignore_index=True)

    xailient_df_images = pd.DataFrame(columns=['image_id', 'image_name'])

    for i in data['images']:
        image_id = i['id']
        image_name = i['file_name']
        xailient_df_images = xailient_df_images.append({'image_id': image_id, 'image_name': image_name},
                                                       ignore_index=True)

    xailient_df_categories = pd.DataFrame(columns=['category_id', 'class'])

    for i in data['categories']:
        class_name = i['name']
        category_id = i['id']
        xailient_df_categories = xailient_df_categories.append({'category_id': category_id, 'class': class_name},
                                                               ignore_index=True)

    first_merge = pd.merge(xailient_df_annotation, xailient_df_images, on=['image_id'])

    final_df = pd.merge(first_merge, xailient_df_categories, on=['category_id'])

    drop_columns = ['image_id', 'category_id']
    final_df = final_df.drop(columns=drop_columns)
    columns = ['image_name', 'xmin', 'xmax', 'ymin', 'ymax', 'class']
    final_df = final_df[columns]
    final_df.to_csv(output_path, index=False)


def convert_yolo_to_xailient(input_folder, output_path):
    labels_df = get_labels_from_yolo_txt(input_folder)
    absolute_df = relative_to_absolute(labels_df, input_folder)
    absolute_df.to_csv(output_path, index=False)


def get_labels_from_yolo_txt(input_folder, include_neg=False):
    '''A function to get separate annotations in separate txt files (darknet format)
    into one dataframe object
    input_folder is the parent directory where the annotations txts are
    columns is an optional list passed in and given to the names of the columns of the
    dataframe
    Returns a dataframe object with all the labels and annotations in the same format
    as they were in the txt files'''
    files = os.listdir(input_folder)
    columns = ['class', 'xmid', 'ymid', 'width', 'height', 'image_name']
    df = pd.DataFrame(columns=columns)
    print('Getting labels from txt files...')
    for filename in tqdm(files, total=len(files)):
        if filename.endswith('.txt'):
            if include_neg:
                if os.stat(input_folder + '/' + filename).st_size == 0:
                    jpg_filename = re.sub('.txt', '.jpg', filename)
                    df = df.append(pd.Series(jpg_filename, index=['image_name']), ignore_index=True)

            with open(input_folder + '/' + filename) as txt_file:
                for line in txt_file:
                    jpg_filename = re.sub('.txt', '.jpg', filename)
                    row = line.split()
                    row.append(jpg_filename)
                    df = df.append(pd.Series(row, index=columns), ignore_index=True)
    return df


def relative_to_absolute(data, input_folder, classes=None):
    '''A function to transform 'data' dataframe from relative coordinates to absolute coordinates
    It has to have columns ['image_name', 'class', xmid', 'ymid', 'width', 'height'].
    The height and width here refer to the relative height and width of the object, as per darknet format.
    classes is a dictionary to map class integers to class labels for tf.record
    It returns absolute coordinates dataframe and bad filenames that do not correspond to actual images
    @returns absolute_data (df):        A dataframe with columns ['image_name', 'class', 'xmin', 'xmax', 'ymin', 'ymax', 'height', 'width']
                                        where height and width are now the height and width of the image
    @returns bad_filenames (list):      A list of bad image filenames that could not be processed.
    '''
    bad_filenames = []
    data['xmin'], data['xmax'], data['ymin'], data['ymax'] = 0, 0, 0, 0
    print('Converting relative to absolute coordinates...')

    for col in data.columns:
        if col == 'image_name':
            continue
        data[col] = data[col].astype('float')

    for i, (ix, row) in tqdm(enumerate(data.iterrows()), total=data.shape[0]):
        try:
            img = Image.open(input_folder + '/' + row['image_name'])
            w, h = img.size
        except Exception:
            bad_filenames.append(row['image_name'])
            continue
        data.iloc[i, data.columns.get_loc('xmin')] = row['xmid'] * w - .5 * (row['width'] * w)
        data.iloc[i, data.columns.get_loc('xmax')] = row['xmid'] * w + .5 * (row['width'] * w)
        data.iloc[i, data.columns.get_loc('ymin')] = row['ymid'] * h - .5 * (row['height'] * h)
        data.iloc[i, data.columns.get_loc('ymax')] = row['ymid'] * h + .5 * (row['height'] * h)
        data.iloc[i, data.columns.get_loc('height')] = h
        data.iloc[i, data.columns.get_loc('width')] = w
    data.loc[data['xmin'] < 0, 'xmin'] = 0
    data.loc[data['ymin'] < 0, 'ymin'] = 0
    if classes:
        data['class'] = data['class'].map(classes)
    absolute_data = data[['image_name', 'class', 'xmin', 'xmax', 'ymin', 'ymax']]
    return absolute_data


if __name__ == '__main__':
    main()