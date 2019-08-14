#!/usr/bin/env python3

# as for making a server for multiple clients, see: https://qiita.com/1000VICKY/items/2338852a41c6aaf8efbb#4%E3%82%AF%E3%83%A9%E3%82%A4%E3%82%A2%E3%83%B3%E3%83%88%E5%81%B4%E3%81%AE%E5%8F%97%E4%BF%A1%E3%82%92%E5%88%A5%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89%E3%81%AB%E5%88%86%E9%9B%A2

import socket
import json
import base64
import threading
import select
from tictoctoe import TictactoeGame

game_field = TictactoeGame(3)

def dispatch(address, method, args):
    if method == "set_new_player":
        state = game_field.set_new_player(address)

    if method == "put":
        state = game_field.put(address, args["position"])

    if method == "show":
        state = game_field.show()
    return state


def loop_handler(connection, address):
    while True:
        bin_data = connection.recv(1024)
        if not bin_data:
            break
        str_data = bin_data.decode()
        dict_data = json.loads(str_data)

        method = dict_data["method"]
        args = dict_data["args"]
        state = dispatch(address, method, args)
        message = state[1].encode()
        conn.sendall(message)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 65432
sock.bind((HOST, PORT))
sock.listen(2)

client_list = []
while True:
    try:
        conn, addr = sock.accept()
        print("hoge")
    except KeyboardInterapt:
        sock.close()
        exit()
        break
    print("[client address]=>{}".format(addr[0]))
    print("[client port]=>{}".format(addr[1]))
    client_list.append((conn, addr))
    dispatch(addr, "set_new_player", {})
    thread = threading.Thread(target = loop_handler, args = (conn, addr))
    thread.start()

