# Created by Zahorack
# 1.5.2020

import json
import time
from people_counter import MotionTracker, Camera
from interfaces import SocketCommunication

def millis():
    return int(round(time.time() * 1000))

def minutes():
    return int(round(time.time() / 60))

class PeopleCounter(object):
    def __init__(self, src=0):
        self.counter = 0
        self.name = "home"
        self.unique_key = "KL56M49Q"
        self.countingDirection = 'left'

        # stream = Camera.Camera('data/output4.avi')
        self.stream = Camera.Camera(0)

        self.tracker = MotionTracker.MotionTracker()
        self.tracker.setBorders(190, 360)

        self.communication = SocketCommunication.SocketCommunication()

        self.last_send = 0
        self.last_counter = 0

    def send(self):
        print("send")
        self.last_send = minutes()
        data = json.dumps({"name": str(self.name), "key": self.unique_key, "counter": int(self.counter)})
        self.communication.send(data)


    def update(self):
        frame = self.stream.read()

        self.tracker.update(frame)
        self.tracker.show()

        if self.countingDirection == 'right':
            self.counter = self.tracker.passed_right - self.tracker.passed_left
        elif self.countingDirection == 'left':
            self.counter = self.tracker.passed_left - self.tracker.passed_right

        if self.counter < 0:
            self.counter = 0
            self.tracker.reset()

        if self.last_counter != self.counter:
            self.last_counter = self.counter
            self.send()

        if minutes() > (self.last_send + 1):
            self.send()



if __name__ == '__main__':

    peopleCounter = PeopleCounter()

    while True:
        peopleCounter.update()






