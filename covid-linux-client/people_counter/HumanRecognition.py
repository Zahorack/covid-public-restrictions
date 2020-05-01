# Created by Zahorack
# 1.5.2020

import cv2
import imutils
import numpy as np


class HumanRecognition(object):

    def __init__(self):
        self.frame = np.empty((480, 640, 3), dtype=np.uint8)

        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def HogMethod(self, frame):
        self.frame = np.copy(frame)

        image = imutils.resize(self.frame, width=min(400, self.frame.shape[1]))

        (regions, weights) = self.hog.detectMultiScale(image,
            winStride=(4, 4),
            padding=(8, 8),
            scale=1.2)


        for (x, y, w, h) in regions:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.imshow('hog detector', self.frame)


    def show(self):
        cv2.imshow('hog detector', self.frame)