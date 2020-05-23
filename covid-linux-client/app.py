# Created by Zahorack
# 1.5.2020

import json
import time
from people_counter import MotionTracker, Camera
from interfaces import SocketCommunication

stream = Camera.Camera('data/output4.avi')
# stream = Camera.Camera(0)

tracker = MotionTracker.MotionTracker()
tracker.setBorders(190, 360)


class PeopleCounter(object):
    def __init__(self, src=0):
        self.counter = 5
        self.name = "home"

    def update(self):

        return 1


if __name__ == '__main__':
    print("hello")
    peopleCounter = PeopleCounter()

    com = SocketCommunication.SocketCommunication()

    while True:
        # frame = stream.read()
        #
        # # input("**** next frame ****")
        # tracker.update(frame)
        # tracker.show()

        time.sleep(1)
        dataJson = json.dumps({"name": str(peopleCounter.name), "counter": int(peopleCounter.counter)})
        com.send(dataJson)
        print('send')






