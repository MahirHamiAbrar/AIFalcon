"""
os.system("cd ~/models/research && export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim && ~/AI/bin/python /home/mahirhamiabrar/AI/Object_Recogniiton/tracker.py")
"""

import os
import cv2
import sys
import tarfile
import zipfile

import numpy as np
import tensorflow as tf
import six.moves.urllib as urllib

from PIL import Image
from io import StringIO
from collections import defaultdict
from matplotlib import pyplot as plt
from pyfirmata import util, ArduinoMega, SERVO

from Falcon2.Database import object_detection_path as od_path

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

port = '/dev/ttyACM0'

board = ArduinoMega(port)
it = util.Iterator(board)
it.start()

servo_x = 2
servo_y = 3

board.digital[servo_x].mode = SERVO
board.digital[servo_y].mode = SERVO

cap = cv2.VideoCapture(0)
cap.set(3, 180) #width
cap.set(4, 180) #height

PATH_TO_CKPT = od_path.ssd_mobile_net_path + '/frozen_inference_graph.pb'

PATH_TO_LABELS = od_path.models_dir + "/object_detection/data/mscoco_label_map.pbtxt"

NUM_CLASSES = 90

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_icategory_indexnto_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def Map(value):
  vA = 650/180
  vB = value/vA

  return vB

with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      ret, image_np = cap.read()

      image_np = cv2.flip(image_np, 1)
      
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')

      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      # Visualization of the results of a detection.
      _, dataset = vis_util.visualize_boxes_and_labels_on_image_array(
          image_np,
          np.squeeze(boxes),
          np.squeeze(classes).astype(np.int32),
          np.squeeze(scores),
          category_index,
          use_normalized_coordinates=True,
          line_thickness=10)

      #viewitems viewkeys viewvalues values
      print(dataset, type(dataset)) #--> ymin, xmin, ymax, xmax

      try:
        key = list(dataset.keys())[0]

        if key == 'person':
          pos = dataset[key][1]
          print('Position in image: {}'.format(pos))

          ymin, xmin, ymax, xmax = pos[0], pos[1], pos[2], pos[3]

          X = (((xmax - xmin)/2)*1000)/2
          Y = (((ymax - ymin)/2)*1000)/2

          X = X+X/2

          print('X: ', X, 'Y: ', Y, 'MapX: ', Map(X), 'MapY: ', Map(Y))

          try:
            board.digital[servo_x].write(180-Map(X))
            board.digital[servo_y].write(130-Map(Y))
          except Exception as e:
            print("[EXCEPTION]:", e)

      except Exception as e:
        print(e)

      cv2.imshow('object detection', image_np)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
