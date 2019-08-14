#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def send_dict(dict_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #dict_data = '{"x": 1, "y": 2}'
        str_data = json.dumps(dict_data)
        bin_data = str_data.encode()
        s.sendall(bin_data)
        data = s.recv(1024)
        print('Received', repr(data))

def send_command(method, args):
    data = dict()
    data["method"] = method
    data["args"] = args
    send_dict(data)

def put(pos):
    args = {'position': pos}
    send_command("put", args)

def show():
    args = {}
    send_command("show", args)


put((1, 1))
put((2, 1))
show()


