from tflite_runtime.interpreter import Interpreter
import cv2 as cv
import numpy as np

# model file and label
model_path = "model.tflite" 
label_path = "label.txt"

# set classification threshold
CLASSIFICATION_THRESHOLD = 0.7
INPUT_FRAME_WIDTH = 224
INPUT_FRAME_HEIGHT = 224

class Classifier():
  labels = None
  interpreter = None

  """
  This method is for initialization. Is is called when a new object of the class is created.
  """
  def __init__(self):
    self.labels = self.load_labels(label_path)
    self.interpreter = Interpreter(model_path=model_path)
    
    self.interpreter.allocate_tensors()
  
  """
  This method contains the higher lever logic for processing an incoming frame.
  It resizes the frame, calls method to perform classification, applied threshold to the 
  result and returns results based on it.
  """
  def process_frame(self, frame):  
      # Resize frame
      image = cv.resize(frame,(INPUT_FRAME_WIDTH, INPUT_FRAME_HEIGHT))
      
      # classify image
      results = self.classify_image(self.interpreter, image)

      # get label and probability score
      label_id, prob = results[0]
      print("Label = {}, prob = {}".format(self.labels[label_id], prob))

      # apply classification threshold
      if prob >= CLASSIFICATION_THRESHOLD:
        return True
    
      return False

  """
  This method loads the labels from the label text file.
  """
  def load_labels(self, path):
    with open(path, 'r') as f:
      return {i: line.strip() for i, line in enumerate(f.readlines())}

  """
  This method contains the implementation for classification of images.
  It returns a sorted array of classification results.
  """
  def classify_image(self, interpreter, image):
    self.set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    # Dequantize results if the model is quantized (uint8 data)
    if output_details['dtype'] == np.uint8:
      scale, zero_point = output_details['quantization']
      output = scale * (output - zero_point)

    ordered = np.argpartition(-output, 1)
    x = [(i, output[i]) for i in ordered[:1]]
    return x

  """
  Sets the input tensor.
  """
  def set_input_tensor(self, interpreter, image):
      tensor_index = interpreter.get_input_details()[0]['index']
      input_tensor = interpreter.tensor(tensor_index)()[0]
      input_tensor[:, :] = image

  """
  Returns the output tensor at the given index.
  """
  def get_output_tensor(self, interpreter, index):
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    return tensor

# Here is an example of how to instantiate classifier class and its methods
#image = cv.imread("example_image.jpeg")
#classifier = Classifier()
#classifier.process_frame(image)