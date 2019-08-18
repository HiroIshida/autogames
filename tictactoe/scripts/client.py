#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import os
import random
import socket
import time
import json


class Client:

    def __init__(self):
        self.host = '127.0.0.1'  # The server's hostname or IP address
        self.port = 65431        # The port used by the server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # reconnectable client
        # https://qiita.com/shino_312/items/3c81ed8d8dfd0d53f25a
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.settimeout(3)
        self.client.connect((self.host, self.port))
        self.field = None

    def put(self, position):
        method = "put"
        args = {'position': position}
        try:
            self._send(method, args)
        except BrokenPipeError:
            print("Game Finished")
            os._exit(0)
        message_recieved = self.client.recv(1024).decode()
        print(message_recieved)

    def get_field(self):
        method = "get_field"
        args = {}
        self._send(method, args)
        message_recieved_ = self.client.recv(1024)
        message_recieved = message_recieved_.decode()
        json_data = json.loads(message_recieved)
        field = json_data["data"]
        return field

    def _send(self, method, args):
        data = dict()
        data["method"] = method
        data["args"] = args
        str_data = json.dumps(data)
        message_send = str_data.encode()
        self.client.sendall(message_send)

    def rand_algorithm(self):
        self.put((random.randint(0, 2), random.randint(0, 2)))

    def main(self):
        while True:
            time.sleep(0.1)
            # PLEASE WRITE ME
            self.rand_algorithm()
            # PLEASE WRITE ME


if __name__ == '__main__':
    client = Client()
    client.main()
