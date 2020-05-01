# Created by Zahorack
# 1.5.2020

import cv2
import numpy as np


class Camera(object):
    def __init__(self, input):

        self.capture = cv2.VideoCapture(input)
        # self.capture = cv2.VideoCapture('output5.avi')
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        # self.capture.set(cv2.CAP_PROP_MODE, 1)
        self.capture.set(cv2.CAP_PROP_FPS, 25)

        self.frame_id = 0
        self.last_frame_id = 0

        self.frame = np.empty((480, 640, 3), dtype=np.uint8)


    def isOpened(self):
        return self.capture.isOpened()

    def read(self):
        if self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            self.frame_id = self.frame_id+1

        if cv2.waitKey(1) == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

        return self.frame

    def show(self):
        cv2.imshow('rgb', self.frame)

    def get(self):
        if self.last_frame_id != self.frame_id:
            self.last_frame_id = self.frame_id
        return self.frame
