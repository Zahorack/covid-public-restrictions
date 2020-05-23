# Created by Zahorack
# 1.5.2020

import socket
import json
import sys
import signal
from threading import Thread
from collections import namedtuple
from people_counter import people_counter

PORT  = 54321
HOST = '161.35.29.46'


class Client(object):
    def __init__(self, socket_file_descriptor, address):
        self.s_fd = socket_file_descriptor
        self.addr = address


def newClientCommunication(client):

    pc = people_counter.PeopleCounter()
    while True:

        data = client.s_fd.recv(1024)

        pc.update(data)

    client.s_fd.close()


class SocketCommunication(object):
    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientList = list()
        self.threadList = list()

        signal.signal(signal.SIGINT, self.close)




    def initialize(self):
        print("SocketCommunication init")


    def update(self):
        self.initialize()

        self.listener.bind(('', PORT))
        self.listener.listen(20)
        while True:
            s_fd, addr = self.listener.accept()

            newClient = Client(s_fd, addr)
            self.clientList.append(newClient)
            thread_handler = Thread(target=newClientCommunication, args=(newClient,))
            thread_handler.start()
            self.threadList.append(thread_handler)

        self.listener.close()

    def close(self, sig, frame):
        print("___Closing socket communication..")
        self.listener.close()

        for t in self.threadList:
            t.join()

        for s in self.clientList:
            s.s_fd.close()

        # sys.exit(0)