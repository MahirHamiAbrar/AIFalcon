"""
This module helps to get the live vedio streaming from the camera to multiple files of the
AI in a same time and also shows the video in a gui window if necessary.

This module is mainly based on OpenCV-Python.

***Created by
                Mahir Hami Abrar
                                    (for developing AI-Falcon2).***
"""
import cv2
import numpy as np

from Falcon2.System.IO_Style import *

class Video():
    def __init__(self, videoCap=0, width=180, height=180):
        self.width = width
        self.height = height
        self.videoCap = videoCap

        self.CreateVideo()

    def CreateVideo(self):
        self.cap = cv2.VideoCapture(self.videoCap)
        self._set_frame_size(self.width, self.height)

    def GetVideo(self, flipCode=1):
        try:
            ret, image = self.cap.read()
            image = cv2.flip(image, flipCode)

            return ret, image
        except Exception as e:
            print_error(e, __name__+".GetVideo()")

    def _set_frame_size(self, width, height):
        self.cap.set(3, width)
        self.cap.set(4, height)

    def SetVideoCap(self, videoCap):
        self.videoCap = videoCap

    def SetSize(self, width, height):
        self.width = width
        self.height = height
        self._set_frame_size(self.width, self.height)

    def ShowVideo(self, video, title="Video", waitKey=25, key='q'):
        status = True
        try:
            if video is not None:
                cv2.imshow(title, video)

                if cv2.waitKey(waitKey) & 0xFF == ord(key):
                    cv2.destroyAllWindows()
                    status = False

            return status
        except Exception as e:
            print_error(e, __name__)

def main():
    v = Video()
    v.SetSize(500, 500)

    while True:
        _, img = v.GetVideo()

        show = v.ShowVideo(img, key='q')

        if show is False:
            break

if __name__ == '__main__':
    main()
