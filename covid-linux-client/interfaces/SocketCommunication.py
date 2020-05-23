# Created by Zahorack
# 1.5.2020

import socket
import time
import json
import signal

HOST = '161.35.29.46'
PORT = 54321


class SocketCommunication(object):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        signal.signal(signal.SIGINT, self.close)

    def send(self, data):
        self.socket.send(data.encode())

    def close(self):
        self.socket.close()

# if __name__ == "__main__":
#
#     com = SocketCommunication()
#
#     while True:
#         time.sleep(1)
#         dataJson = json.dumps({"right": 5, 'left': 2})
#         com.send(dataJson)
