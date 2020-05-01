# Created by Zahorack
# 1.5.2020

import cv2, time
import numpy as np


class ThermalTest(object):
    def __init__(self, src=0):
        self.body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
        self.body_cascade.load('haarcascade_upperbody.xml')

        self.raw = np.empty((60, 80, 1), dtype=np.uint16)
        self.gray = np.empty((60, 80, 1), dtype=np.uint16)

        self.temp1 = np.empty((60, 80, 1), dtype=np.uint16)

    def update(self, raw_image_reference):
        self.raw = np.copy(raw_image_reference)

        cv2.normalize(self.raw, self.gray, 0, 65535, cv2.NORM_MINMAX)
        np.right_shift(self.gray, 8, self.gray)

    def getHeatMap(self):
        return cv2.applyColorMap(np.uint8(self.gray), cv2.COLORMAP_JET)

    def getGray(self):
        return  np.uint8(self.gray)


    def findMaxTemp(self):
        max_col, max_row = np.unravel_index(self.raw.argmax(), (60, 80))
        # print(max_col)
        # print(max_row)
        return (max_row, max_col)

    def getHistogram(self):
        hist_full = cv2.calcHist([self.raw], [0], None, [65535], [0, 65535])
        # tresh_opt = np.argmax(hist_full)
        # plt.plot(hist_full)
        # plt.show()
        return hist_full

    def tresholding(self):
        tresh = np.amax(self.raw)
        print(tresh)

        cv2.putText(self.frame, "X", self.findMaxTemp(), cv2.FONT_HERSHEY_COMPLEX, 0.1, (0,), 1)

        # segmentation by histogram?
        # ret, self.thresh1  = cv2.threshold(np.uint8(self.frame), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #
        # kernel = np.ones((3, 3), np.uint8)
        # self.thresh1 = cv2.morphologyEx(self.thresh1 , cv2.MORPH_OPEN, kernel, iterations=2)
        #
        # sure_bg = cv2.dilate(self.thresh1, kernel, iterations=3)
        #
        # dist_transform = cv2.distanceTransform(self.thresh1, cv2.DIST_L2, 5)
        # ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)


    def thresholdin1(self):
        tresh = np.amax(self.raw)
        ret1, thresh1 = cv2.threshold(self.raw, tresh - 50, 255, cv2.THRESH_BINARY)
        return thresh1

    def thresholding2(self):
        tresh_opt = np.argmax(self.getHistogram())
        ret2, thresh2 = cv2.threshold(self.raw, tresh_opt + 150, 255, cv2.THRESH_BINARY)
        return np.uint8(thresh2)

    def thresholding3(self):
        blur = cv2.GaussianBlur(self.gray, (5, 5), 0)
        ret3, thresh3 = cv2.threshold(np.uint8(self.gray), 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return np.uint8(thresh3)


    def body_detection(self):
        # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.body_cascade.detectMultiScale(
            self.getGray(),
            scaleFactor=1.01,
            minNeighbors=2,
            minSize=(10, 10)
        )
        for (x, y, w, h) in faces:
            print("Body")
            cv2.rectangle(self.gray, (x, y), (x + w, y + h), (255,), 1)

    def pedestrian_detection(self):
        #
        # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(np.uint8(gray), (5, 5), 0)

        # _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        dilated = cv2.dilate(self.thresholding3(), None, iterations=3)
        _, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)

            # if cv2.contourArea(contour) < 900:
            #     continue
            cv2.rectangle(self.gray, (x, y), (x + w, y + h), (255,), 1)
            # cv2.putText(self.gray, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (255,), 1)


