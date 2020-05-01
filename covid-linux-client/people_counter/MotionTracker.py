# Created by Zahorack
# 1.5.2020

import cv2
import numpy as np
from people_counter import TrackingObject, MotionDetection
import math
from collections import OrderedDict



from people_counter.TrackingObject import TrackingObject

motionDetector = MotionDetection.MotionDetection()


def distance(object1, object2):
    return abs(object1.position.x - object2.position.x)

def module(object1, object2):
    x_distance = abs(object1.position.x - object2.position.x)
    y_distance = abs(object1.position.y - object2.position.y)

    module = math.sqrt(math.pow(x_distance, 2) + math.pow(y_distance,2))
    return module

def isFoundInDirection(tracked, found):

    if not tracked.hasDirection():
        return True

    if tracked.direction == 'right':
        # if found.position.x > tracked.position.x and (found.position.x < tracked.position.x + tracked.searchDistance()):
        if found.area.x < tracked.position.x < (found.area.x + found.area.w*2):
            return True
        else:
            return False

    elif tracked.direction == 'left':
        # if found.position.x < tracked.position.x and (found.position.x > tracked.position.x - tracked.searchDistance()):
        if (found.area.x - found.area.w) < tracked.position.x < (found.area.x + found.area.w):
            return True
        else:
            return False





def isFoundInArea(tracked, found):
    if (tracked.area.x - tracked.area.w) < found.position.x < (tracked.area.x + tracked.area.w*2):
        return True

    # if tracked.direction == 'right':
    #     if tracked.area.x < found.position.x < (tracked.area.x + tracked.speed*3):
    #         return True
    # elif tracked.direction == 'left':
    #     if (tracked.area.x - tracked.speed*3) < found.position.x < (tracked.area.x + tracked.area.w):
    #         return True

    return False



