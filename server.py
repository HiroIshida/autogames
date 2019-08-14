#!/usr/bin/env python3

import socket
import json
import base64
import threading
import select
from tictoctoe import TictactoeGame

game_field = TictactoeGame(3)

def dispatch(method, args):
    if method == "put":
        game_field.put(args["position"])

    if method == "show":
        game_field.show()


HOST = '127.0.0.1'
PORT = 65432


def loop_handler(connection, address):
    while True:
        bin_data = connection.recv(1024)
        if not bin_data:
            break
        str_data = bin_data.decode()
        dict_data = json.loads(str_data)

        method = dict_data["method"]
        args = dict_data["args"]
        dispatch(method, args)
        conn.sendall(b'received')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        loop_handler(conn, addr)






