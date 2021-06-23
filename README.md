This repo contains sample reference implementations and example codes

## Scripts for inferencing

### Detection on Static Image

File: [inference_on_video.py](https://github.com/XailientPublic/example_scripts/blob/master/inference_on_video.py)

### Send Detection Event to API using HTTP Post

File: [http_post_example.py](https://github.com/XailientPublic/example_scripts/blob/master/http_post_example.py)


### Detection on Pi Camera Streaming Video

File: [inference_on_video.py](https://github.com/XailientPublic/example_scripts/blob/master/inference_using_raspberrypi_camera.py)

## Split a video into frames for training data

File: [extract_frames_from_video.py](https://github.com/XailientPublic/example_scripts/blob/master/extract_frames_from_video.py)

This tool allows developers to quickly split a video into frames,
with the aim in create training data for model production.

This python script allows developers to either:

1. Go through each frame and manually save the frames you want (default).

`$ python3 extract_frames_from_video <path_to_video>`

2. Save every ith frame in the video.

`$ python3 extract_frames_from_video --every <integer> <path_to_video>`


## Conversion of different annotation formats

File: [convert_label_to_xailient_format.py](https://github.com/XailientPublic/example_scripts/blob/master/convert_label_to_xailient_format.py)

A script to convert different annotations formats to the format required by the Xailient Console.

Currently supported formats for this conversion script are pascalvoc/labelimg, labelme, coco, and yolo formats.

Choices for input_format argument are 'voc', 'coco', 'labelme', 'yolo'

- For annotations present in a single file (e.g. COCO), input_path represents the path to the JSON file. 

- While for separate annotations for each image (e.g. Pascal VOC, yolo, labelme), input_path represents
the path to the folder where the annotations reside.

The output_path is the path and name of the converted xailient annotations.

Examples of usage:

`$ python3 convert_label_to_xailient_format.py --input_path example/coco_annotations.json --input_format coco --output_path example/xailient_labels.csv`

## Scripts for running Xailient SDK as Docker container API

File: [XailientDockerAPI](https://github.com/XailientPublic/example_scripts/blob/master/XailientDockerAPI/docker_x86_64)

## Post-processing scripts to improve accuracy

File: [post_processing_script_to_improved_accuracy.py](https://github.com/XailientPublic/example_scripts/blob/master/post_processing_script_to_improved_accuracy.py)

## Scripts to convert image formats

File: [png_to_jpg_converter.py](https://github.com/XailientPublic/example_scripts/blob/master/png_to_jpg_converter.py)