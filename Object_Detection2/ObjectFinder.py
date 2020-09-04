import cv2
import numpy as np
import tensorflow as tf

from PIL import Image
from threading import Thread

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
#from Falcon2.Object_Detection import _custom_visualization_utils as vis_util

from Falcon2.main.Properties import *
from Falcon2.Features.Video import *
from Falcon2.Features.Firmata import *

from Falcon2.System.IO_Style import *
from Falcon2.Database import object_detection_path as od_path

class Finder():
    def __init__(self, video=None):
        self.video = video
        self.viewImage = None
        self.running = True

        self.PATH_TO_CKPT = od_path.ssd_mobile_net_path + '/frozen_inference_graph.pb'
        self.PATH_TO_LABELS = od_path.models_dir + "/object_detection/data/mscoco_label_map.pbtxt"
        self.NUM_CLASSES = 90

        self.category_index = None
        self.founded = ''

        self.dataset = {}

        self.SetupGraph()

    def SetVideo(self, video):
        self.video = video

    def GetVideo(self):
        return self.viewImage

    def Stop(self):
        self.running = False

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
            	categories = label_map_util.convert_label_map_to_categories(label_map,
                        max_num_classes=self.NUM_CLASSES, use_display_name=True)
            	self.category_index = label_map_util.create_category_index(categories)

        except Exception as e:
            print_error(e, __name__+".SetupGraph()")

    def _print_axis_value(self, object_name):
        object = list(self.dataset[object_name])[1]
        ymin, xmin, ymax, xmax = object[0], object[1], object[2], object[3]

        xHigh = ((xmin+xmax)/2)*100
        xLow = ((xmax-xmin)/2)*100

        yHigh = ((ymin+ymax)/2)*100
        yLow = ((ymax-ymin)/2)*100

        print("High X:", xHigh, "Low X:", xLow, "High Y:", yHigh, "Low Y:", yLow)

    def GetAxisValue(self, object_name):
        object = list(self.dataset[object_name])[1]
        ymin, xmin, ymax, xmax = object[0], object[1], object[2], object[3]

        xHigh = ((xmin+xmax)/2)*100
        xLow = ((xmax-xmin)/2)*100

        yHigh = ((ymin+ymax)/2)*100
        yLow = ((ymax-ymin)/2)*100

        return (xHigh, yHigh), (xLow, yLow)

    def Find(self):
        with self.detection_graph.as_default():
          with tf.Session(graph=self.detection_graph) as sess:
              while self.running:
                try:
                  image_np = self.video
                  if image_np is not None:
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

                      self.dataset = dataset

                      #viewitems viewkeys viewvalues values
                      #print(dataset, type(dataset)) #--> ymin, xmin, ymax, xmax

                      #self._print_axis_value('person')
                      #print("\n\n")

                      self.viewImage = image_np
                      #return image_np

                except Exception as e:
                  print_error(e, __name__+".Find()")

def main():
    v = Video()
    v.SetSize(500, 500)

    finder = Finder()
    Thread(target=finder.Find).start()

    while True:
        _, video = v.GetVideo()

        finder.SetVideo(video)
        show = v.ShowVideo(finder.GetVideo())

        if show is False:
            finder.Stop()
            break

if __name__ == '__main__':
    main()
