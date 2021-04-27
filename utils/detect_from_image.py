import numpy as np
import argparse
import os
import tensorflow as tf
from PIL import Image
from io import BytesIO
import pathlib
import glob
import matplotlib.pyplot as plt
from IPython.display import display
from .object_detection.utils import ops as utils_ops
from .object_detection.utils import label_map_util
from .object_detection.utils import visualization_utils as vis_util
from PIL import Image
import numpy as np
import backend_django.settings as settings

# patch tf1 into `utils.ops`
utils_ops.tf = tf.compat.v1

# Patch the location of gfile
tf.gfile = tf.io.gfile


def load_model(model_path):
    model = tf.saved_model.load(model_path)
    return model


def load_image_into_numpy_array(image):
  """Load an image from file into a numpy array.

  Puts image into numpy array to feed into tensorflow graph.
  Note that by convention we put it into a numpy array with shape
  (height, width, channels), where channels=3 for RGB.

  Args:
    path: a file path (this can be local or on colossus)

  Returns:
    uint8 numpy array with shape (img_height, img_width, 3)
  """
#   img_data = tf.io.gfile.GFile(path, 'rb').read()
#   image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(model, image):
    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis,...]
    
    # Run inference
    output_dict = model(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(output_dict.pop('num_detections'))
    output_dict = {key: value[0, :num_detections].numpy()
                   for key, value in output_dict.items()}
    output_dict['num_detections'] = num_detections

    # detection_classes should be ints.
    output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
   
    # Handle models with masks:
    if 'detection_masks' in output_dict:
        # Reframe the the bbox mask to the image size.
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                                    output_dict['detection_masks'], output_dict['detection_boxes'],
                                    image.shape[0], image.shape[1])      
        detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
        output_dict['detection_masks_reframed'] = detection_masks_reframed.numpy()
    return output_dict


def run_inference(image_path):
    labelmap = 'utils/model/label_map.pbtxt'
    model = settings.detection_model
    category_index = label_map_util.create_category_index_from_labelmap(labelmap, use_display_name=True)

    image_np = load_image_into_numpy_array(image_path)
    # Actual detection.
    output_dict = run_inference_for_single_image(model, image_np)
    # Visualization of the results of a detection.
    vis_util.visualize_boxes_and_labels_on_image_array(
        image_np,
        output_dict['detection_boxes'],
        output_dict['detection_classes'],
        output_dict['detection_scores'],
        category_index,
        instance_masks=output_dict.get('detection_masks_reframed', None),
        use_normalized_coordinates=True,
        line_thickness=8)
    plt.imshow(image_np)
    plt.show()
    display(Image.fromarray(image_np))
    img = Image.fromarray(image_np)
    img.show()
    print(output_dict)
    digits = order_digits(output_dict)
    return digits



def order_digits(output_dict):
  first_box =  output_dict["detection_boxes"][0][1]
  second_box = output_dict["detection_boxes"][1][1]
  third_box = output_dict["detection_boxes"][2][1]
  if output_dict["detection_scores"][3] > 0.5:
    boxes = [first_box, second_box, third_box]
    index = sorted(range(len(boxes)), key=lambda k: boxes[k]) # devuelve los indices ordenados
    print(index)
    detection_classes = output_dict["detection_classes"]
    digits = [detection_classes[index[0]], detection_classes[index[1]], detection_classes[index[2]]]
    print(digits)
    return digits
  else:
    return None