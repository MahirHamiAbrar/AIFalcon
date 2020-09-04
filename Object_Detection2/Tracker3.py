#import os
import cv2
#import sys
#import tarfile
#import zipfile

import numpy as np
import tensorflow as tf
#import six.moves.urllib as urllib

from PIL import Image
#from io import StringIO
#from collections import defaultdict
#from matplotlib import pyplot as plt
#from pyfirmata import util, ArduinoMega, SERVO

from Falcon2.System.IO_Style import *
from Falcon2.Database import object_detection_path as od_path

from Falcon2.main.Properties import *
from Falcon2.Networks.Socket_Client import Client

from Falcon2.Features.Video import *

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from threading import Thread

class Tracker():
	def __init__(self, auto_init=True):
		try:
			self.port = '/dev/ttyACM0'
			self.board = ArduinoMega(self.port)
			self.iterator = util.Iterator(self.board)
		except Exception as e:
			print_error(e, __name__+".__init__()")

		self.running = True

		self.servo_x = 2
		self.servo_y = 3

		self.PATH_TO_CKPT = od_path.ssd_mobile_net_path + '/frozen_inference_graph.pb'
		self.PATH_TO_LABELS = od_path.models_dir + "/object_detection/data/mscoco_label_map.pbtxt"
		self.NUM_CLASSES = 90

		self.category_index = None
		self.founded = ''

		self.client = Client('Object-Tracker', PORT=LOCAL_PORT)
		self.client.Start()

		if auto_init:
			self.InitializeHardware()
			self.SetupVedio()
			self.SetupGraph()

	def InitializeHardware(self):
		try:
			self.iterator.start()
			self.board.digital[self.servo_x].mode = SERVO
			self.board.digital[self.servo_y].mode = SERVO
		except Exception as e:
			print_error(e, __name__+".InitializeHardware()")

	def SetupVedio(self):
		try:
			self.cap = cv2.VideoCapture(0)
			self.cap.set(3, 180)
			self.cap.set(4, 180)
		except Exception as e:
			print_error(e, __name__+".SetupVedio()")

	def SetupGraph(self):
		try:
			self.detection_graph = tf.Graph()

			with self.detection_graph.as_default():
				od_graph_def = tf.GraphDef()

				with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
					serialized_graph = fid.read()
					od_graph_def.ParseFromString(serialized_graph)
					tf.import_graph_def(od_graph_def, name='')

				label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
				categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
				self.category_index = label_map_util.create_category_index(categories)

		except Exception as e:
			print_error(e, __name__+".InitializeHardware()")

	def Map(self, value):
	  vA = 650/180
	  vB = value/vA

	  return vB

	def CheckRunningStatus(self):
		while True:
			#receive from which module?
			msg = self.client.Receive('Processor-MAIN')

			#check the id, if it's about quiting the AI or not
			if msg['id'] == 'quit':
				#if yes, then quit...
				if msg['data'] == 'true':
					self.running = False
					#do not forget to close the client server!
					self.client.Stop()
					break

	def Track(self):
		with self.detection_graph.as_default():
		  with tf.Session(graph=self.detection_graph) as sess:
		    while self.running:
		      ret, image_np = self.cap.read()

		      image_np = cv2.flip(image_np, 1)

		      image_np_expanded = np.expand_dims(image_np, axis=0)
		      image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		      boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		      scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		      classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
		      num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		      (boxes, scores, classes, num_detections) = sess.run(
		          [boxes, scores, classes, num_detections],
		          feed_dict={image_tensor: image_np_expanded})
		      # Visualization of the results of a detection.
		      _, dataset = vis_util.visualize_boxes_and_labels_on_image_array(
		          image_np,
		          np.squeeze(boxes),
		          np.squeeze(classes).astype(np.int32),
		          np.squeeze(scores),
		          self.category_index,
		          use_normalized_coordinates=True,
		          line_thickness=10)

		      #viewitems viewkeys viewvalues values
		      #print(dataset, type(dataset)) #--> ymin, xmin, ymax, xmax

		      try:
		        key = list(dataset.keys())[0]

		        if key == 'person':
		          pos = dataset[key][1]
		          #print('Position in image: {}'.format(pos))

		          ymin, xmin, ymax, xmax = pos[0], pos[1], pos[2], pos[3]

		          X = (((xmax - xmin)/2)*1000)/2
		          Y = (((ymax - ymin)/2)*1000)/2

		          X = X+X/2

		          self.founded = key

		          #print('X: ', X, 'Y: ', Y, 'MapX: ', self.Map(X), 'MapY: ', self.Map(Y))

		          try:
		            self.board.digital[self.servo_x].write(180-self.Map(X))
		            self.board.digital[self.servo_y].write(130-self.Map(Y))
		          except Exception as e:
		            print_error(e, __name__+".Track()")
		        else:
		        	self.founded = None

		      except Exception as e:
		        print_error(e, __name__+".Track()")

		      cv2.imshow('object detection', image_np)
		      if cv2.waitKey(25) & 0xFF == ord('q'):
		        cv2.destroyAllWindows()
		        break

def main():
	tracker = Tracker()
	tracker.Track()
	#Thread(target=tracker.Track).start()

if __name__ == '__main__':
	main()