class MotionTracker(object):
    def __init__(self, input=0):

        self.frame = np.empty((480, 640, 3), dtype=np.uint8)

        self.trackingList = list()
        self.borders_left = 0
        self.borders_right = 0

        self.passed_limit = 100

        self.passed_left = 0
        self.passed_right = 0

    def setBorders(self, left, right):
        self.borders_left = left
        self.borders_right = right

    def getValidContours(self, size):
        validContours = list()

        for contour in self.contours:
            if cv2.contourArea(contour) > size:
                validContours.append(contour)

        return validContours


    # find and assign contour based on best position, direction or prediction if no contour is available
    def findBestContourForTracker(self, validContours):

        if len(self.trackingList) == 0:
            for contour in validContours:
                self.trackingList.append(TrackingObject(contour))
            return True

        usedContoursIndexes = list()
        for trackedObject in self.trackingList:
            trackedObject.live()
            if len(validContours) > 0:
                bestFoundObject = TrackingObject(validContours[0])
                contour_counter = 0
                contour_index = None
                for contour in validContours:
                    foundObject = TrackingObject(contour)
                    if isFoundInDirection(trackedObject, foundObject):
                        if distance(trackedObject, foundObject) <= distance(trackedObject, bestFoundObject):
                            bestFoundObject = foundObject
                            contour_index = contour_counter
                    contour_counter += 1

                # if isFoundInDirection(trackedObject, bestFoundObject) and isFoundInArea(trackedObject, bestFoundObject):
                # if isFoundInArea(trackedObject, bestFoundObject):

                if isFoundInDirection(trackedObject, bestFoundObject) and not (contour_index in usedContoursIndexes):
                    trackedObject.update(bestFoundObject.contour)
                else:
                    trackedObject.nextPositionPrediction()
                    contour_index = None

                if contour_index is not None:
                    usedContoursIndexes.append(contour_index)

            # else:
            #     trackedObject.nextPositionPrediction()

        print(usedContoursIndexes)
        # create list of unused contour
        unusedContours = self.removeComponentsFromListByIndex(validContours.copy(), usedContoursIndexes)

        #create new trackers from unused contours
        for contour in unusedContours:
            self.trackingList.append(TrackingObject(contour))



    def removeComponentsFromListByIndex(self, that_list, components):
        #remove duplicates from component list
        components = list(OrderedDict.fromkeys(components.copy()))

        iterator = 0
        if len(that_list) > 0:
            for index in components:
                del that_list[index - iterator]
                iterator += 1

        return that_list


    def update(self, frame):

        self.frame = np.copy(frame)
        # find motion contours
        self.contours = motionDetector.update(self.frame)

        self.findBestContourForTracker(self.getValidContours(1500))


        # remove duplication tracker based on position
        # self.removeDuplicatedTrackers()
        # self.checkPassed()
        # self.removeDeadTrackers()

        newList = list()
        for trackedObject in self.trackingList:

            if trackedObject.predictions > 10:
                trackedObject.kill()

            if self.borders_left > trackedObject.position.x > self.borders_right:
                trackedObject.kill()

            if not trackedObject.isAlive():
                if abs(trackedObject.distance) > self.passed_limit:
                    if trackedObject.direction == 'left':
                        self.passed_left += 1
                    elif trackedObject.direction == 'right':
                        self.passed_right += 1

            if trackedObject.isAlive():
                newList.append(trackedObject)

        self.trackingList = newList

        self.removeDuplicatedTrackers()


        print('passsed: ' + str(self.passed_left) + ' /  ' + str(self.passed_right))

        return self.contours


    def checkPassed(self):
        for trackedObject in self.trackingList:

            # if not trackedObject.isAlive():
            #     self.removeDuplicatedTrackers(trackedObject)

            if (self.borders_right) < trackedObject.position.x < (self.borders_left):
                trackedObject.kill()

            if trackedObject.predictions > 10:
                trackedObject.kill()

            if not trackedObject.isAlive():
                if abs(trackedObject.distance) > self.passed_limit:
                    if trackedObject.direction == 'left':
                        self.passed_left += 1
                    elif trackedObject.direction == 'right':
                        self.passed_right += 1


    def removeDeadTrackers(self):
        newTrackingList = list()

        for trackedObject in self.trackingList.copy():
            if trackedObject.isAlive():
                newTrackingList.append(trackedObject)
        self.trackingList = newTrackingList


    def removeDuplicatedTrackersFor(self, object):
        newTrackingList = list()

        newTrackingList.append(object)
        duplicationFound = False

        if len(self.trackingList) > 1:
            for item in range(1, len(self.trackingList)):
                duplicationFound = False
                if self.trackingList[item].position.get() == object.position.get():
                    duplicationFound = True

            if not duplicationFound:
                newTrackingList.append(self.trackingList[item])

            self.trackingList = newTrackingList

    def removeDuplicatedTrackers(self):
        # remove duplication tracker based on position and save the oldest one
        newTrackingList = list()
        if len(self.trackingList) > 0:

            newTrackingList.append(self.trackingList[0])
            for item in range(1, len(self.trackingList)):
                duplicationFound = False
                for index in range(0, len(newTrackingList)):
                    if self.trackingList[item].position.get() == newTrackingList[index].position.get():
                        duplicationFound = True
                        self.trackingList[item].duplicationCounter += 1
                    else:
                        self.trackingList[item].duplicationCounter = 0

                if not duplicationFound:
                    newTrackingList.append(self.trackingList[item])
                # if self.trackingList[item].duplicationCounter > 10:
                #     self.trackingList[item].kill()
            self.trackingList = newTrackingList

        # remove duplication tracker based on position and save newest one
        # newTrackingList = list()
        # for item in range(0, len(self.trackingList)):
        #     duplicationFound = False
        #     for index in range(item+1, len(self.trackingList)):
        #         if self.trackingList[item].position.get() == self.trackingList[index].position.get():
        #             duplicationFound = True
        #     if not duplicationFound:
        #         newTrackingList.append(self.trackingList[item])
        #
        # self.trackingList = newTrackingList


    def show(self):

        cv2.line(self.frame, (self.borders_left, 0), (self.borders_left, self.frame.shape[1]), (255, 0, 255), 2)
        cv2.line(self.frame, (self.borders_right, 0), (self.borders_right, self.frame.shape[1]), (255, 0, 255), 2)

        index = 0
        for trackedObject in self.trackingList:
            print('Tracker '+ str(index) + '  '+ trackedObject.direction + ' distance: '+ str(trackedObject.distance)  + '  age: ' + \
                  str(trackedObject.age) + '  position x: ' + str(trackedObject.position.x) + '  predictions: ' + \
                  str(trackedObject.predictions) + '  active life:  ' + str(trackedObject.activeLife))
            for point in trackedObject.trajectory:
                cv2.circle(self.frame, (point[0], point[1]), 2, (0, 0, 255), 2)

            cv2.putText(self.frame, 'ID: ' +str(index), trackedObject.getAreaBegin(), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.rectangle(self.frame, trackedObject.getAreaBegin(), trackedObject.getAreaEnd(), (255, 0, 0), 3)

            index += 1

        for contour in self.contours:
            object = TrackingObject(contour)

            if cv2.contourArea(contour) < 1500:
                continue

            # cv2.circle(self.frame, object.getPosition(), 2, (0, 0, 255), 2)
            cv2.rectangle(self.frame, object.getAreaBegin(), object.getAreaEnd(), (0, 255, 0), 2)



        cv2.imshow('rgb', self.frame)




def getCountourCenter(contour):
    M = cv2.moments(contour)
    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx = cy = 0
    return cx, cy