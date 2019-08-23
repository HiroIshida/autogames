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

    def send_move(self, position):
        args = {'position': position}
        try:
            data = dict()
            data["args"] = args
            str_data = json.dumps(data)
            message_send = str_data.encode()
            self.client.sendall(message_send)
        except BrokenPipeError:
            print("Game Finished")
            os._exit(0)

    def wait_for_my_turn(self):
        received_message = self.client.recv(1024).decode()
        try:
            # receive latest field data from server
            self.game_field.field = json.loads(received_message)['data']
        except json.decoder.JSONDecodeError:
            exit()

    def join_game(self):
        while True:
            time.sleep(0.1)
            # wait until receiving current field state
            self.wait_for_my_turn()
            # execute my turn
            self.send_move(self.game_field.think())


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
    client.joint_game()
