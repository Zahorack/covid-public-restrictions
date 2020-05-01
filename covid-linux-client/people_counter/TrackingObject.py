# Created by Zahorack
# 1.5.2020

import cv2
import numpy as np

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __init__(self):
        self.x = 0
        self.y = 0

    def get(self):
        return (self.x, self.y)

class Area(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0

    def get(self):
        return (self.x, self.y, self.w, self.h)


class TrackingObject(object):
    def __init__(self, contour):

        self.contour = contour
        self.position = Position()
        self.area = Area()
        self.trajectory = list()

        self.direction = 'unknown'
        self.distance = 0
        self.activeLife = 0
        self.age = 0
        self.id = None
        self.duplicationCounter = 0

        self.speed = 0
        self.predictions = 0

        self.update(contour)


    def update(self, contour):
        self.contour = contour

        self.predictions = 0
        (x, y, w, h) = cv2.boundingRect(self.contour)
        cx, cy = getCountourCenter(self.contour)

        self.position.x = cx
        self.position.y = cy

        self.trajectory.append((cx, cy))

        self.area.x = x
        self.area.y = y
        self.area.w = w
        self.area.h = h

        self.activeLife += 1
        self.distance = (self.trajectory[0][0] - self.position.x)

        self.computeSpeed()

        if self.distance > 0:
            self.direction = 'left'
        elif self.distance < 0:
            self.direction = 'right'

    def searchDistance(self):
        if self.speed > 0:
            return self.speed*4

        else:
            return self.area.w*2

    def nextPositionPrediction(self):

        print('\nPrediction needed')
        self.predictions += 1
        self.computeSpeed()

        if self.direction == 'right':
            self.position.x  = self.position.x + self.speed
            self.position.y = self.position.y
            self.area.x = self.area.x + self.speed

        elif self.direction == 'left':
            self.position.x = self.position.x - self.speed
            self.position.y = self.position.y
            self.area.x = self.area.x - self.speed


        self.trajectory.append((self.position.x, self.position.y))

        self.activeLife += 1
        self.distance = (self.trajectory[0][0] - self.position.x)

        if self.distance > 0:
            self.direction = 'left'
        elif self.distance < 0:
            self.direction = 'right'


    def computeSpeed(self):
        if len(self.trajectory) > 2:
            sum_speed = 0
            for index in range(0, len(self.trajectory) - 1):
                sum_speed += abs(self.trajectory[index][0] - self.trajectory[index + 1][0])
            self.speed = int(round(sum_speed / len(self.trajectory)))
            # self.speed = int(round(self.speed))


    def isAlive(self):
        if self.age > (self.activeLife + 3):
            return False

        return True

    def kill(self):
        print('KILL')
        self.age = 10000

    def live(self):
        self.age += 1

    def getPosition(self):
        return self.position.x, self.position.y

    def getArea(self):
        return self.area.x, self.area.y, self.area.w, self.area.h


    def getAreaBegin(self):
        return self.area.x, self.area.y

    def getAreaEnd(self):
        return self.area.x + self.area.w, self.area.y + self. area.h

    def hasDirection(self):
        if self. direction == 'unknown':
            return False

        return True



def getCountourCenter(contour):

    M = cv2.moments(contour)

    if M['m00'] > 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx = cy = 0
    return cx, cy