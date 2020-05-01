# Created by Zahorack
# 1.5.2020

import cv2
import imutils
import numpy as np

class FaceRecognition(object):
    def __init__(self):
        self.frame = np.empty((480, 640, 3), dtype=np.uint8)

        self.face_cascade = cv2.CascadeClassifier('haar_cascades/haarcascade_upperbody.xml')
        self.face_cascade.load('haar_cascades/haarcascade_upperbody.xml')

    def HaarCascadesMethod(self, frame):

        self.frame = np.copy(frame)

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(40, 40)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        cv2.imshow('haar cascades detector', self.frame)