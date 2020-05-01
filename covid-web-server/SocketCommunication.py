# Created by Zahorack
# 1.5.2020

import socket
import thread
import json
from collections import namedtuple

PORT  = 54321
HOST = '161.35.29.46'


class Client(object):
    def __init__(self, socket_file_descriptor, address):
        self.s_fd = socket_file_descriptor
        self.addr = address


def newClientCommunication(client):
    while True:

        data = client.s_fd.recv(1024)
        jsonData = json.loads(data)

        print(jsonData)

    client.s_fd.close()


class SocketCommunication(object):
    def __init__(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(('', PORT))
        self.listener.listen(20)
        self.clientList = list()

    def update(self):

        while True:
            s_fd, addr = self.listener.accept()

            newClient = Client(s_fd, addr)
            self.clientList.append(newClient)
            thread.start_new_thread(newClientCommunication, (newClient,))

        self.listener.close()