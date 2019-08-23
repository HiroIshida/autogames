#!/usr/bin/env python3
# http://edosha.hatenablog.jp/entry/2017/09/05/174453

# for python2 to use absolute path (python3 uses absolute path by default)
from __future__ import absolute_import

import argparse
import os
import socket
import time
import json
from games.tictactoe_game import TictactoeGame
from games import get_game_titles


class Client:

    def __init__(self, game_title):
        # you can see available game list by command below
        # python client.py --list-games or python client.py -l
        game_instances = {'tictactoe_game': TictactoeGame(3)}
        self.game_field = game_instances[game_title]

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
        message_recieved = self.client.recv(1024).decode()

        method = "put"
        args = {'position': position}
        try:
            self._send(method, args)
        except BrokenPipeError:
            print("Game Finished")
            os._exit(0)

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

    def main(self):
        while True:
            time.sleep(0.1)
            self.put(self.game_field.think())


if __name__ == '__main__':
    # pick up available game titles from scripts/games
    game_titles = get_game_titles()

    # parse command line arguments
    parser = argparse.ArgumentParser(description='description of server.py')
    parser.add_argument('-g', '--game', choices=game_titles,
                        help='set game title which you want to play')
    parser.add_argument('-l', '--list-games', action='store_true',
                        help='show all game titles which you can play')
    args = parser.parse_args()

    # show all game titles
    if args.list_games is True:
        print('you must choose game title from below:')
        print(game_titles)
        exit()

    client = Client(args.game)
    client.main()
