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

# install request using pip3 install requests
import requests
import json
import cv2
import base64
import os

def XailientDetector(image_path, sendImageAsFileByte = True):
    url = 'http://127.0.0.1:5001/v1/detector'

    # Send image as file byte
    if sendImageAsFileByte:
        response = send_image_as_filebyte(url, image_path)
    # Send image as base64 string
    else:
        img = cv2.imread(image_path)
        response = send_image_as_base64(url, img)

    res_json =  json.loads(response.text)
    print(type(res_json))
    print(res_json)

    results = res_json['results']

    img = cv2.imread(image_path)

    for result in results:
        bbox = result['bbox']
        
        cv2.rectangle(img, (bbox['xmin'], bbox['ymin']), (bbox['xmax'], bbox['ymax']), (0, 255, 0), 3)

    cv2.imwrite('saved_output.jpg', img)

    return res_json

"""
This function is to send results to a web API using HTTP post.
"""
def send_image_as_base64(API_ENDPOINT, frame):

    # data to be sent to api 
    data = {}
    data['upload'] = encode(frame)

    # convert the data to be sent to json
    data_json = json.dumps(data)

    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data_json) 

    print("Response: {}".format(r))
    print("Response body: {}".format(r.text))

    return r

"""
This function is to send results to a web API using HTTP post.
"""
def send_image_as_filebyte(API_ENDPOINT, image_path):

    files = {'upload': open(image_path, 'rb')}
    r = requests.post(API_ENDPOINT, files=files)

    print("Response: {}".format(r))
    print("Response body: {}".format(r.text))

    return r

def encode(image):
    # Encoded the image to base64
    is_success, im_buf_arr = cv2.imencode(".jpg", image)
    byte_im = im_buf_arr.tobytes()

    myObj = [base64.b64encode(byte_im)]          

    # Assing to return_json variable to return. 
    return_json = str(myObj[0])            

    # repplace this 'b'' is must to get absoulate image.
    return_json = return_json.replace("b'","")          
    base64_encoded_image = return_json.replace("'","")  

    return base64_encoded_image


def decode(base64_img):
    filename = 'decoded_image.png'
    base64_img_bytes = base64_img.encode('utf-8')
    with open(filename, 'wb') as file_to_save:
        decoded_image_data = base64.decodebytes(base64_img_bytes)
        file_to_save.write(decoded_image_data)

    decoded_img = cv2.imread(filename)
    try:
        os.remove(filename)
    except Exception as ex:
        print("Exception removing temp file {}".format(ex))
        
    return decoded_img

XailientDetector("image.png")