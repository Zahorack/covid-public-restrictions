# Created by Zahorack
# 1.5.2020

import cv2, time
import numpy as np

iterator = 0

class MotionDetection(object):
    def __init__(self, src=0):
        self.frame = np.empty((480, 640, 3), dtype=np.uint8)
        self.frameList = list()


    def update(self, image):
        self.frame = np.copy(image)

        global iterator
        iterator = iterator +1

        self.frameList.append(self.frame.copy())

        if len(self.frameList) > 7:
            self.frameList.pop(0)


        diff1 = cv2.absdiff(self.frameList[len(self.frameList)-2].copy(), self.frame)
        diff2 = cv2.absdiff(self.frameList[0].copy(), self.frame)

        gray1 = cv2.cvtColor(diff1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(diff2, cv2.COLOR_BGR2GRAY)

        # blur1 = cv2.GaussianBlur(gray1, (2, 2), 0)
        # blur2 = cv2.GaussianBlur(gray2, (2, 2), 0)

        _, thresh = cv2.threshold(gray1, 15, 255, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(gray2, 15, 255, cv2.THRESH_BINARY)

        diff = np.logical_and(thresh, thresh2)
        diff = diff.astype(np.uint8)
        diff = diff*255

        # dilated = cv2.dilate(diff, np.ones((2, 2), np.uint8), iterations=2)
        # erosion = cv2.erode(dilated, np.ones((2,2),np.uint8), iterations=3)
        # dilated = cv2.dilate(erosion, np.ones((3,3),np.uint8), iterations=4)

        opening = cv2.morphologyEx(diff, cv2.MORPH_OPEN, np.ones((2,2),np.uint8), iterations=2)
        dilated = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=3)


        cv2.imshow('dilated', dilated)
        # cv2.imshow('diff1', diff1)
        # cv2.imshow('diff2', diff2)
        cv2.imshow('gray1', gray1)
        # cv2.imshow('gray2', gray2)

        _,contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # _,contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        return contours
