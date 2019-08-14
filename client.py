#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

import socket
import json

class Player:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def put(self, position):
        method = "put"
        args = {'position': position}
        self._send(method, args)

    def show(self):
        method = "show"
        args = {}
        self._send(method, args)

    def _send(self, method, args):
        data = dict()
        data["method"] = method
        data["args"] = args
        str_data = json.dumps(data)
        message_send = str_data.encode()
        self.client.sendall(message_send)
        message_recieved = self.client.recv(1024)
        print(message_recieved)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

player = Player(HOST, PORT)
player.put((1, 1))
player.show()

