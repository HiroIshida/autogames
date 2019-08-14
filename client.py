#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

import socket
import json

def gen_message(method, args):
    data = dict()
    data["method"] = method
    data["args"] = args
    str_data = json.dumps(data)
    bin_data = str_data.encode()
    return bin_data

def get_put_message(pos):
    args = {'position': pos}
    return gen_message("put", args)

def get_show_message():
    args = {}
    return gen_message("show", args)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

message = get_put_message((1, 1))
client.sendall(message)
data_recv = client.recv(1024)
print('Received', repr(data_recv))

